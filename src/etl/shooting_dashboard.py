import argparse
import multiprocessing as mp

from src import add_season_and_type
from src.utils.arg_parser import *
from src.utils.client import smart
from src.utils.storage import *


def download_season_shot_dashboard(season, season_type, delta):
    where_clause = "SEASON = '{}' and SEASON_TYPE = '{}'".format(season, season_type)
    players = mysql_client.read_table(table=player_box_score_traditional, where=where_clause)
    players = players['PLAYER_ID'].drop_duplicates().values

    if delta:
        print(len(players))
        players_delta = mysql_client.read_table(table=general_shooting, where=where_clause)['PLAYER_ID'].drop_duplicates().values
        players = set(players) - set(players_delta)
        print(len(players))

    for p in players:
        download_player_shot_dashboard(p, season, season_type)
    # pool = mp.Pool(mp.cpu_count())
    # results = []
    #
    # for p in players:
    #     out = pool.apply_async(download_player_shot_dashboard, args=(p, season, season_type))
    #     results.append(out)
    #
    # pool.close()
    # pool.join()
    #
    # print('WAITING FOR GETS')
    # result = [r.get() for r in results]
    # print(result)


def download_player_shot_dashboard(player, season, season_type):
    print("Downloading shots for Player: {}".format(player))
    download_and_write_shot_dashboard(player_id=player, season=season, season_type=season_type)


def clean_df(df):
    return fill_na(df)


def fill_na(df):
    return df.fillna(0)


def download_and_write_shot_dashboard(player_id, season, season_type):
    print('Downloading Shots for {} - {} - {}'.format(player_id, season, season_type))
    shots = download_shot_dashboard(player_id=player_id, season=season, season_type=season_type)

    # try:
    if 'ShotClockShooting' in shots.keys():
        shots_frame = add_season_and_type(clean_df(shots['ShotClockShooting']), season=season, season_type=season_type)
        mysql_client.write(shots_frame, shot_clock_shooting)

    if 'GeneralShooting' in shots.keys():
        shots_frame = add_season_and_type(clean_df(shots['GeneralShooting']), season=season, season_type=season_type)
        mysql_client.write(shots_frame, general_shooting)

    if 'TouchTimeShooting' in shots.keys():
        shots_frame = add_season_and_type(clean_df(shots['TouchTimeShooting']), season=season, season_type=season_type)
        mysql_client.write(shots_frame, touch_time_shooting)

    if 'DribbleShooting' in shots.keys():
        shots_frame = add_season_and_type(clean_df(shots['DribbleShooting']), season=season, season_type=season_type)
        mysql_client.write(shots_frame, dribble_shooting)

    if 'ClosestDefender10ftPlusShooting' in shots.keys():
        shots_frame = add_season_and_type(clean_df(shots['ClosestDefender10ftPlusShooting']), season=season,
                                          season_type=season_type)
        mysql_client.write(shots_frame, closet_defender_shooting_10_plus)

    if 'ClosestDefenderShooting' in shots.keys():
        shots_frame = add_season_and_type(clean_df(shots['ClosestDefenderShooting']), season=season,
                                          season_type=season_type)
        mysql_client.write(shots_frame, closet_defender_shooting)

        # except:
        #     raise Exception("Writing to DB failed!")


def download_shot_dashboard(player_id, season, season_type):
    return smart.shooting_dashboard(player_id=player_id, season=season, season_type=season_type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season shot dashboard')
    season_arg(parser)
    season_type_arg(parser)
    player_id_arg(parser)
    delta_arg(parser)

    args = parser.parse_args()

    if args.player_id is None or args.team_id is None:
        download_season_shot_dashboard(args.season, args.season_type, args.delta)
    else:
        download_and_write_shot_dashboard(args.player_id, args.season, args.season_type)
