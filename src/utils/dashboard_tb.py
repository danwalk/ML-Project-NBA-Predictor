import os, sys

dir = os.path.dirname
SEP = os.sep
src = dir(dir(os.path.abspath(__file__)))
sys.path.append(src)
project_path = dir(dir(dir(os.path.abspath(__file__))))
sys.path.append(project_path)

from utils.visualization_tb import modelresultsbargraph
import pandas as pd

def modelshort(modeldf):
    pd.set_option('mode.chained_assignment',None)
    modeldf = modeldf[["Regressor", "EstimatorsorNeigbor", "ContainsNotConclusivePred", "BetProfit"]]
    modeldf['BetProfit'] = modeldf['BetProfit'].str.rstrip('%').astype('float')
    modeldf = modeldf.sort_values(by=['BetProfit'], ascending=False)
    modeldf.columns = ['Model', 'Param', "Bet Type", "Profit%"]
    modelresultsbargraph(modeldf)
    return modeldf