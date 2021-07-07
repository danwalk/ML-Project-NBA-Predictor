import json
import os
import pandas as pd

def read_json_to_dict(json_fullpath):
    """
    Read a json and return a object created from it.
    Args:
        json_fullpath: json fullpath

    Returns: json object.
    """
    try:
        with open(json_fullpath, 'r+') as outfile:
            json_readed = json.load(outfile)
        return json_readed
    except Exception as error:
        raise ValueError(error)

def opennbacsv(filename):
    SEP = os.sep
    projectpath = os.path.dirname(os.getcwd())
    datapath = projectpath + SEP + "data"
    nba_all = datapath + SEP + filename
    nba = pd.read_csv(nba_all)
    nba['Teamwinpred'] = nba['Teamwinpred'].str.rstrip('%').astype('float') / 100.0
    nba['Opponentwinpred'] = nba['Opponentwinpred'].str.rstrip('%').astype('float') / 100.0
    nba.drop(["Country", "League", "Season"], axis=1, inplace=True)
    return nba

def openmodelresults(filename):
    SEP = os.sep
    projectpath = os.path.dirname(os.getcwd())
    datapath = projectpath + SEP + "data"
    modelres = datapath + SEP + filename
    modelresults = pd.read_csv(modelres, index_col=0)
    return modelresults