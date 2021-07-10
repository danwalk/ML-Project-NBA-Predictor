import streamlit as st
import pandas as pd
import numpy as np
import os, sys

dir = os.path.dirname
SEP = os.sep
src = dir(dir(os.path.abspath(__file__)))
sys.path.append(src)
project_path = dir(dir(dir(os.path.abspath(__file__))))
sys.path.append(project_path)

from utils.folders_tb import openmodelresults
from utils.sql_tb import modelresultstosql
from utils.visualization_tb import linegraphfunc
from utils.visualization_tb import modelresultsbargraph
from utils.dashboard_tb import modelshort


def systempredictionmaker(bookies, systempred):
    if bookies > systempred:
        return "Under"
    else:
        return "Over"

def predictionmaker(bookies, last10gamesscoring, opponentlast10games, opponentform, systempred):
    if bookies < last10gamesscoring and bookies < opponentlast10games and bookies < systempred and opponentform > 5:
        return (f'Prediction is OVER {bookies}')
    if bookies > last10gamesscoring and bookies > opponentlast10games and bookies > systempred and opponentform < 5:
        return (f'Prediction is UNDER {bookies}')
    else:
        return "Not conclusive"

def appendresults(df):
        totgame = len(df)
        df = df.sort_values(by="Date")
        conditions = [(df["SystemResult"] == "Correct"),
                (df["SystemResult"] == "Incorrect")]
        values = [0.83, -1]
        df["BetReturn"] = np.select(conditions, values)
        df.drop(df[df['BookiePrediction'] == 0].index, inplace = True)
        Regressor = df["Regressor"].iloc[-1]
        EstimatorsorNeigbor = df["Estimatororneigbor"].iloc[-1]
        ContainsNotConclusivePred = df.isin(["Not conclusive"]).any().any()
        Totalgames = len(df)
        GamesRemovedPred0 = totgame - Totalgames
        TotalCorrect = df.loc[df["SystemResult"] == "Correct", "BetReturn"].count()
        Correct = "{:.2f}%".format((TotalCorrect / Totalgames)*100)
        BetReturn = df['BetReturn'].sum()
        BetProfit = "{:.2f}%".format((BetReturn/Totalgames)*100)
        TotalOversPred = df[df.ModelResultPrediction == "Over"].count()[-1]
        TotalOversCorrect = df[(df.ModelResultPrediction == "Over") & (df.SystemResult == "Correct")].count()[-1]
        OversCorrect = "{:.2f}%".format((TotalOversCorrect/TotalOversPred)*100)
        OversBetReturn = df[(df['ModelResultPrediction'] == "Over")]['BetReturn'].sum()
        OversProfit = "{:.2f}%".format((OversBetReturn/TotalOversPred)*100)
        TotalUndersPred = df[df.ModelResultPrediction == "Under"].count()[-1]
        TotalUndersCorrect = df[(df.ModelResultPrediction == "Under") & (df.SystemResult == "Correct")].count()[-1]
        UndersCorrect = "{:.2f}%".format((TotalUndersCorrect/TotalUndersPred)*100)
        UndersBetReturn = df[(df['ModelResultPrediction'] == "Under")]['BetReturn'].sum()
        UndersProfit = "{:.2f}%".format((UndersBetReturn/TotalUndersPred)*100)
        funcreturn = [Regressor, EstimatorsorNeigbor, ContainsNotConclusivePred, Totalgames, GamesRemovedPred0, TotalCorrect, Correct, BetReturn, BetProfit, TotalOversPred,
        TotalOversCorrect, OversCorrect, OversBetReturn, OversProfit, TotalUndersPred, TotalUndersCorrect, UndersCorrect, UndersBetReturn, UndersProfit]
        return funcreturn

def appendonlyfirmresults(df):
    x = df[df['FormulaPrediction'] != "Not conclusive"] 
    y = appendresults(x)
    return y

    
def appendnewresultstomodelresultscsvandsql(predresultsdf):
    modelresults = openmodelresults("modelresults.csv")
    to_append = appendresults(predresultsdf)
    dflen = len(modelresults)
    modelresults.loc[dflen] = to_append
    to_append = appendonlyfirmresults(predresultsdf)
    dflen = len(modelresults)
    modelresults.loc[dflen] = to_append
    SEP = os.sep
    dir = os.path.dirname
    projectpath = dir(dir(dir(os.path.abspath(__file__))))
    modelspath = projectpath + SEP + "data" + SEP + "modelresults.csv"
    modelresults.to_csv(modelspath)
    modelresultstosql(modelresults)
    modelshort(modelresults)
    print("Appending done")

def showtotalresultsforateam(team, predresultsdf, regressor):
    modelresults = openmodelresults("modelresults.csv")
    modelresults = modelresults.iloc[0:0]
    to_append = appendresults(predresultsdf)
    dflen = len(modelresults)
    modelresults.loc[dflen] = to_append
    to_append = appendonlyfirmresults(predresultsdf)
    dflen = len(modelresults)
    modelresults.loc[dflen] = to_append
    SEP = os.sep
    dir = os.path.dirname
    projectpath = dir(dir(dir(os.path.abspath(__file__))))
    modelspath = projectpath + SEP + "data" + SEP + team + "_" + regressor + "_" + ".csv"
    modelresults.to_csv(modelspath)
    print("CSV Saved")
    return modelresults


def addtotalwinningscolumn(df, team, regressor):
    df = df.sort_values(by="Date")
    conditions = [df["GameNumber"] > 1,
                df["GameNumber"] == 1]
    values = [1, 1]            
    df["Gamenumberfor%"] = np.select(conditions, values)
    df['TotalGames'] = df['Gamenumberfor%'].cumsum()
    conditions = [(df["SystemResult"] == "Correct"),
                (df["SystemResult"] == "Incorrect")]
    values = [0.83, -1]            
    df["BetReturn"] = np.select(conditions, values)
    df['RunningTotalAll'] = df['BetReturn'].cumsum()
    df["BetReturn%"] = (df['RunningTotalAll']/(df['TotalGames']))*100
    df['BetReturn%'] = df['BetReturn%'].apply(lambda x: float("{:.2f}".format(x)))
    conditions = [df["FormulaPrediction"] == "Not conclusive",
                (df["FormulaPrediction"] != "Not conclusive") & (df["SystemResult"] == "Correct"),
                (df["FormulaPrediction"] != "Not conclusive") & (df["SystemResult"] == "Incorrect")]
    values = [np.NaN, 0.83, -1]
    df["BetReturnWithoutNC"] = np.select(conditions, values)
    df['RunningTotalWithoutNC'] = df['BetReturnWithoutNC'].cumsum()
    df['RunningTotalWithoutNC'] = df['RunningTotalWithoutNC'].fillna(method='ffill')
    conditions = [df["FormulaPrediction"] == "Not conclusive",
                df["FormulaPrediction"] != "Not conclusive"]
    values = [0, 1]            
    df["TotalConclusives"] = np.select(conditions, values)
    df['TotalConclusiveGames'] = df['TotalConclusives'].cumsum()
    df['TotalConclusiveGames'] = df['TotalConclusiveGames'].fillna(method='ffill')
    df["BetReturnWithoutNC%"] = (df['RunningTotalWithoutNC']/(df['TotalConclusiveGames']))*100
    df['BetReturnWithoutNC%'] = df['BetReturnWithoutNC%'].apply(lambda x: float("{:.2f}".format(x)))
    df["Date"] = pd.to_datetime(df["Date"], format='%Y/%m/%d', errors = 'ignore')
    df["BetReturn%"] = pd.to_numeric(df["BetReturn%"], downcast="float")
    df["BetReturnWithoutNC%"] = pd.to_numeric(df["BetReturnWithoutNC%"], downcast="float")
    df = df[df['BookiePrediction'] != 0]
    linegraph = df[["Date", "BetReturn%", "BetReturnWithoutNC%"]]
    linegraphfunc(linegraph, team, regressor)
    return df


def shortversionofresults(df):
    newdf = df[["Regressor", "ContainsNotConclusivePred", "Totalgames", "TotalCorrect", "BetReturn", "BetProfit"]]
    return newdf


def donutdfmaker(df):
    newdf = df[["ContainsNotConclusivePred", "Correct", "BetProfit"]]
    newdf = newdf.rename(columns={"ContainsNotConclusivePred": "Scenario"})
    conditions = [newdf["Scenario"] == True,
                newdf["Scenario"] == False]
    values = ["All Predictions", "Conclusive Predictions"]            
    newdf["Scenario"] = np.select(conditions, values)
    new_row = {'Scenario':'Break Even', 'Correct':"55.00%"}
    newdf = newdf.append(new_row, ignore_index=True)
    return newdf
