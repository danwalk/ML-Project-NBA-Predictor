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