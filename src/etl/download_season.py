import argparse

from src.etl.box_score_advanced import download_box_scores_advanced
from src.etl.box_score_traditional import download_box_scores_traditional
from src.etl.game_log import download_game_log
from src.etl.play_by_play import download_play_by_play
from src.etl.player_season_totals import download_advanced_stats, download_traditional_stats
from src.etl.player_tracking_season_totals import download_all_tracking_stats
from src.etl.players_on_court_per_period import download_players_on_court_for_season
from src.utils.arg_parser import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season stats')
    season_arg(parser)
    season_type_arg(parser)
    delta_arg(parser)
    run_all_arg(parser)

    parser.add_argument('-gl', '--game_log', action='store_true', dest='game_log',
                        help='Download Game Log')

    parser.add_argument('-box', '--box_scores', action='store_true', dest='box_scores',
                        help='Download Box Scores')

    parser.add_argument('-ttl', '--totals', action='store_true', dest='totals',
                        help='Download Traditional Totals')

    parser.add_argument('-trk', '--player_tracking', action='store_true', dest='player_tracking',
                        help='Download Player Tracking Totals')

    parser.add_argument('-pbp', '--play_by_play', action='store_true', dest='play_by_play',
                        help='Download Play by Play')

    parser.add_argument('-poc', '--players_on_court', action='store_true', dest='players_on_court',
                        help='Download Players On Court')

    args = parser.parse_args()

    if args.game_log or args.run_all:
        download_game_log(args.season, args.season_type)

    if args.box_scores or args.run_all:
        download_box_scores_traditional(args.season, args.season_type, args.delta)
        download_box_scores_advanced(args.season, args.season_type, args.delta)

    if args.totals or args.run_all:
        download_traditional_stats(args.season, args.season_type)
        download_advanced_stats(args.season, args.season_type)

    if args.player_tracking or args.run_all:
        download_all_tracking_stats(args.season, args.season_type)
        
    if args.play_by_play or args.run_all:
        download_play_by_play(args.season, args.season_type, args.delta)

    if args.players_on_court or args.run_all:
        download_players_on_court_for_season(args.season, args.season_type, args.delta)
