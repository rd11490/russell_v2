import argparse

from src.utils.arg_parser import *
from src.utils.client import smart, MeasureType
from src.utils.storage import *
from src.utils.utils import *


def download_box_scores_traditional(season, season_type):
    download_and_store_player_box_scores(season, season_type)
    download_and_store_team_box_scores(season, season_type)


def download_and_store_player_box_scores(season, season_type):
    box_score_data = smart.get_player_game_log(season=season, season_type=season_type, measure_type=MeasureType.Base)
    player_stats = clean_df(add_season_and_type(box_score_data, season, season_type))
    mysql_client.write(player_stats, table=player_box_score_traditional)


def download_and_store_team_box_scores(season, season_type):
    box_score_data = smart.get_teams_game_log(season=season, season_type=season_type, measure_type=MeasureType.Base)
    team_stats = clean_df(add_season_and_type(box_score_data, season, season_type))
    mysql_client.write(team_stats, table=team_box_score_traditional)


def clean_df(df):
    return rename_tov(fill_na(df))


def fill_na(df):
    return df.fillna(value={'MIN': '0:00'}).fillna(0.0)


def rename_tov(df):
    return df.rename(columns={"TO": "TOV"})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season stats')
    season_arg(parser)
    season_type_arg(parser)
    args = parser.parse_args()

    download_box_scores_traditional(args.season, args.season_type)
