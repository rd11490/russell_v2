import argparse

from src.utils.arg_parser import *
from src.utils.client import smart
from src.utils.storage import *
from src.utils.utils import *
import multiprocessing as mp


def download_season_shots(season, season_type):
    where_clause = "SEASON = '{}' and SEASON_TYPE = '{}'".format(season, season_type)
    players = mysql_client.read_table(table=player_box_score_traditional, where=where_clause)
    players = players[['PLAYER_ID', 'TEAM_ID']].drop_duplicates()

    pool = mp.Pool(mp.cpu_count())
    results = []

    for p in players.index:
        out = pool.apply_async(download_player_shots, args=(players, p, season, season_type))
        results.append(out)

    pool.close()
    pool.join()

    print('WAITING FOR GETS')
    result = [r.get() for r in results]
    print(result)


def download_player_shots(players, p, season, season_type):
    player = players.loc[p, 'PLAYER_ID']
    team = players.loc[p, 'TEAM_ID']

    print("Downloading shots for Player: {} - Team: {}".format(player, team))
    download_and_write_shots(player_id=player, team_id=team, season=season, season_type=season_type)


def download_and_write_shots(player_id, team_id, season, season_type):
    print('Downloading Shots for {} - {} - {} - {}'.format(player_id, team_id, season, season_type))
    shots = download_player_shot_chart(player_id=player_id, team_id=team_id, season=season, season_type=season_type)
    if shots.shape[0] == 0:
        return
    shots = clean_df(add_season_and_type(shots, season, season_type))
    try:
        mysql_client.write(shots, table=shot_chart_detail)
    except:
        print(shots)
        raise Exception("Writing to DB failed!")


def clean_df(df):
    return fill_na(df)


def fill_na(df):
    return df.fillna(value={'MIN': '0:00', 'SCOREMARGIN': 'TIE'}).fillna('')


def download_player_shot_chart(player_id, team_id, season, season_type):
    return smart.get_shot_chart_detail(player_id=player_id, team_id=team_id, season=season, season_type=season_type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download season stats')
    season_arg(parser)
    season_type_arg(parser)
    player_id_arg(parser)
    team_id_arg(parser)

    args = parser.parse_args()

    if args.player_id is None or args.team_id is None:
        download_season_shots(args.season, args.season_type)
    else:
        download_and_write_shots(args.player_id, args.team_id, args.season, args.season_type)
