import time

from .client.smart import SeasonType

SLEEP_TIME = 0.01


def add_field(df, name, value):
    df[name] = value
    return df


def add_season(df, season):
    return add_field(df, 'SEASON', season)


def add_season_type(df, season_type):
    return add_field(df, 'SEASON_TYPE', season_type)


def add_season_and_type(df, season, season_type):
    return add_season_type(add_season(df, season), season_type)


def api_rate_limit():
    time.sleep(SLEEP_TIME)


def extract_season_from_game_id(game_id):
    season_start = int(game_id[3:5])
    season_end = season_start + 1
    return '20{}-{}'.format(season_start, season_end)


def extract_season_type_from_game_id(gameid):
    season_type_ind = gameid[2]
    if season_type_ind == '1':
        return SeasonType.Preseason
    elif season_type_ind == '2':
        return SeasonType.RegularSeason
    elif season_type_ind == '4':
        return SeasonType.Playoffs
