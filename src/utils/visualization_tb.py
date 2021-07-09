import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import pandas as pd
import re

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
    projectpath = os.path.dirname(os.getcwd())
    imagepath = projectpath + SEP + "resources" + SEP + team + "_" + regressor + ".jpg"
    plt.savefig(imagepath)
    plt.show()
    print("Line Graph Saved")

def donutgraph(df, team, regressor):
    data = df
    print(data.head())
    startingRadius = 0.7 + (0.3* (len(data)-1))
    for index, row in data.iterrows():
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
    projectpath = os.path.dirname(os.getcwd())
    imagepath = projectpath + SEP + "resources" + SEP + team + "_betdonut_" + regressor + ".jpg"
    plt.savefig(imagepath)
    plt.show()
    print("Donut Saved")