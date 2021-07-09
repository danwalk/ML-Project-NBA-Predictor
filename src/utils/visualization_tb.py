import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

def linegraphfunc(df, team, regressor):
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
    