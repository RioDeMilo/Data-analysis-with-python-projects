import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['height'] = df['height'] * 0.01
df['overweight'] = ((df['weight'] / (df['height']) ** 2) >= 25).replace({True: 1, False: 0})

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
##using the same .replace to change the mask values if the column
df['cholesterol'] = (df['cholesterol'] == 1).replace({True: 0, False: 1})
df['gluc'] = (df['gluc'] == 1).replace({True: 0, False: 1})


def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from
    # 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    vars = sorted(
        ["cholesterol", "gluc", "smoke", "alco", "active", "overweight"]
    )

    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=vars,
    )

    # Group and reformat the data to split it by 'cardio'. Show the counts of
    # each feature. You will have to rename one of the columns for the catplot
    # to work correctly.
    df_cat = df_cat.value_counts().reset_index(name="total")

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(
        data=df_cat,
        x="variable",
        y="total",
        hue="value",
        col="cardio",
        kind="bar",
        order=vars,
    )
    fig.set_ylabels("total")
    fig.set_xlabels("variable")
    fig = fig.fig

    # Do not modify the next two lines
    # fig.savefig("catplot.png") # Don't save to file
    return fig

# Draw Heat Map
def draw_heat_map():
    # Clean the data
    # here in this case we add the conditions for the clean database that filter the values in this case adding the required conditions for being a valid data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = (df_heat.corr().round(1))

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(250, 20, as_cmap=True)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 9))

    # Draw the heatmap with 'sns.heatmap()'

    ax = sns.heatmap(
        corr,
        mask=mask,
        vmax=0.4,
        square=True,
        fmt=".1f",
        annot=True,
    )

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig