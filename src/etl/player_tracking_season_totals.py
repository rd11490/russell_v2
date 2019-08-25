import argparse

from src.utils.arg_parser import *
from src.utils.client import smart, PtMeasureType
from src.utils.storage import *
from src.utils.utils import *


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


def retrieve_data(season, season_type, pt_measure_type, table):
    stats = download_player_player_tracking_stats(season, season_type, pt_measure_type)
    stats = clean_fa(stats)
    stats = stats.fillna(0.0)
    mysql_client.write(stats, table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download player season stats')
    season_arg(parser)
    season_type_arg(parser)
    run_all_arg(parser)

    parser.add_argument('-drv', '--drives', action='store_true', dest='drives',
                        help='Download Player Tracking Drive stats')

    parser.add_argument('-def', '--defense', action='store_true', dest='defense',
                        help='Download Player Tracking Defense stats')

    parser.add_argument('-cs', '--catch_and_shoot', action='store_true', dest='catch_and_shoot',
                        help='Download Player Tracking Catch and Shoot stats')

    parser.add_argument('-pas', '--passing', action='store_true', dest='passing',
                        help='Download Player Tracking Passing stats')

    parser.add_argument('-tch', '--touches', action='store_true', dest='touches',
                        help='Download Player Tracking Touches stats')

    parser.add_argument('-pus', '--pull_up_shots', action='store_true', dest='pull_up_shots',
                        help='Download Player Tracking Pull Up Shot stats')

    parser.add_argument('-rbd', '--rebounding', action='store_true', dest='rebounding',
                        help='Download Player Tracking Rebounding stats')

    parser.add_argument('-efg', '--efficiency', action='store_true', dest='efficiency',
                        help='Download Player Tracking Efficiency stats')

    parser.add_argument('-spd', '--speed', action='store_true', dest='speed',
                        help='Download Player Tracking Speed and Distance stats')

    parser.add_argument('-elb', '--elbow_touches', action='store_true', dest='elbow_touches',
                        help='Download Player Tracking Elbow Touches stats')

    parser.add_argument('-pst', '--post_touches', action='store_true', dest='post_touches',
                        help='Download Player Tracking Post Touches stats')

    parser.add_argument('-pnt', '--paint_touches', action='store_true', dest='paint_touches',
                        help='Download Player Tracking Paint Touches stats')

    args = parser.parse_args()

    if args.drives or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.Drives, player_tracking_drives)

    if args.defense or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.Defense, player_tracking_defense)

    if args.catch_and_shoot or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.CatchAndShoot, player_tracking_catch_and_shoot)

    if args.passing or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.Passing, player_tracking_passing)

    if args.touches or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.Touches, player_tracking_touches)

    if args.pull_up_shots or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.PullUp, player_tracking_pull_up_shots)

    if args.rebounding or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.Rebounding, player_tracking_rebounds)

    if args.efficiency or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.Efficiency, player_tracking_efficiency)

    if args.speed or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.SpeedDistance, player_tracking_speed_and_distance)

    if args.elbow_touches or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.ElbowTouches, player_tracking_elbow_touches)

    if args.post_touches or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.PostTouches, player_tracking_post_touches)

    if args.paint_touches or args.run_all:
        retrieve_data(args.season, args.season_type, PtMeasureType.PaintTouches, player_tracking_paint_touches)
