import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import linregress


def draw_plot():
    # Read data from file
    df = pd.read_csv("./epa-sea-level.csv")
    # i added the range for X and Y to 2050 for the regression line
    New_year = np.arange(1880, 2051)
    Short_year = np.arange(2000, 2051)  # thiss second range is for the short line to not distort the plot

    # Create scatter plot
    x = df["Year"]
    y = df["CSIRO Adjusted Sea Level"]
    plt.scatter(x, y)

    # Create first line of best fit
    res = linregress(x, y)

    plt.plot(New_year, res.intercept + res.slope * New_year, 'r', label='fitted line')
    plt.xticks(range(1850, 2076, 25))  # the values of the X axis that are going to be showed

    # Create second line of best fit
    # here we are setting the database for the line of best fit from 2000 to the max data available
    dfs = df.set_index('Year')  # setting the Year ass a index
    dfs = dfs.loc[2000:2050]  # slicing the data for a new line
    xs = dfs.index  # calling the X as the year for the plot
    ys = dfs['CSIRO Adjusted Sea Level']  # setting the Y axis as the sea level for the new line
    S_res = linregress(xs, ys)  # this is the new line with the sliced data
    plt.plot(Short_year, S_res.intercept + S_res.slope * Short_year, 'g', label='fitted line')
    plt.title("Rise in Sea Level")
    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")

    # Add labels and title

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()