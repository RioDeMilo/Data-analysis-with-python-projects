import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import unittest
import matplotlib as mpl
import matplotlib.ticker as mticker
from pandas.plotting import register_matplotlib_converters
from datetime import datetime

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
# Dont run the code multiple times
# first i change the index to date and drop the column of the date since the index contains the same value
def parse_date(x):
  return datetime.strptime(x, "%Y-%m-%d")
df = pd.read_csv(
    "./fcc-forum-pageviews.csv", # thanks to the dot we can read the file
    index_col=["date"], #now the  index column is date
    parse_dates=["date"], # here we apply the function parse_dates to the data "date"
    date_parser=parse_date,
)    
df = df.loc[
    (df["value"] >= df["value"].quantile(0.025))
    & (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
  #Draw line plot
  #here from subtplot we define the fig an the ax that are two diferrent values
  fig, ax = plt.subplots(figsize=(16, 6)) # thiss saves the fig  in the ax
  ax = sns.lineplot(data=df, x="date", y="value")# the ax value i the plotting of the cart
  ax.set(
      xlabel="Date",
      ylabel="Page Views",
      )
  ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df['Year'] = df.index.year
    df['Month'] = df.index.month_name()
    # the list is to give a order to the data set
    sort_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    # we aplied that order and
    df['Month'] = pd.Categorical(df['Month'], categories=sort_order)
    df_pivot = pd.pivot_table(
        df,
        values="value",
        index="Year",
        columns="Month",
        aggfunc=np.mean
    )

    # Draw bar plot
    ax = df_pivot.plot(kind="bar")
    # Get a Matplotlib figure from the axes object for formatting purposes
    fig = ax.get_figure()
    # Change the plot dimensions (width, height)
    fig.set_size_inches(7, 6)
    # Change the axes labels
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy().rename(columns={"value": "views"})
    df_box.reset_index(inplace=True)

    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    sns.boxplot(ax=ax1, data=df_box, x=df_box["year"], y=df_box["views"])

    # Remember to edit the labels after call to seaborn.
    ax1.set(
        xlabel="Year", ylabel="Page Views", title="Year-wise Box Plot (Trend)"
    )

    sns.boxplot(
        ax=ax2,
        data=df_box,
        x=df_box["month"],
        y=df_box["views"],
        order=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
    )

    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")
    fig.savefig('box_plot.png')
    return fig