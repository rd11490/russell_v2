import multiprocessing as mp
import sys

import numpy as np
import pandas as pd
import requests

from src.utils.storage import *

headers = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Referer': 'https://stats.nba.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}
default_league = '00'
default_season_type = 'Regular Season'

base_url = 'https://stats.nba.com/stats/'


def api_call(endpoint, params):
    return api_call_with_retry(endpoint, params, 10)


def api_call_with_retry(endpoint, params, retries_left=10):
    print('Calling: "{}{}" -- retries remaining: {}'.format(base_url, endpoint, retries_left))
    if retries_left > 0:
        try:
            print("REQUEST!")
            resp = requests.get("{}{}".format(base_url, endpoint), params=params, headers=headers, timeout=(1, 1))
            print(resp)
            if resp.status_code != 200:
                print('Non-200 status code:')
                print(resp.status_code)
                print(resp.request.path_url)
                print(resp.content)
                raise ValueError('{} returned with the status code: {}'.format(endpoint, resp.status_code))

            sets = resp.json()['resultSets']
            results = {}
            for s in sets:
                try:
                    if s['rowSet']:
                        frame = pd.DataFrame(s['rowSet'])
                        frame.columns = s['headers']
                        results[s['name']] = frame
                except:
                    print(resp.request.path_url)
                    print(s)
                    raise Exception("Failed to deserialize the response!")
            print(results)
            return results
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return api_call_with_retry(endpoint, params, retries_left - 1)
    else:
        raise Exception('Number of retries exceeded')


def get_shots(player_id, team_id):
    if player_id is None:
        raise ValueError("Must provide a Team Id")
    if team_id is None:
        raise ValueError("Must provide a Team Id")
    params = (
        ('leagueId', '00'),
        ('season', '2018-19'),
        ('seasonType', 'Regular Season'),
        ('teamId', team_id),
        ('playerId', player_id),
        ('gameID', ''),
        ('outcome', ''),
        ('location', ''),
        ('month', '0'),
        ('seasonSegment', ''),
        ('dateFrom', ''),
        ('dateTo', ''),
        ('opponentTeamId', '0'),
        ('vsConference', ''),
        ('vsDivision', ''),
        ('position', ''),
        ('playerPosition', ''),
        ('rookieYear', ''),
        ('gameSegment', ''),
        ('period', '0'),
        ('lastNGames', '0'),
        ('clutchTime', ''),
        ('aheadBehind', ''),
        ('pointDiff', ''),
        ('rangeType', '0'),
        ('startPeriod', '1'),
        ('endPeriod', '10'),
        ('startRange', '0'),
        ('endRange', '2147483647'),
        ('contextFilter', ''),
        ('contextMeasure', 'FGA'),
    )

    response = api_call('shotchartdetail', params=params)
    return response['Shot_Chart_Detail']


where_clause = "SEASON = '{}' and SEASON_TYPE = '{}'".format('2018-19', 'Regular Season')
players = mysql_client.read_table(table=player_box_score_traditional, where=where_clause)
players = players[['PLAYER_ID', 'TEAM_ID']].drop_duplicates()


# for p in players.index:
#     print(p)
#     player = players.loc[p, 'PLAYER_ID']
#     team = players.loc[p, 'TEAM_ID']
#     shots = get_shots(player, team)
#     print(shots)

def download_player_shots(p):
    print(p)
    player = p['PLAYER_ID']
    team = p['TEAM_ID']
    shots = get_shots(player, team)
    print(shots)
    return shots


cores = mp.cpu_count()
rows = players.to_dict('records')

with mp.Pool(processes=1) as pool:
    results = pool.map(download_player_shots, rows)
# for r in rows:
#     download_player_shots(r)

print('WAITING FOR GETS')
print(results)
