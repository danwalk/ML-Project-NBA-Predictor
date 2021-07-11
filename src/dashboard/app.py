import streamlit as st
from PIL import Image
import os, sys
import pandas as pd
import json


dir = os.path.dirname
SEP = os.sep
src = dir(dir(os.path.abspath(__file__)))
sys.path.append(src)
project_path = dir(dir(dir(os.path.abspath(__file__))))
sys.path.append(project_path)

from src.utils.dataframes import shortversionofresults
from src.utils.models import gamepredictor
from src.utils.models import runfullseasonpredictor
from src.utils.sql_tb import getpredictiontablefromsql

from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
from threading import current_thread
from contextlib import contextmanager
from io import StringIO
import sys


@contextmanager
def st_redirect(src, dst):
    placeholder = st.empty()
    output_func = getattr(placeholder, dst)

    with StringIO() as buffer:
        old_write = src.write

        def new_write(b):
            if getattr(current_thread(), REPORT_CONTEXT_ATTR_NAME, None):
                buffer.write(b + '')
                output_func(buffer.getvalue() + '')
            else:
                old_write(b)

        try:
            src.write = new_write
            yield
        finally:
            src.write = old_write


@contextmanager
def st_stdout(dst):
    "this will show the prints"
    with st_redirect(sys.stdout, dst):
        yield


@contextmanager
def st_stderr(dst):
    "This will show the logging"
    with st_redirect(sys.stderr, dst):
        yield


menu = st.sidebar.selectbox('Menu:',
            options=["Welcome", "Visualization", "Json API-Flask", "Model Prediction", "Feature Heatmap", "All Team Season Generator", "Models From SQL Database"])

if menu == "Welcome":

    config_json_path = project_path + SEP + "src" + SEP + "utils" + SEP + 'config.json'

    with open(config_json_path, "r") as config_json_readed:
        json_config = json.load(config_json_readed)

    st.header(json_config['Title'])
    st.subheader(json_config['Description'])
    st.write("Win, Lose or Draw, this is entertainment, with numbers and statistics!")
    st.write("Project created by Daniel Jonathan Walker")
    st.write("https://github.com/danwalk/ML-Project-NBA-Predictor")
    st.write("https://www.linkedin.com/in/daniel-jonathan-walker-2a5a461b5")
    image1 = project_path + SEP + 'data' + SEP + 'img' + SEP + 'NBA logo.jpg'
    image = Image.open(image1)
    st.image (image, use_column_width=False)
    st.write("Bookies stats, results and original predictions collected from:")
    st.write("https://masseyratings.com/nba/games")
    image2 = project_path + SEP + 'data' + SEP + 'img' + SEP + 'Massey Rating logo.jpg'
    image2 = Image.open(image2)
    st.image (image2,use_column_width=False)
    st.write("https://www.oddsportal.com/")
    image3 = project_path + SEP + 'data' + SEP + 'img' + SEP + 'OddsPortal logo.jpg'
    image3 = Image.open(image3)
    st.image (image3,use_column_width=False)
    
if menu == "Visualization":
    teamlist = ["Select", "All Teams", "Atlanta Hawks", "Charlotte Hornets", "Denver Nuggets", "Golden State Warriors", "Indiana Pacers",
        "Los Angeles Lakers", "Miami Heat","Milwaukee Bucks", "Phoenix Suns", "Utah Jazz"]
    reglist = ["Select", "BayesianRidge", "DecisionTreeRegressor", "GaussianProcessRegressor", "GradientBoostingRegressor",
    "KNeighborsRegressor", "LinearRegression", "RadiusNeighborsRegressor", "RandomForestRegressor", "RidgeCV", "SVR"]
    team = st.selectbox('Select', teamlist)
    regressor = st.selectbox('Select', reglist)
    imagepath = project_path + SEP + 'resources' + SEP + team + "_" + regressor + ".jpg"
    image2path = project_path + SEP + 'resources' + SEP + team + "_betdonut_" + regressor + ".jpg"
    if team != "Select" and regressor != "Select":
        image = Image.open(imagepath)
        st.image (image,use_column_width=False)
        image2 = Image.open(image2path)
        st.image (image2,use_column_width=False)
        if team == "All Teams":
            teamcsv = project_path + SEP + 'data' + SEP + team + "_" + regressor + "_.csv"
            teamcsv1 = pd.read_csv(teamcsv)
            shortdf = shortversionofresults(teamcsv1)
            st.table(shortdf)

if menu == "Model Prediction":
    teamlist = ["Select", "Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers",
        "Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers",
        "Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves",
        "New Orleans Pelicans","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns",
        "Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"]
    reglist = ["Select", "BayesianRidge", "DecisionTreeRegressor", "GaussianProcessRegressor", "GradientBoostingRegressor",
        "KNeighborsRegressor", "LinearRegression", "RadiusNeighborsRegressor", "RandomForestRegressor", "RidgeCV", "SVR"]
    team = st.selectbox('Choose Team', teamlist)
    regressor = st.selectbox('Choose Regressor', reglist)
    if regressor == "DecisionTreeRegressor":
        eon = st.selectbox('Choose Criterion', ["mse", "mae", "poisson", "friedman_mse"])
    elif regressor == "RandomForestRegressor":
        eon = st.slider("Select Estimators", min_value=50, max_value=200)
    elif regressor == "KNeighborsRegressor":
        eon = st.slider("Select Neighbors", min_value=3, max_value=8)
    elif regressor == "SVR":
        eon = st.slider("Select epsilon", min_value=0.1, max_value=0.25)
    else:
        eon = 5
    Gamenumber = st.slider(f'Select {team} game to predict with {regressor}', min_value=10, max_value=72)
    if st.button(f'Click to see predictions for {team} in game {Gamenumber} using {regressor} regressor'):
        if __name__ == '__main__':
            with st_stdout("success"), st_stderr("code"):
                gamepredictor(team, Gamenumber, regressor, eon)

if menu == "Json API-Flask":
    st.title('Starting Dataset')
    if st.checkbox('Click to GET json from flask ---- which receives from mysql!!!'):
        dataframe_nba = pd.read_json('http://127.0.0.1:6060/nbadata?token_id=X9808164K')
        st.table(dataframe_nba)


if menu == "Models From SQL Database":
    st.title("Overall Model Results")
    x = getpredictiontablefromsql()
    if st.checkbox('Click to convert table to Bar Graph'):
        image3 = project_path + SEP + 'resources' + SEP + 'ModelBarGraph.jpg'
        image3 = Image.open(image3)
        st.image (image3,use_column_width=False)
    if st.checkbox('Click to sort by highest Bet Return %'):
        x = getpredictiontablefromsql(True)
        st.table(x)
    else:
        st.table(x)
    


if menu == "All Team Season Generator":
    reglist = ["Select", "BayesianRidge", "DecisionTreeRegressor", "GaussianProcessRegressor", "GradientBoostingRegressor",
        "KNeighborsRegressor", "LinearRegression", "RadiusNeighborsRegressor", "RandomForestRegressor", "RidgeCV", "SVR"]
    regressor = st.selectbox('Choose Regressor', reglist)
    if regressor == "DecisionTreeRegressor":
        eon = st.selectbox('Choose Criterion', ["mse", "mae", "poisson", "friedman_mse"])
    elif regressor == "RandomForestRegressor":
        eon = st.slider("Select Estimators", min_value=10, max_value=200)
    elif regressor == "KNeighborsRegressor":
        eon = st.slider("Select Neighbors", min_value=3, max_value=8)
    elif regressor == "SVR":
        eon = st.slider("Select epsilon", min_value=0.1, max_value=0.25)
    else:
        eon = 5
    reg = [regressor]
    if st.button(f'Click to simulate the full season using {regressor} regressor'):
        if __name__ == '__main__':
            with st_stdout("success"):
                runfullseasonpredictor(reg, eon, returnsummary=False, fromstreamlit=True)
                imagepath = project_path + SEP + 'resources' + SEP + "All Teams" + "_" + regressor + ".jpg"
                image = Image.open(imagepath)
                st.image (image,use_column_width=False)

if menu == "Feature Heatmap":
    st.header("Feature Heatmap Of The Columns Used To Fit Prediction Models")
    st.subheader("This is the heatmap of one of the predictions made. Depending on the team, their form, the teams form that they have played, the team they are playing, the correlation between columns will change.")
    if st.checkbox('Click to see Heatmap'):
        image = project_path + SEP + 'data' + SEP + "img" + SEP + 'PredictionHeatMap.jpg'
        image = Image.open(image)
        st.image (image,use_column_width=False)
