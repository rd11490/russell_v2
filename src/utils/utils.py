import time

SLEEP_TIME = 1.25


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
