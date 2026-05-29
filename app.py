#----------------------------------------------------------------------- IMPORT STATEMENTS ---------------------------------------------------------------------


from flask import request, Flask, jsonify, render_template
import pandas as pd
from helpers import get_headshot_url

#----------------------------------------------------------------------- LOAD CSV, USE FLASK ---------------------------------------------------------------------

df = pd.read_csv('scored_players.csv')
app = Flask(__name__)

#----------------------------------------------------------------------- HAVE INDEX OPEN ---------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

#----------------------------------------------------------------------- OVERVIEW ROUTE ---------------------------------------------------------------------

@app.route('/overview')
def overview():
    position_avg = df.groupby('Pos')['ValuePerMillion'].mean().reset_index() #calculate position averages relative to their position
    top10 = df.nlargest(10, 'ValuePerMillion').reset_index(drop=True) #find top 10
    top10.index = top10.index + 1
    bottom10 = df.nsmallest(10, 'ValuePerMillion').reset_index(drop=True) # find bottom 10
    bottom10.index = bottom10.index +1
    return render_template('overview.html',
        position_avg = position_avg.to_dict('records'),
        top10=list(enumerate(top10.to_dict('records'), 1)),
        bottom10=list(enumerate(bottom10.to_dict('records'), 1))) # pass position average, top 10, bottom 10 to overview.html

#----------------------------------------------------------------------- PLAYER ROUTE---------------------------------------------------------------------

@app.route('/player')
def player():
    name = request.args.get('name') # get player name
    players_list = df['Player'].sort_values().tolist()
    if name:
        row = df[df['Player'] == name].iloc[0] # find player row
        url = get_headshot_url(name) # get url link for player headshot
        return render_template('player.html', row=row, url=url, players_list=players_list, selected=name) # render player.html
    return render_template('player.html', players_list=players_list, selected=None) # if no name, enter None, no photo

#----------------------------------------------------------------------- COMPARE ROUTE ---------------------------------------------------------------------

@app.route('/compare')
def compare():
    players_list = df['Player'].sort_values().tolist() # get players list, and both players
    p1 = request.args.get('p1')
    p2 = request.args.get('p2')

#----------------------------------------------------------------------- IF BOTH PLAYERS HAVE PHOTOS ---------------------------------------------------------------------

    if p1 and p2: 
        row1 = df[df['Player'] == p1].iloc[0]
        row2 = df[df['Player'] == p2].iloc[0]
        url1 = get_headshot_url(p1)
        url2 = get_headshot_url(p2) # get players and photos 
        stat_defs = [
            ('Points', 'PTS', True),
            ('Assists', 'AST', True),
            ('Rebounds', 'TRB', True),
            ('Steals', 'STL', True),
            ('Blocks', 'BLK', True),
            ('TS%', 'TS%', True),
            ('Win Shares', 'WS', True),
            ('BPM', 'BPM', True),
            ('VORP', 'VORP', True),
            ('Salary', 'Salary', False),
            ('Score', 'Score', True),
            ('Value/Million', 'ValuePerMillion', True),
        ] # get their stats from exported csv

#----------------------------------------------------------------------- COMPARE EACH INDIVIDUAL STAT ---------------------------------------------------------------------

        stats = [] 
        for label, col, higher_is_better in stat_defs:
            v1 = row1[col] 
            v2 = row2[col] 
            tie = (v1 == v2) # find stat1, stat2 values, and see if tie
            p1_wins = (v1 > v2) if higher_is_better else (v1 < v2)
            p2_wins = (v2 > v1) if higher_is_better else (v2 < v1) # find the winner
            if col == 'Salary':
                f1 = f"${v1:,.0f}"
                f2 = f"${v2:,.0f}" # adjust salary symbols
            elif col in ['Score', 'ValuePerMillion', 'TS%', 'VORP', 'BPM', 'WS']:
                f1 = f"{v1:.3f}"
                f2 = f"{v2:.3f}" # format if it is the following stats
            else:
                f1 = f"{v1:.1f}"
                f2 = f"{v2:.1f}" # otherwise use this format
            stats.append({'label': label, 'v1': f1, 'v2': f2, 'p1_wins': p1_wins, 'p2_wins': p2_wins, 'tie': tie}) # append the following to the stats list
        return render_template('compare.html', p1=p1, p2=p2, url1=url1, url2=url2, stats=stats, players_list=players_list) # input the stats list and others to compare.html

#----------------------------------------------------------------------- CHECK INDIVIDUAL NAMES NOW ---------------------------------------------------------------------

    elif p1:
        return render_template('compare.html', players_list=players_list, p1=p1, p2=None, stats=None)

    elif p2:
        return render_template('compare.html', players_list=players_list, p1=None, p2=p2, stats=None)

    else:
        return render_template('compare.html', players_list=players_list, p1=None, p2=None, stats=None)

#----------------------------------------------------------------------- RUN PROGRAM ---------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)

    