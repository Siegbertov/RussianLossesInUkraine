import pandas as pd
import matplotlib.pyplot as plt
from csv_creator import create


def main():
    # Reading CSV
    df = pd.read_csv("enemy_loses.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")
    df.set_index("Date", inplace=True)

    # Creating PLOT
    fig, ax = plt.subplots(1, 1)
    fig.suptitle('Russian Loses in war against Ukraine', fontsize=16)
    fig.set_figwidth(12)
    fig.set_figheight(6)
    ax.plot(df.index, df["Troops"], color="black")
    ax.fill_between(df.index, df["Troops"], color="#C5C5C5")
    ax.set_xlabel("Daily")
    ax.set_ylabel("Total Troops")

    name = df.index[0].strftime("%Y-%m-%d").split("-")[1:]
    name.reverse()
    plt.savefig(f"images/{'-'.join(name)}.png")



if __name__ == "__main__":
    create()
    main()
