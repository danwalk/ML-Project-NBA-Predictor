import os, sys
import pandas as pd
import json
from sqlalchemy import create_engine
import pymysql
from getpass import getpass
from mysql.connector import connect, Error
import numpy as np

dir = os.path.dirname
SEP = os.sep
src = dir(dir(os.path.abspath(__file__)))
sys.path.append(src)
project_path = dir(dir(dir(os.path.abspath(__file__))))
sys.path.append(project_path)

from utils.folders_tb import read_json_to_dict
from utils.mysql_driver import MySQL
from utils.dashboard_tb import modelshort


def createengine():
    SEP = os.sep
    dir = os.path.dirname
    projectpath = dir(dir(dir(os.path.abspath(__file__))))
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
    dir = os.path.dirname
    projectpath = dir(dir(dir(os.path.abspath(__file__))))
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

def getpredictiontablefromsql(sortedresults=False):
    engine = createengine()
    df = pd.read_sql('SELECT * FROM prediction', con=engine)
    if sortedresults == True:
        df = modelshort(df)
    return df

def getfullnbatablefromsql():
    engine = createengine()
    df = pd.read_sql('SELECT * FROM daniel_walker', con=engine)
    return df
