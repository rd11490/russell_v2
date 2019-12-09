import argparse

from src.utils.arg_parser import *
from src.utils.client import smart
from src.utils.storage import *
from src.utils.utils import *


def download_matchups(season, season_type):
    print('Downloading season defensive matchups for season: {0}, season_tyoe: {1}'.format(season, season_type))
    matchups = smart.get_defensive_matchups(season=season, season_type=season_type)
    matchups = add_season_and_type(matchups, season, season_type)
    matchups = matchups.fillna(0.0)
    mysql_client.write(matchups, defensive_matchups_table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download Defensive Matchups')
    season_arg(parser)
    season_type_arg(parser)

    args = parser.parse_args()
    download_matchups(args.season, args.season_type)

