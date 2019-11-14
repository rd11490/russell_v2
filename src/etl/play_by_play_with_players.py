import argparse

import pandas as pd
import numpy as np

from src.utils.arg_parser import *
from src.utils.storage import *
from src.utils.utils import *

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def isHomeOrAway(value):
    return 'vs' in value


def convert_to_player_array(group):
    home_players = np.sort(group[group['HOME'] == True]['PLAYER_ID'].values)
    home_team = group[group['HOME'] == True]['TEAM_ID'].values[0]

    away_players = np.sort(group[group['HOME'] == False]['PLAYER_ID'].values)
    away_team = group[group['HOME'] == False]['TEAM_ID'].values[0]

    data = {
        'HOME_TEAM': home_team,
        'HOME_PLAYER_1': home_players[0],
        'HOME_PLAYER_2': home_players[1],
        'HOME_PLAYER_3': home_players[2],
        'HOME_PLAYER_4': home_players[3],
        'HOME_PLAYER_5': home_players[4],

        'AWAY_TEAM': away_team,
        'AWAY_PLAYER_1': away_players[0],
        'AWAY_PLAYER_2': away_players[1],
        'AWAY_PLAYER_3': away_players[2],
        'AWAY_PLAYER_4': away_players[3],
        'AWAY_PLAYER_5': away_players[4],
    }

    return pd.Series(data=data)


def play_by_play_with_players(season, season_type):
    where = "SEASON = '{}' AND SEASON_TYPE = '{}'".format(season, season_type)
    # play_by_play_df = mysql_client.read_table(play_by_play, where)
    #
    #
    game_log = mysql_client.read_table(game_log_table, where)
    game_log['HOME'] = game_log['MATCHUP'].apply(isHomeOrAway)
    game_log = game_log[['GAME_ID', 'TEAM_ID', 'HOME']]

    players_at_start_of_period_df = mysql_client.read_table(players_on_court_per_period, where)
    players_at_start_of_period_df = players_at_start_of_period_df.merge(game_log, on=['GAME_ID', 'TEAM_ID'])
    players_at_start_of_period_df = players_at_start_of_period_df.groupby(by=['GAME_ID', 'PERIOD']).apply(
        convert_to_player_array).reset_index()
    print(players_at_start_of_period_df.head(10))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season stats')
    season_arg(parser)
    season_type_arg(parser)
    game_id_arg(parser)
    delta_arg(parser)
    args = parser.parse_args()

    if args.game_id is None:
        play_by_play_with_players(args.season, args.season_type)
    else:
        season = extract_season_from_game_id(args.game_id)
        season_type = extract_season_type_from_game_id(args.game_id)
