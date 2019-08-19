import sqlalchemy

from sqlalchemy import Column, Integer, VARCHAR, Float, Boolean, Text
from sqlalchemy import MetaData
from sqlalchemy import Table

meta = MetaData()
game_log_table = Table('game_log',
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

team_box_score_traditional = Table('team_box_score_traditional',
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

player_box_score_traditional = Table('player_box_score_traditional',
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
