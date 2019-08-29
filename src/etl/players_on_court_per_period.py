import argparse

import pandas as pd

from src.utils.arg_parser import *
from src.utils.client import smart
from src.utils.storage import *
from src.utils.utils import *


def download_players_on_court_for_season(season, season_type, delta):
    where_clause = "SEASON = '{}' and SEASON_TYPE = '{}'".format(season, season_type)
    game_log = mysql_client.read_table(table=game_log_table, where=where_clause)
    if delta:
        play_by_play_complete = mysql_client.read_table(players_on_court_per_period, where_clause)
        log_ids = set(game_log['GAME_ID'].unique())
        pbp_ids = set(play_by_play_complete['GAME_ID'].unique())
        game_ids = log_ids - pbp_ids
    else:
        game_ids = game_log['GAME_ID'].unique()

    for game_id in game_ids:
        print(game_id)
        download_players_at_start_of_period(game_id, season, season_type)
        api_rate_limit()


def calculate_time_at_period(period):
    if period > 5:
        return (720 * 4 + (period - 5) * (5 * 60)) * 10
    else:
        return (720 * (period - 1)) * 10


def split_subs(df, tag):
    subs = df[[tag, 'PERIOD', 'EVENTNUM']]
    subs['SUB'] = tag
    subs.columns = ['PLAYER_ID', 'PERIOD', 'EVENTNUM', 'SUB']
    return subs


def download_players_at_start_of_period(game_id, season, season_type):
    where_clause = "SEASON = '{}' and SEASON_TYPE = '{}' and GAME_ID = '{}'".format(season, season_type, game_id)
    frame = mysql_client.read_table(play_by_play, where_clause)
    substitutions_only = frame[frame["EVENTMSGTYPE"] == 8][['PERIOD', 'EVENTNUM', 'PLAYER1_ID', 'PLAYER2_ID']]
    substitutions_only.columns = ['PERIOD', 'EVENTNUM', 'OUT', 'IN']
    subs_in = split_subs(substitutions_only, 'IN')
    subs_out = split_subs(substitutions_only, 'OUT')

    full_subs = pd.concat([subs_out, subs_in], axis=0).reset_index()[['PLAYER_ID', 'PERIOD', 'EVENTNUM', 'SUB']]
    first_event_of_period = full_subs.loc[full_subs.groupby(by=['PERIOD', 'PLAYER_ID'])['EVENTNUM'].idxmin()]
    players_subbed_in_at_each_period = first_event_of_period[first_event_of_period['SUB'] == 'IN'][
        ['PLAYER_ID', 'PERIOD', 'SUB']]

    periods = players_subbed_in_at_each_period['PERIOD'].drop_duplicates().values.tolist()

    frames = []
    for period in periods:
        low = calculate_time_at_period(period) + 5
        high = calculate_time_at_period(period + 1) - 5
        boxscore = smart.box_score_traditional(game_id=game_id, range_type=2, start_range=low, end_range=high)
        boxscore_players = boxscore['PlayerStats'][['PLAYER_NAME', 'PLAYER_ID', 'TEAM_ID']].copy(True)
        boxscore_players['PERIOD'] = period
        boxscore_players['PLAYER_ID'] = boxscore_players['PLAYER_ID'].astype(str)
        players_subbed_in_at_period = players_subbed_in_at_each_period[
            players_subbed_in_at_each_period['PERIOD'] == period]

        joined_players = pd.merge(boxscore_players, players_subbed_in_at_period, on=['PLAYER_ID', 'PERIOD'], how='left')
        joined_players = joined_players[pd.isnull(joined_players['SUB'])][
            ['PLAYER_NAME', 'PLAYER_ID', 'TEAM_ID', 'PERIOD']]
        frames.append(joined_players)

    players = pd.concat(frames)
    players['GAME_ID'] = game_id
    players['SEASON'] = season
    players['SEASON_TYPE'] = season_type
    mysql_client.write(players, players_on_court_per_period)
    api_rate_limit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season stats')
    season_arg(parser)
    season_type_arg(parser)
    game_id_arg(parser)
    delta_arg(parser)
    args = parser.parse_args()

    if args.game_id is None:
        download_players_on_court_for_season(args.season, args.season_type, args.delta)
    else:
        pass
