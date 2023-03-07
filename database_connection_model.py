from urllib.parse import quote_plus
from config import config_data

class SQLconnection:
    def __init__(self, server, database, user, password, port) -> None:
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn_str = self.__get_connection_str()

    def __get_connection_str(self):
        # params = quote_plus(f'mysql+pymysql://{self.user}:{self.password}@{self.server}:{self.port}/{self.database}')
        conn_str = f'mysql+mysqlconnector://{self.user}:{self.password}@{self.server}:{self.port}/{self.database}'
        return conn_str



