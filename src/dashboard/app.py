import streamlit as st
from PIL import Image
import os, sys
import pandas as pd
import json
#from utils.stream_config import draw_map
#from utils.dataframes import load_csv

# Haz que se pueda importar correctamente estas funciones que están en la carpeta utils/
dir = os.path.dirname
SEP = os.sep
src_path = dir(dir(os.path.abspath(__file__)))
sys.path.append(src_path)
project_path = dir(dir(dir(os.path.abspath(__file__))))
sys.path.append(project_path)


menu = st.sidebar.selectbox('Menu:',
            options=["Welcome", "Team Stats", "Game Predictor", "API"])

if menu == "Welcome":
    # Pon el título del proyecto que está en el archivo "config.json" en /config

    config_json_path = project_path + SEP + 'config' + SEP + 'config.json'

    with open(config_json_path, "r") as config_json_readed:
        json_config = json.load(config_json_readed)

    st.title(json_config['Title'])
    st.write(json_config['Description'])
    st.write("Win, Lose or Draw, this is entertainment, with numbers and statistics!")
    
if menu == "Team Stats":

    path_image_nba = project_path + SEP + 'data' + SEP + 'img' + SEP + 'nba background.jpg'
    image = Image.open(path_image_nba)
    st.image (image,use_column_width=True)

if menu == "Game Predictor":
    # El archivo que está en data/ con nombre 'red_recarga_acceso_publico_2021.csv'
    nbacsv = project_path + SEP + 'data' + SEP + 'nbaclean.csv'
    df_nba = pd.read_csv(nbacsv)
    st.dataframe(df_nba)

if menu == "API":
    # Accede al único endpoint de tu API flask y lo muestra por pantalla como tabla/dataframe
    st.title('Play Store')
    dataframe_playstore = pd.read_json('http://localhost:6060/playstore')
    st.table(dataframe_playstore)
    st.balloons()


if menu == "Australia Fire":
    """6"""
    st.title("Fire Table")
    

    # 1. Conecta a la BBDD
    # 2. Obtén, a partir de sentencias SQL (no pandas), la información de las tablas que empiezan por 'fire_archive*' (join)
    # 3. Entrena tres modelos de ML diferentes siendo el target la columna 'fire_type'. Utiliza un pipeline que preprocese los datos con PCA. Usa Gridsearch.  
    # 4. Añade una entrada en la tabla 'student_findings' por cada uno de los tres modelos. 'student_id' es EL-ID-DE-TU-GRUPO.
    # 5. Obtén la información de la tabla 'fire_nrt_M6_96619' y utiliza el mejor modelo para predecir la columna target de esos datos. 
    # 6. Usando SQL (no pandas) añade una columna nueva en la tabla 'fire_nrt_M6_96619' con el nombre 'fire_type_EL-ID-DE-TU-GRUPO'
    # 7. Muestra por pantalla en Streamlit la tabla completa (X e y)
    


