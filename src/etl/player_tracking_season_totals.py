import argparse

from src.utils.arg_parser import *
from src.utils.client import smart, PtMeasureType
from src.utils.storage import *
from src.utils.utils import *

"""
    Rebounding = 'Rebounding'
    Efficiency = 'Efficiency'
    SpeedDistance = 'SpeedDistance'
    ElbowTouches = 'ElbowTouch'
    PostTouches = 'PostTouch'
    PaintTouches = 'PaintTouch'
"""


def download_player_player_tracking_stats(season, season_type, pt_measure_type):
    print('Downloading player season totals for season: {0}, season_tyoe: {1}, measure_type: {2}'.format(season,
                                                                                                         season_type,
                                                                                                         pt_measure_type))
    player_season_pt_stats_totals = smart.player_season_tracking(season=season, season_type=season_type,
                                                                 pt_measure_type=pt_measure_type)
    player_season_pt_stats_totals = add_season_and_type(player_season_pt_stats_totals, season, season_type)
    return player_season_pt_stats_totals


def clean_fa(df):
    df['TEAM_ID'] = df['TEAM_ID'].fillna('-1')
    df['TEAM_ABBREVIATION'] = df['TEAM_ABBREVIATION'].fillna('FA')
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download player season stats')
    season_arg(parser)
    season_type_arg(parser)
    run_all_arg(parser)

    parser.add_argument('-d', '--drives', action='store_true', dest='drives',
                        help='Download Player Tracking Drive stats')

    parser.add_argument('-def', '--defense', action='store_true', dest='defense',
                        help='Download Player Tracking Defense stats')

    parser.add_argument('-cs', '--catch_and_shoot', action='store_true', dest='catch_and_shoot',
                        help='Download Player Tracking Catch and Shoot stats')

    parser.add_argument('-p', '--passing', action='store_true', dest='passing',
                        help='Download Player Tracking Passing stats')

    parser.add_argument('-t', '--touches', action='store_true', dest='touches',
                        help='Download Player Tracking Touches stats')

    parser.add_argument('-pus', '--pull_up_shots', action='store_true', dest='pull_up_shots',
                        help='Download Player Tracking Pull Up Shot stats')

    parser.add_argument('-rbd', '--rebounding', action='store_true', dest='rebounding',
                        help='Download Player Tracking Rebounding stats')

    args = parser.parse_args()

    if args.drives or args.run_all:
        stats = download_player_player_tracking_stats(args.season, args.season_type, PtMeasureType.Drives)
        stats = clean_fa(stats)
        mysql_client.write(stats, player_tracking_drives)

    if args.defense or args.run_all:
        stats = download_player_player_tracking_stats(args.season, args.season_type, PtMeasureType.Defense)
        stats = clean_fa(stats)
        mysql_client.write(stats, player_tracking_defense)

    if args.catch_and_shoot or args.run_all:
        stats = download_player_player_tracking_stats(args.season, args.season_type, PtMeasureType.CatchAndShoot)
        stats = clean_fa(stats)
        mysql_client.write(stats, player_tracking_catch_and_shoot)

    if args.passing or args.run_all:
        stats = download_player_player_tracking_stats(args.season, args.season_type, PtMeasureType.Passing)
        stats = clean_fa(stats)
        mysql_client.write(stats, player_tracking_passing)

    if args.touches or args.run_all:
        stats = download_player_player_tracking_stats(args.season, args.season_type, PtMeasureType.Touches)
        stats = clean_fa(stats)
        mysql_client.write(stats, player_tracking_touches)

    if args.pull_up_shots or args.run_all:
        stats = download_player_player_tracking_stats(args.season, args.season_type, PtMeasureType.PullUp)
        stats = clean_fa(stats)
        mysql_client.write(stats, player_tracking_pull_up_shots)

    if args.rebounding or args.run_all:
        stats = download_player_player_tracking_stats(args.season, args.season_type, PtMeasureType.Rebounding)
        stats = clean_fa(stats)
        print(stats.columns)
        print(stats.head(10))