import datetime
import random
from time import sleep

import pandas as pd
import requests
import sys

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


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


class PerMode:
    Totals = 'Totals'
    PerGame = 'PerGame'
    Per100 = 'Per100Possessions'
    Per36 = 'Per36'
    Default = Totals


class SeasonType:
    RegularSeason = 'Regular Season'
    Playoffs = 'Playoffs'
    Preseason = 'Pre Season'
    Default = RegularSeason


class MeasureType:
    Base = 'Base'
    Advanced = 'Advanced'
    Misc = 'Misc'
    Scoring = 'Scoring'
    Usage = 'Usage'
    Defense = 'Defense'
    FourFactors = 'Four Factors'
    Default = Base


class PtMeasureType:
    Drives = 'Drives'
    Defense = 'Defense'
    CatchAndShoot = 'CatchShoot'
    Passing = 'Passing'
    Touches = 'Possessions'
    PullUp = 'PullUpShot'
    Rebounding = 'Rebounding'
    Efficiency = 'Efficiency'
    SpeedDistance = 'SpeedDistance'
    ElbowTouches = 'ElbowTouch'
    PostTouches = 'PostTouch'
    PaintTouches = 'PaintTouch'


headers = {
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
        self.default_season = self.__current_season()
        self.default_season_type = 'Regular Season'

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

    def team_season_totals(self, per_mode=PerMode.Default, season=None, season_type=SeasonType.Default,
                           measure_type=MeasureType.Default):
        if season is None:
            season = self.default_season
        params = (
            ('Conference', ''),
            ('DateFrom', ''),
            ('DateTo', ''),
            ('Division', ''),
            ('GameScope', ''),
            ('GameSegment', ''),
            ('LastNGames', '0'),
            ('LeagueID', '00'),
            ('Location', ''),
            ('MeasureType', measure_type),
            ('Month', '0'),
            ('OpponentTeamID', '0'),
            ('Outcome', ''),
            ('PORound', '0'),
            ('PaceAdjust', 'N'),
            ('PerMode', per_mode),
            ('Period', '0'),
            ('PlayerExperience', ''),
            ('PlayerPosition', ''),
            ('PlusMinus', 'N'),
            ('Rank', 'N'),
            ('Season', season),
            ('SeasonSegment', ''),
            ('SeasonType', season_type),
            ('ShotClockRange', ''),
            ('StarterBench', ''),
            ('TeamID', '0'),
            ('TwoWay', '0'),
            ('VsConference', ''),
            ('VsDivision', ''),
        )

        return self.api_call('leaguedashteamstats', params=params)

    def player_season_totals(self, per_mode=PerMode.Default, season=None, season_type=SeasonType.Default,
                             measure_type=MeasureType.Default):
        if season is None:
            season = self.default_season

        params = (
            ('College', ''),
            ('Conference', ''),
            ('Country', ''),
            ('DateFrom', ''),
            ('DateTo', ''),
            ('Division', ''),
            ('DraftPick', ''),
            ('DraftYear', ''),
            ('GameScope', ''),
            ('GameSegment', ''),
            ('Height', ''),
            ('LastNGames', '0'),
            ('LeagueID', '00'),
            ('Location', ''),
            ('MeasureType', measure_type),
            ('Month', '0'),
            ('OpponentTeamID', '0'),
            ('Outcome', ''),
            ('PORound', '0'),
            ('PaceAdjust', 'N'),
            ('PerMode', per_mode),
            ('Period', '0'),
            ('PlayerExperience', ''),
            ('PlayerPosition', ''),
            ('PlusMinus', 'N'),
            ('Rank', 'N'),
            ('Season', season),
            ('SeasonSegment', ''),
            ('SeasonType', season_type),
            ('ShotClockRange', ''),
            ('StarterBench', ''),
            ('TeamID', '0'),
            ('TwoWay', '0'),
            ('VsConference', ''),
            ('VsDivision', ''),
            ('Weight', '')
        )

        return self.api_call('leaguedashplayerstats', params=params)['LeagueDashPlayerStats']

    def player_season_tracking(self, season=None, season_type=SeasonType.Default, pt_measure_type=None,
                               per_mode=PerMode.Default):
        return self.season_tracking_stats(season=season, season_type=season_type, pt_measure_type=pt_measure_type,
                                          per_mode=per_mode, player_or_team='Player')

    def team_season_tracking(self, season=None, season_type=SeasonType.Default, pt_measure_type=None,
                             per_mode=PerMode.Default):
        return self.season_tracking_stats(season=season, season_type=season_type, pt_measure_type=pt_measure_type,
                                          per_mode=per_mode, player_or_team='Team')

    def season_tracking_stats(self, season=None, season_type=SeasonType.Default, pt_measure_type=None,
                              per_mode=PerMode.Default, player_or_team=None):
        if season is None:
            season = self.default_season
        if pt_measure_type is None:
            raise ValueError("Must provide a MeasureType")
        if player_or_team is None:
            raise ValueError("Must provide either Player or Team")

        params = (
            ('College', ''),
            ('Conference', ''),
            ('Country', ''),
            ('DateFrom', ''),
            ('DateTo', ''),
            ('Division', ''),
            ('DraftPick', ''),
            ('DraftYear', ''),
            ('GameScope', ''),
            ('Height', ''),
            ('LastNGames', '0'),
            ('LeagueID', '00'),
            ('Location', ''),
            ('Month', '0'),
            ('OpponentTeamID', '0'),
            ('Outcome', ''),
            ('PORound', '0'),
            ('PerMode', per_mode),
            ('PlayerExperience', ''),
            ('PlayerOrTeam', player_or_team),
            ('PlayerPosition', ''),
            ('PtMeasureType', pt_measure_type),
            ('Season', season),
            ('SeasonSegment', ''),
            ('SeasonType', season_type),
            ('StarterBench', ''),
            ('TeamID', '0'),
            ('VsConference', ''),
            ('VsDivision', ''),
            ('Weight', ''),
        )

        return self.api_call('leaguedashptstats', params=params)['LeagueDashPtStats']

    def shooting_dashboard(self, season=None, season_type=None, player_id=None, per_mode=PerMode.Default):

        if season is None:
            season = self.default_season
        if season_type is None:
            season_type = self.default_season_type
        if player_id is None:
            raise ValueError("Must Provide a Player Id")

        params = (
            ('DateFrom', ''),
            ('DateTo', ''),
            ('GameSegment', ''),
            ('LastNGames', '0'),
            ('LeagueID', '00'),
            ('Location', ''),
            ('Month', '0'),
            ('OpponentTeamID', '0'),
            ('Outcome', ''),
            ('PerMode', per_mode),
            ('Period', '0'),
            ('PlayerID', player_id),
            ('Season', season),
            ('SeasonSegment', ''),
            ('SeasonType', season_type),
            ('TeamID', '0'),
            ('VsConference', ''),
            ('VsDivision', ''),
        )
        return self.api_call('playerdashptshots', params=params)

    def box_score_traditional(self, game_id=None, start_period=None, end_period=None, start_range=None,
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

    def box_score_advanced(self, game_id=None, start_period=None, end_period=None, start_range=None,
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
            ('EndPeriod', end_period),
            ('EndRange', end_range),
            ('GameID', game_id),
            ('RangeType', range_type),
            ('StartPeriod', start_period),
            ('StartRange', start_range)
        )

        return self.api_call('boxscoreadvancedv2', params=params)

    def get_season_traditional_box_score(self, season=None, season_type=None):
        return self.__get_season_box_scores(season, season_type, MeasureType.Base)

    def get_season_advanced_box_score(self, season=None, season_type=None):
        return self.__get_season_box_scores(season, season_type, MeasureType.Advanced)

    def __get_season_box_scores(self, season=None, season_type=None, measure_type=None):
        params = (
            ('DateFrom', ''),
            ('DateTo', ''),
            ('GameSegment', ''),
            ('LastNGames', '0'),
            ('LeagueID', '00'),
            ('Location', ''),
            ('MeasureType', measure_type),
            ('Month', '0'),
            ('OpponentTeamID', '0'),
            ('Outcome', ''),
            ('PORound', '0'),
            ('PaceAdjust', 'N'),
            ('PerMode', 'Totals'),
            ('Period', '0'),
            ('PlusMinus', 'N'),
            ('Rank', 'N'),
            ('Season', season),
            ('SeasonSegment', ''),
            ('SeasonType', season_type),
            ('ShotClockRange', ''),
            ('VsConference', ''),
            ('VsDivision', ''),
        )

        return self.api_call('playergamelogs', params=params)['PlayerGameLogs']

    def win_probability(self, game_id=None):
        if game_id is None:
            raise ValueError("Must provide a Game Id")
        params = {
            ('GameID', game_id),
            ('RunType', 'each second')
        }
        return self.api_call('winprobabilitypbp', params=params)

    def get_player_game_log(self, season_type=SeasonType.Default, season=None, league_id=None, date_to=None,
                            date_from=None, measure_type=None):
        return self.__get_league_game_log(player_or_team='P', season_type=season_type, season=season,
                                          league_id=league_id, date_to=date_to, date_from=date_from, measure_type=measure_type)

    def get_teams_game_log(self, season_type=SeasonType.Default, season=None, league_id=None, date_to=None,
                           date_from=None, measure_type=None):
        return self.__get_league_game_log(player_or_team='T', season_type=season_type, season=season,
                                          league_id=league_id, date_to=date_to, date_from=date_from, measure_type=measure_type)

    def play_by_play(self, game_id=None, start_period=None, end_period=None):
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

        return self.api_call('playbyplayv2', params=params)['PlayByPlay']

    def __get_league_game_log(self, player_or_team=None, season_type=SeasonType.Default, season=None, league_id=None,
                              date_to=None,
                              date_from=None, measure_type=None):
        if player_or_team is None:
            raise ValueError("Must provide a Team Id")
        if season is None:
            season = self.default_season
        if league_id is None:
            league_id = self.default_league
        if date_to is None:
            date_to = ''
        if date_from is None:
            date_from = ''
        if measure_type is None:
            measure_type = MeasureType.Base

        params = (
            ('DateFrom', date_from),
            ('DateTo', date_to),
            ('LeagueID', league_id),
            ('Season', season),
            ('SeasonType', season_type),
            ('playerOrTeam', player_or_team),
            ('sorter', 'DATE'),
            ('direction', 'ASC'),
            ('MeasureType', measure_type),

        )

        resp = self.api_call('leaguegamelog', params)
        return resp['LeagueGameLog']

    def get_defensive_matchups(self, season=None, season_type=None):
        if season is None:
            season = self.default_season
        if season_type is None:
            season_type = self.default_season

        params = (
            ('DateFrom', ''),
            ('DateTo', ''),
            ('DefPlayerID', ''),
            ('OffPlayerID', ''),
            ('LeagueID', '00'),
            ('Outcome', ''),
            ('PORound', '0'),
            ('PerMode', 'Totals'),
            ('Season', season),
            ('SeasonType', season_type),
        )

        response = self.api_call('leagueseasonmatchups', params=params, timeout=45)
        return response['SeasonMatchups']

    def get_shot_chart_detail(self, player_id=None, team_id=None, game_id=None, season=None, season_type=None,
                              league_id=None):
        return self.get_shot_chart_detail_data(player_id=player_id, team_id=team_id, game_id=game_id, season=season,
                                               season_type=season_type,
                                               league_id=league_id, context='FGA')

    def get_foul_chart_detail(self, player_id=None, team_id=None, game_id=None, season=None, season_type=None,
                              league_id=None):
        return self.get_shot_chart_detail_data(player_id=player_id, team_id=team_id, game_id=game_id, season=season,
                                               season_type=season_type,
                                               league_id=league_id, context='PF')

    def get_shot_chart_detail_data(self, player_id=None, team_id=None, game_id=None, season=None, season_type=None,
                                   league_id=None, context=None):

        if player_id is None:
            raise ValueError("Must provide a Team Id")
        if team_id is None:
            raise ValueError("Must provide a Team Id")
        if context is None:
            raise ValueError("Must provide a Team Id")
        if season is None:
            season = self.default_season
        if season_type is None:
            season_type = self.default_season
        if league_id is None:
            league_id = self.default_league
        if game_id is None:
            game_id = ''

        params = (
            ('leagueId', league_id),
            ('season', season),
            ('seasonType', season_type),
            ('teamId', team_id),
            ('playerId', player_id),
            ('gameID', game_id),
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
            ('contextMeasure', context),
        )

        response = self.api_call('shotchartdetail', params=params)
        return response['Shot_Chart_Detail']

    def api_call(self, endpoint, params, headers=None, timeout=10, retries=10):
        return self.api_call_with_retry(endpoint, params, headers, timeout, retries)

    def api_call_with_retry(self, endpoint, params, headers=None, timeout=10, retries_left=10):
        print('Calling: "{}{} - {}" -- retries remaining: {}'.format(self.base_url, endpoint, params, retries_left))
        if retries_left > 0:
            try:
                if headers is None:
                    headers = self.headers
                resp = requests.get("{}{}".format(self.base_url, endpoint), params=params, headers=headers,
                                    timeout=timeout)
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
                return results
            except:
                print("Unexpected error:", sys.exc_info()[0])
                return self.api_call_with_retry(endpoint, params, headers, retries_left - 1)
        else:
            raise Exception('Number of retries exceeded')


smart = Smart()
