# all the imports
import os, json, plotly, requests
import pandas as pd
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('RIOTGAMES_SETTINGS', silent=True)


# Get the Data from the Riot Games API
api_key = "RGAPI-a7b3c202-4a92-4b44-8c53-5e1c7dad3f6e"
locale = "en_US"
payload = {'locale': locale, 'api_key': api_key}
# viz1 = requests.get("https://na1.api.riotgames.com/lol/static-data/v3/runes", params=payload)

# df = pd.read_json(json.dumps(viz1.json()['data']), orient='index')
# df = pd.concat([df, df['rune'].apply(lambda x: pd.Series(x))], axis=1)

# Chart one
# num_words = {1:'one', 2:'two', 3:'three', 4:'four', 5:'five'}
# tiers_count = df.tier.value_counts(ascending=True)
# x_tiers = pd.to_numeric(tiers_count.index).tolist()
# x_tiers = ['tier ' + num_words[x] for x in x_tiers]
# y_tiers = tiers_count.values
x_tiers = ['tier one', 'tier two', 'tier three']
y_tiers = [300, 250, 175]

@app.route('/')
def show_dashboard():
    return render_template('dashboard.html')
        
@app.route('/plotly')
def index():

    graphs = [
        dict(
            data=[
                dict(
                    x=x_tiers,
                    y=y_tiers,
                    type='bar'
                ),
            ],
            layout=dict(
                title='Number of Runes per Tier'
            )
        ),

        dict(
            data=[
                dict(
                    x=[1, 3, 5],
                    y=[10, 50, 30],
                    type='line',
                    marker=dict(color = 'rgb(142,124,195)')
                ),
            ],
            layout=dict(
                title='second graph',
            )
        ),
        dict(
            data=[
                dict(
                    x=[1, 3, 5, 6],
                    y=[10, 50, 30, 12],
                    type='bar',
                    marker=dict(color = 'rgb(106,90,205)')
                ),
            ],
            layout=dict(
                title='third graph'
            )
        ),
        dict(
            data=[
                dict(
                    x=[1, 3, 5, 6],
                    y=[10, 50, 30, 12],
                    type='bar',
                    marker=dict(color = 'rgb(0,191,255)')
                ),
            ],
            layout=dict(
                title='fourth graph'
            )
        )
        
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('plotly.html',
                           ids=ids,
                           graphJSON=graphJSON)
