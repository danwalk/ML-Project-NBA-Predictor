import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import pandas as pd
import re
import numpy as np
import seaborn as sns
from matplotlib.pyplot import figure

def linegraphfunc(df, team, regressor):
    plt.figure(figsize=(10,5))
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()
    months = mdates.MonthLocator()
    plt.plot(df["Date"],df["BetReturn%"], color='blue', linestyle='--', label = "All Bets %")
    plt.plot(df["Date"],df["BetReturnWithoutNC%"], color='green', linestyle='--', label = "Conclusive Bets %")
    plt.axhline(y=0, linewidth=2, color='red')
    ax.set_xlabel('Date')
    ax.set_ylabel('% of Investment Returned')
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_minor_locator(months)
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.legend()
    plt.grid(True)
    Title1 = team + " " + regressor + " Return % From Investment" 
    plt.legend()
    plt.title(Title1)
    SEP = os.sep
    dir = os.path.dirname
    projectpath = dir(dir(dir(os.path.abspath(__file__))))
    imagepath = projectpath + SEP + "resources" + SEP + team + "_" + regressor + ".jpg"
    plt.savefig(imagepath)
    plt.show()
    print("Line Graph Saved")
    return "Line Graph Ok"



def donutgraph(df, team, regressor):
    print(df.head())
    startingRadius = 0.7 + (0.3* (len(df)-1))
    for index, row in df.iterrows():
        scenario = row["Scenario"]
        percentage = row["Correct"]
        textLabel = scenario + ' ' + percentage
        percentage = int(re.search(r'\d+', percentage).group())
        remainingPie = 100 - percentage
        donut_sizes = [remainingPie, percentage]
        if percentage > 55:
            color="green"
        elif percentage == 55:
            color="grey"
        else:
            color="red"
        plt.text(0.01, startingRadius + 0.07, textLabel, horizontalalignment='right', verticalalignment='top')
        plt.pie(donut_sizes, radius=startingRadius, startangle=90, colors=['white', color],
                wedgeprops={"edgecolor": "white", 'linewidth': 1})
        startingRadius-=0.3
    plt.axis('equal')
    circle = plt.Circle(xy=(0, 0), radius=0.35, facecolor='white')
    plt.gca().add_artist(circle)
    Title1 = team + " " + regressor + " Win % from bets"
    plt.title(Title1)
    SEP = os.sep
    dir = os.path.dirname
    projectpath = dir(dir(dir(os.path.abspath(__file__))))
    imagepath = projectpath + SEP + "resources" + SEP + team + "_betdonut_" + regressor + ".jpg"
    plt.savefig(imagepath)
    plt.show()
    print("Donut Saved")
    return "Donut Graph Ok"

def modelresultsbargraph(df):
    figure(figsize=(8, 6), dpi=80)
    df["modeon"] = df["Model"] + df["Param"].astype(str)
    df = df.replace({'Bet Type': {1: "All Bets", 
                                0: "Conclusive Bets"}})
    sns.set_style("darkgrid")
    ax = sns.barplot(x="Profit%", y="modeon", hue="Bet Type", data=df)
    plt.ylabel("Model + Param")
    plt.title("Model vs % Profit - Comparison")
    SEP = os.sep
    dir = os.path.dirname
    projectpath = dir(dir(dir(os.path.abspath(__file__))))
    imagepath = projectpath + SEP + "resources" + SEP + "ModelBarGraph.jpg"
    plt.legend(bbox_to_anchor=(1.01, 1),
            borderaxespad=0)
    plt.tight_layout()
    plt.savefig(imagepath)
    plt.show()
    return "Model Graph Saved"
