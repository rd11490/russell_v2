import argparse

from src.utils.arg_parser import *
from src.utils.client import smart
from src.utils.storage import *
from src.utils.utils import *


def download_win_probability_for_season(season, season_type, delta):
    where_clause = "SEASON = '{}' and SEASON_TYPE = '{}'".format(season, season_type)
    game_log = mysql_client.read_table(table=game_log_table, where=where_clause)
    if delta:
        advanced_complete = mysql_client.read_table(win_probability, where_clause)
        log_ids = set(game_log['GAME_ID'].unique())
        pbp_ids = set(advanced_complete['GAME_ID'].unique())
        game_ids = log_ids - pbp_ids
    else:
        game_ids = game_log['GAME_ID'].unique()

    for game_id in game_ids:
        download_and_store_from_game_id(game_id, season, season_type)
        api_rate_limit()


def download_and_store_from_game_id(game_id, season, season_type):
    print(game_id)
    win_prob_resp = download_win_probability(game_id=game_id)
    win_prob_df = clean_df(add_season_and_type(win_prob_resp['WinProbPBP'], season, season_type))
    try:
        mysql_client.write(win_prob_df, table=win_probability)
    except:
        print(win_prob_df)
        raise Exception("Writing to DB failed!")


def clean_df(df):
    return fill_na(df)


def fill_na(df):
    return df.fillna(value={'MIN': '0:00'}).fillna(0.0)


def download_win_probability(game_id):
    return smart.win_probability(game_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season stats')
    season_arg(parser)
    season_type_arg(parser)
    game_id_arg(parser)
    delta_arg(parser)
    args = parser.parse_args()

    if args.game_id is None:
        download_win_probability_for_season(args.season, args.season_type, args.delta)
    else:
        season = extract_season_from_game_id(args.game_id)
        season_type = extract_season_type_from_game_id(args.game_id)
        download_and_store_from_game_id(args.game_id, season, season_type)
