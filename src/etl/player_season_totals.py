import argparse

from src.utils.arg_parser import *
from src.utils.client import smart, MeasureType
from src.utils.storage import *
from src.utils.utils import *


def download_traditional_stats(season, season_type):
    traditional_stats = download_player_season_stats(season=season, season_type=season_type,
                                                     measure_type=MeasureType.Base)
    traditional_stats = traditional_stats[
        ['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM',
         'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV',
         'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'NBA_FANTASY_PTS', 'DD2', 'TD3', 'SEASON',
         'SEASON_TYPE']]

    traditional_stats = clean_fa(traditional_stats)

    mysql_client.write(traditional_stats, player_season_totals_traditional)


def download_advanced_stats(season, season_type):
    advanced_stats = download_player_season_stats(season, season_type, MeasureType.Advanced)
    advanced_stats = advanced_stats[
        ['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'W', 'L', 'W_PCT', 'MIN',
         'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_PCT', 'AST_TO', 'AST_RATIO', 'OREB_PCT', 'DREB_PCT',
         'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'USG_PCT', 'PACE', 'PACE_PER40', 'PIE', 'POSS', 'FGM', 'FGA',
         'FGM_PG', 'FGA_PG', 'FG_PCT', 'SEASON', 'SEASON_TYPE']]

    advanced_stats = clean_fa(advanced_stats)

    mysql_client.write(advanced_stats, player_season_totals_advanced)


def download_player_season_stats(season, season_type, measure_type):
    print('Downloading player season totals for season: {0}, season_tyoe: {1}, measure_type: {2}'.format(season,
                                                                                                         season_type,
                                                                                                         measure_type))
    player_season_base_stats_totals = smart.player_season_totals(season=season, season_type=season_type,
                                                                 measure_type=measure_type)
    player_season_base_stats_totals = add_season_and_type(player_season_base_stats_totals, season, season_type)
    return player_season_base_stats_totals


def clean_fa(df):
    df['TEAM_ID'] = df['TEAM_ID'].fillna('-1')
    df['TEAM_ABBREVIATION'] = df['TEAM_ABBREVIATION'].fillna('FA')
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download player season stats')
    season_arg(parser)
    season_type_arg(parser)
    run_all_arg(parser)

    parser.add_argument('-t', '--traditional_stats', action='store_true', dest='traditional_stats',
                        help='download advanced stats')
    parser.add_argument('-a', '--advanced_stats', action='store_true', dest='advanced_stats',
                        help='download advanced stats')

    args = parser.parse_args()

    if args.traditional_stats or args.run_all:
        download_traditional_stats(args.season, args.season_type)

    if args.advanced_stats or args.run_all:
        download_advanced_stats(args.season, args.season_type)
