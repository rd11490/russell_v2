import argparse

from src.utils.client import smart
from src.utils.storage import *
from src.utils.utils import *
from src.utils.arg_parser import *

def download_box_scores(season, season_type):
    where_clause = "SEASON = '{}' and SEASON_TYPE = '{}'".format(season, season_type)
    game_log = mysql_client.read_table(table=game_log_table, where=where_clause)
    for game_id in game_log['GAME_ID'].unique():
        print(game_id)
        box_score_data = download_box_score(game_id=game_id)
        team_stats = clean_df(add_season_and_type(box_score_data['TeamStats'], season, season_type))
        player_stats = clean_df(add_season_and_type(box_score_data['PlayerStats'], season, season_type))
        try:
            mysql_client.write(team_stats, table=team_box_score_traditional)
        except:
            print(team_stats)
            raise Exception("Writing to DB failed!")

        try:
            mysql_client.write(player_stats, table=player_box_score_traditional)
        except:
            print(player_stats)
            raise Exception("Writing to DB failed!")

        api_rate_limit()


def clean_df(df):
    return rename_tov(fill_na(df))


def fill_na(df):
    return df.fillna(value={'MIN': '0:00'}).fillna(0.0)


def rename_tov(df):
    return df.rename(columns={"TO": "TOV"})


def download_box_score(game_id):
    return smart.box_score_traditional(game_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season stats')
    season_arg(parser)
    season_type_arg(parser)
    game_id_arg(parser)
    args = parser.parse_args()

    if args.game_id is None:
        download_box_scores(args.season, args.season_type)
    else:
        download_box_score(args.game_id)
