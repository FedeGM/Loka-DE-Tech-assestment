from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database_connection_model import SQLconnection as SQL
from config import config_data

# Creating the engine to MySQL database on AWS: loka-db-tech-assestment.XXXXXXXXXXXXXX.rds.amazonaws.com

aws_mysql = SQL(server= config_data['SERVER'],
                database= config_data['DATABASE'],
                user= config_data['USERNAME'],
                password= config_data['PASSWORD'],
                port= config_data['PORT'])

engine = create_engine(aws_mysql.conn_str, echo= True)
db = scoped_session(sessionmaker(autocommit = False,
                                 autoflush = False,
                                 bind = engine))

Base = declarative_base()
Base.query = db.query_property()

