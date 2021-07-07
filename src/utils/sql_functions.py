import streamlit as st
from PIL import Image
import os, sys
import pandas as pd
import json
import pymysql
from sqlalchemy import create_engine
import pymysql
from getpass import getpass
from mysql.connector import connect, Error
import numpy as np
from .folders_tb import read_json_to_dict
from .mysql_driver import MySQL


'''
dir = os.path.dirname
sep = os.sep
src_path = dir(dir(os.path.abspath(__file__)))
sys.path.append(src_path)
totum_revol_path = dir(dir(dir(os.path.abspath(__file__))))
sys.path.append(totum_revol_path)


configbd_json_path = totum_revol_path + sep + 'config' + sep + 'bd_info.json'
with open(configbd_json_path, "r") as configbd_json_readed:
    json_configbd = json.load(configbd_json_readed)
IP_DNS = json_configbd["IP_DNS"]
USER = json_configbd["USER"]
PASSWORD = json_configbd["PASSWORD"]
BD_NAME = json_configbd["BD_NAME"]
PORT = json_configbd["PORT"]

mysql_db = MySQL(IP_DNS=IP_DNS, USER=USER, PASSWORD=PASSWORD, BD_NAME=BD_NAME, PORT=PORT)
conn = mysql_db.connect()

select_sql = """SELECT * FROM australia_fires.fire_archive_M6_96619"""
select_result = mysql_db.execute_get_sql(sql=select_sql)

df = pd.read_sql('SELECT * FROM australia_fires.fire_archive_M6_96619', con=conn)
'''

def nbacleantomysql(csvname):
    SEP = os.sep
    dir = os.path.dirname
    csv_fullpath = dir(os.getcwd()) + SEP + "data" + SEP + csvname
    json_fullpath = (os.getcwd()) + SEP + "utils" + SEP + "sql_server_settings.json"
    json_readed = read_json_to_dict(json_fullpath)
    IP_DNS = json_readed["IP_DNS"]
    USER = json_readed["USER"]
    PASSWORD = json_readed["PASSWORD"]
    BD_NAME = json_readed["BD_NAME"]
    PORT = json_readed["PORT"]
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{IP_DNS}:{PORT}/{BD_NAME}')
    NBA = pd.read_csv(csv_fullpath, index_col=None)
    NBA['Date'] = pd.to_datetime(NBA['Date'])
    NBA.to_sql('daniel_walker', con = engine, index=False, if_exists='replace')
    return f'{csvname} appended to daniel_walker table in {BD_NAME}'

def modelresultstosql(modelresults):
    SEP = os.sep
    dir = os.path.dirname
    csv_fullpath = dir(os.getcwd()) + SEP + "data" + SEP + csvname
    json_fullpath = (os.getcwd()) + SEP + "utils" + SEP + "sql_server_settings.json"
    json_readed = read_json_to_dict(json_fullpath)
    IP_DNS = json_readed["IP_DNS"]
    USER = json_readed["USER"]
    PASSWORD = json_readed["PASSWORD"]
    BD_NAME = json_readed["BD_NAME"]
    PORT = json_readed["PORT"]
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{IP_DNS}:{PORT}/{BD_NAME}')
    #modelresults = pd.read_csv(csv_fullpath, index_col=None)
    modelresults.to_sql('prediction', con = engine, index=False, if_exists='replace')
    return f'Model result appended to prediction table in {BD_NAME}'