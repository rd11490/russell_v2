import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
import json
import os
import pymysql
from .upsert import Upsert
from .nba import meta

class MySqlClient:
    def __init__(self):
        creds_file = open(os.path.join(os.path.dirname(__file__), './MySqlCred.json'), "r")
        self.__creds = json.loads(creds_file.read())
        self.__engine = self.__build_engine()
        self.create_tables()

    def __username(self):
        return self.__creds['Username']

    def __password(self):
        return self.__creds['Password']

    def __build_engine(self):
        # ssl_args = {'ssl_disabled': True}
        return create_engine(
            'mysql+pymysql://{0}:{1}@localhost:3306/nba_data'.format(self.__username(), self.__password()))

    def run_query(self, query):
        """
        Takes in a query string and outputs a pandas dataframe of the results
        :param query: String Query
        :return: Pandas dataframe
        """
        con = self.__engine.connect()
        df = pd.read_sql(query, con=con)
        return df

    def read_table(self, table, where=None):
        if where is not None:
            where = 'WHERE {}'.format(where)
        else:
            where = ''
        query = 'SELECT * FROM {} {}'.format(table.name, where)

        return self.run_query(query)

    def write(self, df, table):
        """
        Writes a dataframe to a table
        :param df: Dataframe to write
        :param table: SqlAlchemy Table object
        """
        on_duplicate_key_stmt = Upsert(table, df.to_dict('records'))
        self.__engine.execute(on_duplicate_key_stmt)

    def create_tables(self):
        meta.create_all(bind=self.__engine, checkfirst=True)

    def drop_table(self, table):
        self.__engine.execute('DROP TABLE IF EXISTS {}'.format(table.name))

    def truncate_table(self, table, where='1 = 1'):
        self.__engine.execute('DELETE FROM {0} WHERE {1}'.format(table.name, where))


mysql_client = MySqlClient()
