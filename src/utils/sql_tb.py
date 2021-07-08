import os, sys
import pandas as pd
import json
from sqlalchemy import create_engine
import pymysql
from getpass import getpass
from mysql.connector import connect, Error
import numpy as np
from .folders_tb import read_json_to_dict
from .mysql_driver import MySQL

def createengine():
    SEP = os.sep
    projectpath = os.path.dirname(os.getcwd())
    json_fullpath = projectpath + SEP + "src" + SEP + "utils" + SEP + "sql_server_settings.json"
    json_readed = read_json_to_dict(json_fullpath)
    IP_DNS = json_readed["IP_DNS"]
    USER = json_readed["USER"]
    PASSWORD = json_readed["PASSWORD"]
    BD_NAME = json_readed["BD_NAME"]
    PORT = json_readed["PORT"]
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{IP_DNS}:{PORT}/{BD_NAME}')
    return engine

def nbacleantomysql(csvname):
    SEP = os.sep
    projectpath = os.path.dirname(os.getcwd())
    csv_fullpath = projectpath + SEP + "data" + SEP + csvname
    engine = createengine()
    NBA = pd.read_csv(csv_fullpath, index_col=None)
    jsonname = str(csvname[:-3]) + "json"
    json_fullpath = projectpath + SEP + "data" + SEP + jsonname
    nbatojson = NBA.to_json(orient="split")
    with open(json_fullpath, 'w') as fp:
        json.dump(nbatojson, fp, indent=4)
    NBA['Date'] = pd.to_datetime(NBA['Date'])
    NBA.to_sql('daniel_walker', con = engine, index=False, if_exists='replace')
    print(f'{csvname} appended to daniel_walker table in database')
    return "Done"

def modelresultstosql(modelresults):
    engine = createengine()
    modelresults.to_sql('prediction', con = engine, index=False, if_exists='replace')
    print(f'Model result appended to prediction table in database')
    return "Done"

def getpredictiontablefromsql():
    engine = createengine()
    df = pd.read_sql('SELECT * FROM prediction', con=engine)
    return df

def getfullnbatablefromsql():
    engine = createengine()
    df = pd.read_sql('SELECT * FROM daniel_walker', con=engine)
    return df