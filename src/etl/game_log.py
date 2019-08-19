import argparse

from src.utils.client import smart
from src.utils.storage import *
from src.utils.utils import *


def download_game_log(season, season_type):
    print('Downloading season game log for season: {0}, season_tyoe: {1}'.format(season, season_type))
    season_game_log = smart.get_teams_game_log(season=season, season_type=season_type)
    season_game_log = add_season_and_type(season_game_log, season, season_type)
    return season_game_log

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season stats')
    parser.add_argument('-s', '--season', action="store", dest='season', help='The season you are trying to download')
    parser.add_argument('-st', '--seasonType', action="store", dest='season_type',
                        help='The season type you are trying to download')
    args = parser.parse_args()
    game_log = download_game_log(args.season, args.season_type)
    mysql_client.write(game_log, game_log_table)

