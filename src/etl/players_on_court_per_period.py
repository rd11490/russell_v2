import argparse

import pandas as pd

from src.utils.arg_parser import *
from src.utils.client import smart
from src.utils.storage import *
from src.utils.utils import *

import multiprocessing as mp


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


def length_of_period(period):
    if period < 5:
        return 12 * 60
    else:
        return 5 * 60


def calculate_time_at_period(period):
    if period > 5:
        return (720 * 4 + (period - 5) * (5 * 60))
    else:
        return (720 * (period - 1))


def convert_time_to_seconds(row):
    period = row['PERIOD']
    time_str = row['PCTIMESTRING']
    mins, sec = time_str.split(':')
    time_at_start = calculate_time_at_period(period) * 10
    len_of_period = length_of_period(period)
    min_int = int(mins) * 60
    sec_int = int(sec)
    time_elapsed = len_of_period - (min_int + sec_int)
    return time_at_start + time_elapsed


def split_subs(df, tag):
    subs = df[[tag, 'PERIOD', 'EVENTNUM', 'TIME']]
    subs['SUB'] = tag
    subs.columns = ['PLAYER_ID', 'PERIOD', 'EVENTNUM', 'TIME', 'SUB']
    return subs


def download_players_at_start_of_period(game_id, season, season_type):
    where_clause = "SEASON = '{}' and SEASON_TYPE = '{}' and GAME_ID = '{}'".format(season, season_type, game_id)
    frame = mysql_client.read_table(play_by_play, where_clause)
    print('Got Data for {}'.format(game_id))
    substitutions_only = frame[frame["EVENTMSGTYPE"] == 8][
        ['PERIOD', 'EVENTNUM', 'PLAYER1_ID', 'PLAYER2_ID', 'PCTIMESTRING']]
    substitutions_only['PCTIMESTRING'] = substitutions_only.apply(convert_time_to_seconds, axis=1)
    substitutions_only.columns = ['PERIOD', 'EVENTNUM', 'OUT', 'IN', 'TIME']
    subs_in = split_subs(substitutions_only, 'IN')
    subs_out = split_subs(substitutions_only, 'OUT')

    full_subs = pd.concat([subs_out, subs_in], axis=0).reset_index()[['PLAYER_ID', 'PERIOD', 'EVENTNUM', 'SUB', 'TIME']]

    full_subs = full_subs.sort_values(by=['TIME', 'EVENTNUM'])
    first_event_of_period = full_subs.loc[full_subs.groupby(by=['PERIOD', 'PLAYER_ID'])['TIME'].idxmin()]
    players_subbed_in_at_each_period = first_event_of_period[first_event_of_period['SUB'] == 'IN'][
        ['PLAYER_ID', 'PERIOD', 'SUB']]

    periods = players_subbed_in_at_each_period['PERIOD'].drop_duplicates().values.tolist()

    frames = []

    for period in periods:
        low = 10 * calculate_time_at_period(period) + 5
        high = 10 * calculate_time_at_period(period + 1) - 5
        boxscore = smart.box_score_traditional(game_id=game_id, range_type=2, start_range=low, end_range=high)
        boxscore_players = boxscore['PlayerStats'][['PLAYER_NAME', 'PLAYER_ID', 'TEAM_ID']].copy(True)
        boxscore_players['PERIOD'] = period
        boxscore_players['PLAYER_ID'] = boxscore_players['PLAYER_ID'].astype(str)
        players_subbed_in_at_period = players_subbed_in_at_each_period[
            players_subbed_in_at_each_period['PERIOD'] == period]

        joined_players = pd.merge(boxscore_players, players_subbed_in_at_period, on=['PLAYER_ID', 'PERIOD'], how='left')
        joined_players = joined_players[pd.isnull(joined_players['SUB'])][
            ['PLAYER_NAME', 'PLAYER_ID', 'TEAM_ID', 'PERIOD']]

        if joined_players.shape[0] != 10:
            print(game_id)
            print(players_subbed_in_at_period)
            print(boxscore_players)
            print(joined_players)
            raise Exception('Incorrect Number of players found for {} - {}'.format(game_id, period))
        frames.append(joined_players)

    players = pd.concat(frames)
    players['GAME_ID'] = game_id
    players['SEASON'] = season
    players['SEASON_TYPE'] = season_type

    mysql_client.write(players, players_on_court_per_period)


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
        season = extract_season_from_game_id(args.game_id)
        season_type = extract_season_type_from_game_id(args.game_id)
        download_players_at_start_of_period(args.game_id, season, season_type)
