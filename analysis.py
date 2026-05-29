#----------------------------------------------------------------------- IMPORT STATEMENTS ---------------------------------------------------------------------


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#----------------------------------------------------------------------- LOAD CSV'S FROM BASKETBALL REFERENCE ---------------------------------------------------------------------

advanced = pd.read_csv('advanced_stats.csv')
per_game = pd.read_csv('per_game.csv')
salaries = pd.read_csv('salaries.csv')

#----------------------------------------------------------------------- FILTER ROWS WITH DUPLICATES. REMOVE PLAYERS WHO DIDN'T PLAY---------------------------------------------------------------------


advanced = advanced.drop_duplicates(subset = ["Player", "Team"], keep = "first")
advanced = advanced[advanced['MP'] >=400]
traded = advanced[advanced['Team'].isin(['2TM', '3TM', '4TM'])]['Player'].unique()
advanced = advanced[
    (advanced['Player'].isin(traded) & advanced['Team'].isin(['2TM', '3TM', '4TM'])) |
    (~advanced['Player'].isin(traded))
]

per_game = per_game.drop_duplicates(subset = ["Player", "Team"], keep = "first")
traded = per_game[per_game['Team'].isin(['2TM', '3TM', '4TM'])]['Player'].unique()
per_game = per_game[
    (per_game['Player'].isin(traded) & per_game['Team'].isin(['2TM', '3TM', '4TM'])) |
    (~per_game['Player'].isin(traded))
]
salaries = salaries.drop_duplicates(subset=['Player'], keep='first')

salaries['2025-26'] = salaries['2025-26'].str.replace('$', '', regex=False).astype(float)

col_index = salaries.columns.get_loc("2025-26")
salaries = salaries.iloc[:, : col_index + 1]

#----------------------------------------------------------------------- MERGE ALL 3 CSV'S INTO ONE ---------------------------------------------------------------------

merged = pd.merge(per_game, advanced, on=["Player", "Team"], how="inner")
merged = pd.merge(merged, salaries, on="Player", how="inner")

#----------------------------------------------------------------------- RENAME COLUMNS FOR PRACTICALITY---------------------------------------------------------------------

merged = merged.rename(columns={"2025-26": "Salary"})
merged = merged.rename(columns={"Pos_x": "Pos"})
merged = merged.rename(columns={"MP_x": "MPG"})

#----------------------------------------------------------------------- FILTER MERGED AGAIN ---------------------------------------------------------------------

merged = merged[merged['MPG'] >= 10]
merged = merged[merged['Salary'] >= 1500000]

#----------------------------------------------------------------------- NORMALIZE THE FOLLOWING STATS---------------------------------------------------------------------

for col in ['VORP', 'BPM', 'TS%', 'WS', 'PTS', 'MPG', 'AST', 'TRB', 'PER', 'STL', 'BLK']:
    merged[col + '_norm'] = merged.groupby('Pos')[col].transform(
        lambda x: (x - x.min()) / (x.max() - x.min())
    )

#----------------------------------------------------------------------- SCORE FORMULA ---------------------------------------------------------------------

merged['Score'] = (0.35* merged['VORP_norm']) + (0.10 * merged['BPM_norm']) + (0.05*merged['TS%_norm']) + (0.20 * merged['PTS_norm']) + (0.05*merged['WS_norm']) + (0.05 * merged['MPG_norm']) + \
    (0.10*merged['PER_norm']) + (0.05*merged['STL_norm']) + (0.05*merged['BLK_norm'])
merged['ValuePerMillion'] = merged['Score'] / (np.log(merged['Salary'] / 1000000))

#----------------------------------------------------------------------- EXPORT CSV ---------------------------------------------------------------------

merged.to_csv('scored_players.csv', index=False)

#----------------------------------------------------------------------- CREATE PLOT GRAPH ---------------------------------------------------------------------

df = pd.read_csv('scored_players.csv')

position_avg = df.groupby('Pos')["ValuePerMillion"].mean().reset_index()

plt.figure(figsize=(10, 6), facecolor='#0f1117')
ax = plt.axes()
ax.set_facecolor('#0f1117')

colors = ['#00b4d8', '#90e0ef', '#0077b6', '#48cae4', '#023e8a']
order = ['PG', 'SG', 'SF', 'PF', 'C']
sns.barplot(data=position_avg, x='Pos', y='ValuePerMillion', hue=colors, legend=False, order=order)

plt.title('Average Value Per Million by Position', color='white', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Position', color='white', fontsize=12)
plt.ylabel('Value Per Million', color='white', fontsize=12)
plt.xticks(color='white')
plt.yticks(color='white')
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.yaxis.grid(True, color='#ffffff20')


plt.show()
