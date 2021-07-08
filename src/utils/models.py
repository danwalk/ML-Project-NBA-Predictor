import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import RidgeCV
from sklearn.neighbors import RadiusNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn import linear_model
import pickle
import os
from .dataframes import systempredictionmaker
from .dataframes import predictionmaker
from .dataframes import appendnewresultstomodelresultscsvandsql
from .folders_tb import opennbacsv



def fitmodel(X, y, regressor, eon=5, savemodel=False):
    if regressor=="LinearRegression":
        reg = LinearRegression(n_jobs=-1)
    elif regressor=="RandomForestRegressor":
        reg = RandomForestRegressor(n_estimators= eon, random_state=1)
    elif regressor=="DecisionTreeRegressor":
        reg = DecisionTreeRegressor(criterion= eon)
    elif regressor=="RidgeCV":
        reg = RidgeCV()
    elif regressor=="GradientBoostingRegressor":
        reg = GradientBoostingRegressor(random_state=1)
    elif regressor=="GaussianProcessRegressor":
        reg = GaussianProcessRegressor(random_state=1)
    elif regressor=="BayesianRidge":
        reg = linear_model.BayesianRidge()
    elif regressor=="KNeighborsRegressor":
        reg = KNeighborsRegressor(n_neighbors=eon)
    elif regressor=="RadiusNeighborsRegressor":
        reg = RadiusNeighborsRegressor(n_jobs=-1)
    else:
        reg = SVR(gamma=.1, kernel='rbf', C=1.0, epsilon=eon)
    tree_preprocessor = ColumnTransformer(
    [
        ("categorical", OrdinalEncoder(),
            ["Homeoraway", "Favourite", "OpponentFormReceivedLast10Games"]),
        ("numeric", "passthrough",
            ["Teamodds", "Totalscorepred", "Teamwinpred", "Teamscorepred", "Opponentscorepred",
            "Teamscore", "Totalscorereal", "Totalfrompred", "Scoredfrompred",
            "OpponentAvgRealReceived10games", "OpponentAvgPredReceived10games",
            "OpponentAvgDifReceivedRealvsPred10games", "OpponentReceivedOorULast10Games"
            ]),
    ],
    remainder="drop")
    model = Pipeline([
        ("preprocessor", tree_preprocessor),
        ("regressor", reg),
    ])
    model1 = model.fit(X, y)
    if savemodel == True:
        SEP = os.sep
        projectpath = os.path.dirname(os.getcwd())
        modelspath = projectpath + SEP + "models"
        finalizedmodel = regressor + str(eon)
        pathandname = modelspath + SEP + finalizedmodel
        filename = pathandname + '.sav'
        pickle.dump(model, open(filename, 'wb'))
        print("Model Pickle Saved")
    return model1

def predictor(Team, predgamenumber, regressor="SVR", eon=5, savemodel=1):
    if savemodel == 0:
        savemodel = True
    else:
        savemodel = False
    columnlist = ["Date", "Homeoraway", "Opponent", "Teamodds", "Teamscore", "Opponentodds",
                "Opponentscore", "Favourite", "Totalscorepred", "Totalscorereal",
                "Totalfrompred", "Teamwinpred", "Teamscorepred", "Scoredfrompred",
                "Opponentwinpred", "Opponentscorepred", "Receivedfrompred"]
    nba = opennbacsv("nbaclean.csv") #Function called to retrieve DF
    pd.set_option('mode.chained_assignment',None)
    x = nba.loc[nba["Team"] == Team] #New DF made to filter the team to predict
    gamesfinished = predgamenumber - 1
    x = x.head(gamesfinished)[columnlist]
    x = x.tail(10)[columnlist]
    columnstoadd = ["OpponentAvgRealScored10games", "OpponentAvgPredScored10games", "OpponentAvgDifScoredRealvsPred10games", 
                    "OpponentAvgRealReceived10games", "OpponentAvgPredReceived10games", "OpponentAvgDifReceivedRealvsPred10games",
                    "OpponentFormScoredLast10Games", "OpponentFormReceivedLast10Games", "OpponentReceivedOorULast10Games"]
    for column in columnstoadd: #Add columns as NaN to update DF with the opponents statistics over previous games
        x[column] = np.nan
    realscore = x["Teamscore"].iloc[-1] 
    teamscoreavg = x["Teamscore"].mean()
    opposcoreavg = x["Opponentscorepred"].mean()
    totalscoreavg = x["Totalscorepred"].mean()
    x["Teamscore"].iloc[-1] = teamscoreavg #these scores are modified before using fit as the actual value would not be available before the game
    x["Opponentscore"].iloc[-1] = opposcoreavg #these scores are modified same reason as teamscoreavg
    x["Totalscorereal"].iloc[-1] = totalscoreavg #these scores are modified same reason as teamscoreavg
    x["Totalfrompred"].iloc[-1] = x["Totalscorepred"].iloc[-1] - x["Totalscorepred"]. iloc[-2] #these scores are modified same reason as teamscoreavg
    x["Scoredfrompred"].iloc[-1] = (x["Totalscorepred"].iloc[-1] - x["Totalscorepred"]. iloc[-2])/2 #these scores are modified same reason as teamscoreavg
    x["Receivedfrompred"].iloc[-1] = (x["Totalscorepred"].iloc[-1] - x["Totalscorepred"]. iloc[-2])/2 #these scores are modified same reason as teamscoreavg
    opporange = np.arange(0, (len(x)))
    for i in opporange:
        opponentteam = x["Opponent"].iloc[i]
        opponentdf = nba.loc[nba["Team"] == opponentteam]
        opponentdf = opponentdf.head(predgamenumber)[columnlist]
        opponentdf = opponentdf.tail(11)[columnlist]
        opponentdf = opponentdf[:-1]
        conditions = [(opponentdf["Opponentscore"] >= opponentdf["Opponentscorepred"]),
                    (opponentdf["Opponentscore"] < opponentdf["Opponentscorepred"])]
        values = [1, 0]
        opponentdf["OUPred"] = np.select(conditions, values)
        x["OpponentAvgRealScored10games"].iloc[i] = opponentdf["Teamscore"].mean()
        x["OpponentAvgPredScored10games"].iloc[i] = opponentdf["Teamscorepred"].mean()
        x["OpponentAvgDifScoredRealvsPred10games"].iloc[i] = opponentdf["Scoredfrompred"].mean()
        x["OpponentAvgRealReceived10games"].iloc[i] = opponentdf["Opponentscore"].mean()
        x["OpponentAvgPredReceived10games"].iloc[i] = opponentdf["Opponentscorepred"].mean()
        x["OpponentAvgDifReceivedRealvsPred10games"].iloc[i] = opponentdf["Receivedfrompred"].mean()
        x["OpponentReceivedOorULast10Games"].iloc[i] = opponentdf["OUPred"].sum() 
        if opponentdf["Scoredfrompred"].mean() > 0:
            x["OpponentFormScoredLast10Games"].iloc[i] = "FormIsScoringOver"
        else:
            x["OpponentFormScoredLast10Games"].iloc[i] = "FormIsScoringUnder"
        if opponentdf["Receivedfrompred"].mean() > 0:
            x["OpponentFormReceivedLast10Games"].iloc[i] = "FormIsReceivingOver"
        else:
            x["OpponentFormReceivedLast10Games"].iloc[i] = "FormIsReceivingUnder"
    model = fitmodel(x, x["Teamscore"], regressor, eon, savemodel)
    Bookie = x["Teamscorepred"].iloc[-1]
    last10gamesscoring = float("{:.2f}".format(x["Teamscore"].mean()))
    opponentlast10games = float("{:.2f}".format(x["OpponentAvgRealReceived10games"].iloc[-1]))
    opponentform = x["OpponentReceivedOorULast10Games"].iloc[-1]
    systemprediction = float("{:.2f}".format(model.predict(x)[-1]))
    VariablePrediction = predictionmaker(Bookie, last10gamesscoring, opponentlast10games, opponentform, systemprediction)
    SystemStraightPrediction = systempredictionmaker(Bookie, systemprediction)
    if SystemStraightPrediction == "Over" and realscore > Bookie:
        SystemPred = "Correct"
    elif SystemStraightPrediction == "Under" and realscore < Bookie:
        SystemPred = "Correct"
    else:
        SystemPred = "Incorrect"
    date = x["Date"].iloc[-1]
    Column2predict = "TeamScore"
    estimatororneigbor = eon
    funcreturn = [date, Column2predict, Team, predgamenumber, regressor, estimatororneigbor, Bookie, last10gamesscoring, opponentlast10games, 
    opponentform, systemprediction, SystemStraightPrediction, VariablePrediction, realscore, SystemPred]
    return funcreturn

def gamepredictor(Team, predgamenumber, regressor="SVR", eon=5, savemodel=1):
    if savemodel == 0:
        savemodel = True
    else:
        savemodel = False
    columnlist = ["Date", "Homeoraway", "Opponent", "Teamodds", "Teamscore", "Opponentodds",
                "Opponentscore", "Favourite", "Totalscorepred", "Totalscorereal",
                "Totalfrompred", "Teamwinpred", "Teamscorepred", "Scoredfrompred",
                "Opponentwinpred", "Opponentscorepred", "Receivedfrompred"]
    nba = opennbacsv("nbaclean.csv")
    pd.set_option('mode.chained_assignment',None)
    x = nba.loc[nba["Team"] == Team] #New DF made to filter the team to predict
    gamesfinished = predgamenumber - 1
    x = x.head(gamesfinished)[columnlist]
    x = x.tail(10)[columnlist]
    oppo = x["Opponent"].iloc[-1]
    columnstoadd = ["OpponentAvgRealScored10games", "OpponentAvgPredScored10games", "OpponentAvgDifScoredRealvsPred10games", 
                    "OpponentAvgRealReceived10games", "OpponentAvgPredReceived10games", "OpponentAvgDifReceivedRealvsPred10games",
                    "OpponentFormScoredLast10Games", "OpponentFormReceivedLast10Games", "OpponentReceivedOorULast10Games"]
    for column in columnstoadd: #Add columns as NaN to update DF with the opponents statistics over previous games
        x[column] = np.nan
    realscore = x["Teamscore"].iloc[-1] 
    teamscoreavg = x["Teamscore"].mean()
    opposcoreavg = x["Opponentscorepred"].mean()
    totalscoreavg = x["Totalscorepred"].mean()
    x["Teamscore"].iloc[-1] = teamscoreavg #these scores are modified before using fit as the actual value would not be available before the game
    x["Opponentscore"].iloc[-1] = opposcoreavg #these scores are modified same reason as teamscoreavg
    x["Totalscorereal"].iloc[-1] = totalscoreavg #these scores are modified same reason as teamscoreavg
    x["Totalfrompred"].iloc[-1] = x["Totalscorepred"].iloc[-1] - x["Totalscorepred"]. iloc[-2] #these scores are modified same reason as teamscoreavg
    x["Scoredfrompred"].iloc[-1] = (x["Totalscorepred"].iloc[-1] - x["Totalscorepred"]. iloc[-2])/2 #these scores are modified same reason as teamscoreavg
    x["Receivedfrompred"].iloc[-1] = (x["Totalscorepred"].iloc[-1] - x["Totalscorepred"]. iloc[-2])/2 #these scores are modified same reason as teamscoreavg
    opporange = np.arange(0, (len(x)))
    for i in opporange:
        opponentteam = x["Opponent"].iloc[i]
        opponentdf = nba.loc[nba["Team"] == opponentteam]
        opponentdf = opponentdf.head(predgamenumber)[columnlist]
        opponentdf = opponentdf.tail(11)[columnlist]
        opponentdf = opponentdf[:-1]
        conditions = [(opponentdf["Opponentscore"] >= opponentdf["Opponentscorepred"]),
                    (opponentdf["Opponentscore"] < opponentdf["Opponentscorepred"])]
        values = [1, 0]
        opponentdf["OUPred"] = np.select(conditions, values)
        x["OpponentAvgRealScored10games"].iloc[i] = opponentdf["Teamscore"].mean()
        x["OpponentAvgPredScored10games"].iloc[i] = opponentdf["Teamscorepred"].mean()
        x["OpponentAvgDifScoredRealvsPred10games"].iloc[i] = opponentdf["Scoredfrompred"].mean()
        x["OpponentAvgRealReceived10games"].iloc[i] = opponentdf["Opponentscore"].mean()
        x["OpponentAvgPredReceived10games"].iloc[i] = opponentdf["Opponentscorepred"].mean()
        x["OpponentAvgDifReceivedRealvsPred10games"].iloc[i] = opponentdf["Receivedfrompred"].mean()
        x["OpponentReceivedOorULast10Games"].iloc[i] = opponentdf["OUPred"].sum() 
        if opponentdf["Scoredfrompred"].mean() > 0:
            x["OpponentFormScoredLast10Games"].iloc[i] = "FormIsScoringOver"
        else:
            x["OpponentFormScoredLast10Games"].iloc[i] = "FormIsScoringUnder"
        if opponentdf["Receivedfrompred"].mean() > 0:
            x["OpponentFormReceivedLast10Games"].iloc[i] = "FormIsReceivingOver"
        else:
            x["OpponentFormReceivedLast10Games"].iloc[i] = "FormIsReceivingUnder"
    model = fitmodel(x, x["Teamscore"], regressor, eon=eon, savemodel=savemodel)
    Bookie = x["Teamscorepred"].iloc[-1]
    last10gamesscoring = float("{:.2f}".format(x["Teamscore"].mean()))
    opponentlast10games = float("{:.2f}".format(x["OpponentAvgRealReceived10games"].iloc[-1]))
    opponentform = x["OpponentReceivedOorULast10Games"].iloc[-1]
    print(f'{Team} in game {predgamenumber} vs {oppo}')
    print("-----------------------------")
    print(f'Bookies predicted points for {Team} is: {Bookie}')
    print(f'{Team} last 10 games scoring Avg is: {last10gamesscoring}')
    print(f'Over the previous 10 games {oppo} receiving Avg is: {opponentlast10games}')
    print(f'In {oppo} previous 10 games, {opponentform} of their games have gone over the bookies prediction')
    systemprediction = float("{:.2f}".format(model.predict(x)[-1]))
    print("SYSTEM PREDICTED score: ", systemprediction)
    VariablePrediction = predictionmaker(Bookie, last10gamesscoring, opponentlast10games, opponentform, systemprediction)
    print(f'Using the variable prediction, the programs recommendation is: {VariablePrediction}')
    SystemStraightPrediction = systempredictionmaker(Bookie, systemprediction)
    print(f'The SYSTEMS STRAIGHT PREDICTION is: {SystemStraightPrediction} the bookies prediction')
    print("-----------------------------")
    print("Final Score (Real): ", realscore)
    if SystemStraightPrediction == "Over" and realscore > Bookie:
        SystemPred = "Correct"
    elif SystemStraightPrediction == "Under" and realscore < Bookie:
        SystemPred = "Correct"
    else:
        SystemPred = "Incorrect"
    print("The SYSTEM STRAIGHT PREDICTION was: ", SystemPred)
    print("-----------------------------")
    return None

def runteamseasonpredictor(team, regressor, eon, savemodel=1):
    games = list(range(10,73))
    columnnames= ["Date", "MarketPredicted", "Team", "GameNumber", "Regressor", "Estimatororneigbor", "BookiePrediction",
        "TeamAvg10Games", "OpponentAvg10Games", "OpponentFormOver10Games", "ModelScorePrediction", "ModelResultPrediction", 
        "FormulaPrediction", "RealScore", "SystemResult"]
    predresultsdf = pd.DataFrame(columns = columnnames)
    for i in games:
        to_append = predictor(team, i, regressor, eon, savemodel)
        dflen = len(predresultsdf)
        predresultsdf.loc[dflen] = to_append
    return predresultsdf

def runfullseasonpredictor(regressorlist, eon):
    regressors = regressorlist
    estimatororneigbor = eon
    games = list(range(10,73))
    teamlist = ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers",
        "Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers",
        "Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves",
        "New Orleans Pelicans","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns",
        "Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"]
    columnnames= ["Date", "MarketPredicted", "Team", "GameNumber", "Regressor", "Estimatororneigbor", "BookiePrediction",
        "TeamAvg10Games", "OpponentAvg10Games", "OpponentFormOver10Games", "ModelScorePrediction", "ModelResultPrediction", 
        "FormulaPrediction", "RealScore", "SystemResult"]
    for regressor in regressors:
        count = 0
        print(regressor)
        predresultsdf = pd.DataFrame(columns = columnnames)
        for team in teamlist:
            for i in games:
                to_append = predictor(team, i, regressor, estimatororneigbor, count)
                count += 1
                dflen = len(predresultsdf)
                predresultsdf.loc[dflen] = to_append
        appendnewresultstomodelresultscsvandsql(predresultsdf)
    return "Done"

