import sqlalchemy

from sqlalchemy import Column, Integer, VARCHAR, Float, Boolean, Text
from sqlalchemy import MetaData
from sqlalchemy import Table

meta = MetaData()
game_log_table = Table(
    'game_log',
    meta,
    Column('SEASON_ID', VARCHAR(255)),
    Column('TEAM_ID', VARCHAR(255), primary_key=True),
    Column('TEAM_ABBREVIATION', VARCHAR(255)),
    Column('TEAM_NAME', VARCHAR(255)),
    Column('GAME_ID', VARCHAR(255), primary_key=True),
    Column('GAME_DATE', VARCHAR(255)),
    Column('MATCHUP', VARCHAR(255)),
    Column('WL', VARCHAR(255)),
    Column('MIN', Float),
    Column('FGM', Float),
    Column('FGA', Float),
    Column('FG_PCT', Float),
    Column('FG3M', Float),
    Column('FG3A', Float),
    Column('FG3_PCT', Float),
    Column('FTM', Float),
    Column('FTA', Float),
    Column('FT_PCT', Float),
    Column('OREB', Float),
    Column('DREB', Float),
    Column('REB', Float),
    Column('AST', Float),
    Column('STL', Float),
    Column('BLK', Float),
    Column('TOV', Float),
    Column('PF', Float),
    Column('PTS', Float),
    Column('PLUS_MINUS', Float),
    Column('VIDEO_AVAILABLE', Integer),
    Column('SEASON', VARCHAR(255)),
    Column('SEASON_TYPE', VARCHAR(255)))

team_box_score_traditional = Table(
    'team_box_score_traditional',
    meta,
    Column('GAME_ID', VARCHAR(255), primary_key=True),
    Column('TEAM_ID', VARCHAR(255), primary_key=True),
    Column('TEAM_NAME', VARCHAR(255)),
    Column('TEAM_ABBREVIATION', VARCHAR(255)),
    Column('TEAM_CITY', VARCHAR(255)),
    Column('MIN', Text),
    Column('FGM', Float),
    Column('FGA', Float),
    Column('FG_PCT', Float),
    Column('FG3M', Float),
    Column('FG3A', Float),
    Column('FG3_PCT', Float),
    Column('FTM', Float),
    Column('FTA', Float),
    Column('FT_PCT', Float),
    Column('OREB', Float),
    Column('DREB', Float),
    Column('REB', Float),
    Column('AST', Float),
    Column('STL', Float),
    Column('BLK', Float),
    Column('TOV', Float),
    Column('PF', Float),
    Column('PTS', Float),
    Column('PLUS_MINUS', Float),
    Column('SEASON', VARCHAR(255)),
    Column('SEASON_TYPE', VARCHAR(255)))

player_box_score_traditional = Table(
    'player_box_score_traditional',
    meta,
    Column('GAME_ID', VARCHAR(255), primary_key=True),
    Column('TEAM_ID', VARCHAR(255)),
    Column('TEAM_ABBREVIATION', VARCHAR(255)),
    Column('TEAM_CITY', VARCHAR(255)),
    Column('PLAYER_ID', VARCHAR(255), primary_key=True),
    Column('PLAYER_NAME', VARCHAR(255)),
    Column('START_POSITION', VARCHAR(255)),
    Column('COMMENT', Text),
    Column('MIN', Text),
    Column('FGM', Float),
    Column('FGA', Float),
    Column('FG_PCT', Float),
    Column('FG3M', Float),
    Column('FG3A', Float),
    Column('FG3_PCT', Float),
    Column('FTM', Float),
    Column('FTA', Float),
    Column('FT_PCT', Float),
    Column('OREB', Float),
    Column('DREB', Float),
    Column('REB', Float),
    Column('AST', Float),
    Column('STL', Float),
    Column('BLK', Float),
    Column('TOV', Float),
    Column('PF', Float),
    Column('PTS', Float),
    Column('PLUS_MINUS', Float),
    Column('SEASON', VARCHAR(255)),
    Column('SEASON_TYPE', VARCHAR(255))
)

player_season_totals_traditional = Table(
    'player_season_totals_traditional',
    meta,
    Column('PLAYER_ID', VARCHAR(255), primary_key=True),
    Column('PLAYER_NAME', VARCHAR(255)),
    Column('TEAM_ID', VARCHAR(255)),
    Column('TEAM_ABBREVIATION', VARCHAR(255)),
    Column('AGE', Float),
    Column('GP', Float),
    Column('W', Float),
    Column('L', Float),
    Column('W_PCT', Float),
    Column('MIN', Float),
    Column('FGM', Float),
    Column('FGA', Float),
    Column('FG_PCT', Float),
    Column('FG3M', Float),
    Column('FG3A', Float),
    Column('FG3_PCT', Float),
    Column('FTM', Float),
    Column('FTA', Float),
    Column('FT_PCT', Float),
    Column('OREB', Float),
    Column('DREB', Float),
    Column('REB', Float),
    Column('AST', Float),
    Column('TOV', Float),
    Column('STL', Float),
    Column('BLK', Float),
    Column('BLKA', Float),
    Column('PF', Float),
    Column('PFD', Float),
    Column('PTS', Float),
    Column('PLUS_MINUS', Float),
    Column('NBA_FANTASY_PTS', Float),
    Column('DD2', Float),
    Column('TD3', Float),
    Column('SEASON', VARCHAR(255), primary_key=True),
    Column('SEASON_TYPE', VARCHAR(255), primary_key=True)
)

player_season_totals_advanced = Table(
    'player_season_totals_advanced',
    meta,
    Column('PLAYER_ID', VARCHAR(255), primary_key=True),
    Column('PLAYER_NAME', VARCHAR(255)),
    Column('TEAM_ID', VARCHAR(255)),
    Column('TEAM_ABBREVIATION', VARCHAR(255)),
    Column('AGE', Float),
    Column('GP', Float),
    Column('W', Float),
    Column('L', Float),
    Column('W_PCT', Float),
    Column('MIN', Float),
    Column('OFF_RATING', Float),
    Column('DEF_RATING', Float),
    Column('NET_RATING', Float),
    Column('AST_PCT', Float),
    Column('AST_TO', Float),
    Column('AST_RATIO', Float),
    Column('OREB_PCT', Float),
    Column('DREB_PCT', Float),
    Column('REB_PCT', Float),
    Column('TM_TOV_PCT', Float),
    Column('EFG_PCT', Float),
    Column('TS_PCT', Float),
    Column('USG_PCT', Float),
    Column('PACE', Float),
    Column('PACE_PER40', Float),
    Column('PIE', Float),
    Column('POSS', Float),
    Column('FGM', Float),
    Column('FGA', Float),
    Column('FGM_PG', Float),
    Column('FGA_PG', Float),
    Column('FG_PCT', Float),
    Column('SEASON', VARCHAR(255), primary_key=True),
    Column('SEASON_TYPE', VARCHAR(255), primary_key=True)

)