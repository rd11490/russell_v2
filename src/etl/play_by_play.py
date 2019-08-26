import argparse

from src.utils.arg_parser import *
from src.utils.client import smart
from src.utils.storage import *
from src.utils.utils import *


def download_play_by_play(season, season_type, delta):
    where_clause = "SEASON = '{}' and SEASON_TYPE = '{}'".format(season, season_type)
    game_log = mysql_client.read_table(table=game_log_table, where=where_clause)
    if delta:
        play_by_play_complete = mysql_client.read_table(play_by_play, where_clause)
        log_ids = set(game_log['GAME_ID'].unique())
        pbp_ids = set(play_by_play_complete['GAME_ID'].unique())
        game_ids = log_ids - pbp_ids
        print(len(log_ids))
        print(len(pbp_ids))
        print(len(game_ids))
    else:
        game_ids = game_log['GAME_ID'].unique()
        print(len(game_ids))

    for game_id in game_ids:
        print(game_id)
        download_and_write_play_by_play(game_id, season, season_type)
        api_rate_limit()


def clean_df(df):
    return fill_na(df)


def fill_na(df):
    return df.fillna(value={'MIN': '0:00', 'SCOREMARGIN' : 'TIE'}).fillna('')


def download_game_play_by_play(game_id):
    return smart.play_by_play(game_id)


def download_and_write_play_by_play(game_id, season, season_type):
    play_by_play_data = download_game_play_by_play(game_id=game_id)
    play_by_play_data = clean_df(add_season_and_type(play_by_play_data, season, season_type))
    try:
        mysql_client.write(play_by_play_data, table=play_by_play)
    except:
        print(play_by_play)
        raise Exception("Writing to DB failed!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season stats')
    season_arg(parser)
    season_type_arg(parser)
    game_id_arg(parser)
    delta_arg(parser)
    args = parser.parse_args()

    if args.game_id is None:
        download_play_by_play(args.season, args.season_type, args.delta)
    else:
        print(download_game_play_by_play(args.game_id))