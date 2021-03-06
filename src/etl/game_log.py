import argparse

from src.utils.arg_parser import *
from src.utils.client import smart
from src.utils.storage import *
from src.utils.utils import *


def download_game_log(season, season_type):
    print('Downloading season game log for season: {0}, season_tyoe: {1}'.format(season, season_type))
    season_game_log = smart.get_teams_game_log(season=season, season_type=season_type)
    season_game_log = add_season_and_type(season_game_log, season, season_type)
    game_log = season_game_log.fillna(0.0)
    mysql_client.write(game_log, game_log_table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season stats')
    season_arg(parser)
    season_type_arg(parser)

    args = parser.parse_args()
    download_game_log(args.season, args.season_type)

