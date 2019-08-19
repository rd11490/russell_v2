import datetime

import pandas as pd
import requests

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class Smart:
    def __init__(self):
        self.headers = {
            'Host': 'stats.nba.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'Referer': 'stats.nba.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
        self.default_league = '00'
        self.default_season_type = 'Regular Season'
        self.default_season = self.__current_season()
        self.base_url = 'https://stats.nba.com/stats/'

    def __current_season(self):
        now = datetime.datetime.now()
        if now.month > 8:
            last_year = datetime.datetime.now().year
            year = last_year + 1
            return str(last_year) + '-' + str(year)[2:]
        else:
            year = datetime.datetime.now().year
            last_year = year - 1
            return str(last_year) + '-' + str(year)[2:]

    def get_box_score_traditional(self, game_id=None, start_period=None, end_period=None, start_range=None,
                                  end_range=None, range_type=None):
        if game_id is None:
            raise ValueError("Must provide a Game Id")
        if start_period is None:
            start_period = 0
        if end_period is None:
            end_period = 14
        if start_range is None:
            start_range = 0
        if end_range is None:
            end_range = 2147483647
        if range_type is None:
            range_type = 0

        params = (
            ('gameId', game_id),
            ('startPeriod', start_period),
            ('endPeriod', end_period),
            ('startRange', start_range),
            ('endRange', end_range),
            ('rangeType', range_type)
        )

        return self.api_call('boxscoretraditionalv2', params=params)

    def get_player_game_log(self, season_type=None, season=None, league_id=None, date_to=None, date_from=None):
        return self.__get_league_game_log(player_or_team='P')

    def get_teams_game_log(self, season_type=None, season=None, league_id=None, date_to=None, date_from=None):
        return self.__get_league_game_log(player_or_team='T')

    def get_play_by_play(self, game_id=None, start_period=None, end_period=None):
        if game_id is None:
            raise ValueError("Must provide a Game Id")
        if start_period is None:
            start_period = 0
        if end_period is None:
            end_period = 14

        params = (
            ('gameId', game_id),
            ('startPeriod', start_period),
            ('endPeriod', end_period)
        )

        return self.api_call('playbyplayv2', params=params)

    def __get_league_game_log(self, player_or_team=None, season_type=None, season=None, league_id=None, date_to=None,
                              date_from=None):
        if player_or_team is None:
            raise ValueError("Must provide a Team Id")
        if season_type is None:
            season_type = self.default_season_type
        if season is None:
            season = self.default_season
        if league_id is None:
            league_id = self.default_league
        if date_to is None:
            date_to = ''
        if date_from is None:
            date_from = ''

        params = (
            ('DateFrom', date_from),
            ('DateTo', date_to),
            ('LeagueID', league_id),
            ('Season', season),
            ('SeasonType', season_type),
            ('playerOrTeam', player_or_team),
            ('sorter', 'DATE'),
            ('direction', 'ASC')
        )

        resp = self.api_call('leaguegamelog', params)
        return resp['LeagueGameLog']

    def get_team_game_log(self, team_id=None, season_type=None, season=None, league_id=None, date_to=None,
                          date_from=None):
        if team_id is None:
            raise ValueError("Must provide a Team Id")
        if season_type is None:
            season_type = self.default_season_type
        if season is None:
            season = self.default_season
        if league_id is None:
            league_id = self.default_league
        if date_to is None:
            date_to = ''
        if date_from is None:
            date_from = ''

        params = (
            ('DateFrom', date_from),
            ('DateTo', date_to),
            ('LeagueID', league_id),
            ('Season', season),
            ('SeasonType', season_type),
            ('TeamID', team_id)
        )

        resp = self.api_call('teamgamelog', params)
        return resp['TeamGameLog']

    def api_call(self, endpoint, params, headers=None):
        if headers is None:
            headers = self.headers

        resp = requests.get("{}{}".format(self.base_url, endpoint), params=params, headers=headers)

        if resp.status_code != 200:
            print(resp.request.path_url)
            print(resp.content)
            raise ValueError('{} returned with the status code: {}'.format(endpoint, resp.status_code))

        sets = resp.json()['resultSets']
        results = {}
        for s in sets:
            frame = pd.DataFrame(s['rowSet'])
            frame.columns = s['headers']
            results[s['name']] = frame
        return results


class NBATeams:
    AtlantaHawks = '1610612737'
    BostonCeltics = '1610612738'
    BrooklynNets = '1610612751'
    CharlotteHornets = '1610612766'
    ChicagoBulls = '1610612741'
    ClevelandCavaliers = '1610612739'
    DallasMavericks = '1610612742'
    DenverNuggets = '1610612743'
    DetroitPistons = '1610612765'
    GoldenStateWarriors = '1610612744'
    HoustonRockets = '1610612745'
    IndianaPacers = '1610612754'
    LosAngelesClippers = '1610612746'
    LosAngelesLakers = '1610612747'
    MemphisGrizzlies = '1610612763'
    MiamiHeat = '1610612748'
    MilwaukeeBucks = '1610612749'
    MinnesotaTimberwolves = '1610612750'
    NewOrleansPelicans = '1610612740'
    NewYorkKnicks = '1610612752'
    OklahomaCityThunder = '1610612760'
    OrlandoMagic = '1610612753'
    Philadelphia76ers = '1610612755'
    PhoenixSuns = '1610612756'
    PortlandTrailBlazers = '1610612757'
    SacramentoKings = '1610612758'
    SanAntonioSpurs = '1610612759'
    TorontoRaptors = '1610612761'
    UtahJazz = '1610612762'
    WashingtonWizards = '1610612764'


smart = Smart()
