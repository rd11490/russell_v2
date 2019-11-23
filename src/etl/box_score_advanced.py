import argparse

from src.utils.arg_parser import *
from src.utils.client import smart
from src.utils.storage import *
from src.utils.utils import *

import multiprocessing as mp


def download_box_scores_advanced(season, season_type, delta):
    where_clause = "SEASON = '{}' and SEASON_TYPE = '{}'".format(season, season_type)
    game_log = mysql_client.read_table(table=game_log_table, where=where_clause)
    if delta:
        advanced_complete = mysql_client.read_table(team_box_score_advanced, where_clause)
        log_ids = set(game_log['GAME_ID'].unique())
        pbp_ids = set(advanced_complete['GAME_ID'].unique())
        game_ids = log_ids - pbp_ids
    else:
        game_ids = game_log['GAME_ID'].unique()

    for game_id in game_ids:
        download_and_write_box_score(game_id, season, season_type)
    # pool = mp.Pool(int(mp.cpu_count()))
    # results = []
    #
    # for game_id in game_ids:
    #     out = pool.apply_async(download_and_write_box_score, args=(game_id, season, season_type))
    #     results.append(out)
    #
    # pool.close()
    # pool.join()
    #
    # print('WAITING FOR GETS')
    # result = [r.get() for r in results]
    # print(result)


def clean_df(df):
    return rename_tov(fill_na(df))


def fill_na(df):
    return df.fillna(value={'MIN': '0:00'}).fillna(0.0)


def rename_tov(df):
    return df.rename(columns={"TO": "TOV"})


def download_box_score(game_id):
    return smart.box_score_advanced(game_id)


def download_and_write_box_score(game_id, season, season_type):
    print(game_id)
    box_score_data = download_box_score(game_id=game_id)
    team_stats = clean_df(add_season_and_type(box_score_data['TeamStats'], season, season_type))
    player_stats = clean_df(add_season_and_type(box_score_data['PlayerStats'], season, season_type))

    mysql_client.write(team_stats, table=team_box_score_advanced)
    mysql_client.write(player_stats, table=player_box_score_advanced)

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season stats')
    season_arg(parser)
    season_type_arg(parser)
    game_id_arg(parser)
    delta_arg(parser)

    args = parser.parse_args()

    if args.game_id is None:
        download_box_scores_advanced(args.season, args.season_type, args.delta)
    else:
        season = extract_season_from_game_id(args.game_id)
        season_type = extract_season_type_from_game_id(args.game_id)
        download_and_write_box_score(args.game_id, season, season_type)
