# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import collections
import datetime
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import flask

server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

#colors = {
#    'background': '#111111',
#    'text': '#7FDBFF'
#}

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

df = pd.read_csv('data/county-level-jackie.csv')
date_cols = [x for x in list(df) if "date" in x]
for col in date_cols:
    df.loc[:, col] = pd.to_datetime(df[col])
df = df.rename({"location_1": "state", "location_2": "county"}, axis=1)

nyt = pd.read_csv('data/us-counties.csv')
nyt.loc[:, "date"] = pd.to_datetime(nyt["date"])

event_col_to_name = {
    "business_closed_date": "Business closure",
    "lockdown_closed_date": "Lockdown",
    "school_closed_date": "School closure",
    "college_closed_date": "College closure",
}
def get_county_events(state, county):
    """
    example return: {Timestamp('2020-03-17 00:00:00'): ['School closure'],
                     Timestamp('2020-03-21 00:00:00'): ['Business closure', 'Lockdown']}
    """
    sub_df = df[(df["state"] == state) & (df["county"] == county + " County")]
    return pd.DataFrame([[event_col_to_name[field], sub_df[field].min()] for field in event_col_to_name], columns=["event", "date"]).sort_values(
        'date').groupby('date')['event'].apply(list).to_dict()


nssac = [['3/4/20',10,54], ['3/5/20',18,98], ['3/6/20',37,125], ['3/7/20',70,168], ['3/8/20',84,197], ['3/9/20',98,234], ['3/10/20',108,265], ['3/11/20',121,308], ['3/12/20',148,308], ['3/13/20',158,3200], ['3/14/20',178,3303],
['3/15/20',196,5272], ['3/16/20',220,5493], ['3/17/20',380,7206], ['3/18/20',538,14597], ['3/19/20',798,22284],
['3/20/20',1091,32427], ['3/21/20',1387,45437], ['3/22/20',1873,61401], ['3/23/20',2894,78289],
['3/24/20',3891,91270], ['3/25/20',4691,103479], ['3/26/20',5944,122104], ['3/27/20',7187,145753],
['3/28/20',7875,155934], ['3/29/20',8519,172360], ['3/30/20',9326,186468], ['3/31/20',9967,205186],
['4/1/20',10683,220880], ['4/2/20',11567,238965], ['4/3/20',12351,260520], ['4/4/20',13081,283621], ['4/5/20',13723,302280],
['4/6/20',14294,320811]]

westchester = pd.DataFrame(nssac, columns=['date', 'cases', 'tests_ny'])
westchester['date'] = pd.to_datetime(westchester['date'])

grey = 'rgb(180, 180, 180)'
my_eve = collections.OrderedDict({
     pd.Timestamp('2020-03-16'): ['School closures', 0.46, -40, True, 'black'],
     pd.Timestamp('2020-03-16') + datetime.timedelta(days=7): ['One week after<br>school closures', 0.51, -50, False, grey],
     pd.Timestamp('2020-03-16') + datetime.timedelta(days=14): ['Two weeks after<br>school closures', 0.61, -50, False, grey],
     pd.Timestamp('2020-03-16') + datetime.timedelta(days=21): ['Three weeks after<br>school closures', 0.72, -50, False, grey],
     pd.Timestamp('2020-03-22'): ['Business closures and <br>a stay-at-home order', 0.69, 50, True, 'black'],
     pd.Timestamp('2020-03-22') + datetime.timedelta(days=7): ['One week after<br>business closures and <br>a stay-at-home order', 1.06, 60, False, grey],
     pd.Timestamp('2020-03-22') + datetime.timedelta(days=14): ['Two weeks after<br>business closures and <br>a stay-at-home order', 1.18, 85, False, grey],
#      pd.Timestamp('2020-03-16') + datetime.timedelta(days=14): ['2 weeks after Public and private school closure'],
#      pd.Timestamp('2020-03-22') + datetime.timedelta(days=14): ['2 weeks after Business closure', 'Lockdown']
})
state = "New York"
county = "Westchester"
min_date = nyt.loc[0, 'date']
max_date = nyt.loc[len(nyt) - 1, 'date']
counties = nyt[(nyt['state'] == state) & (nyt['date'] == max_date)].sort_values('cases', ascending=False).county
# for county in counties:
events = get_county_events(state, county)
count = 0
county_cases = nyt[(nyt['state'] == state) & (nyt["county"] == county)]
counties = nyt[(nyt['state'] == state)].county.unique()



navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Stanford | UVA", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://socialdistancing.stanford.edu/",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        #dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
)

app.layout = html.Div(children=[
	navbar,
	html.Br(),
	html.Br(),
    html.H1(
        children="Visualizing County-Level COVID-19 Interventions' Impact",
        style={
            'textAlign': 'center',
            #'color': colors['text']
        }
    ),
	dbc.Row([
		dbc.Col([
			dbc.Card(
				dbc.CardBody(
					[
					html.Label('State'),
					dcc.Dropdown(
						id='state',
						options=[dict(label=state, value=state) for state in states],
						value='Alabama'
					),

					html.Br(),

					html.Label('County'),
					dcc.Dropdown(
						id='county',
						options=[dict(label=county, value=county) for county in ['(All)', 'Westchester', 'Queens']],
						multi=True,
						value=['(All)']
					),

					]
				),
			)

		], width=2),
		dbc.Col([
			dbc.Card(
				dbc.CardBody(
					html.Div(id='plot-space')
			)
		)
		], width=10),
	], style=dict(margin=30))
])

@app.callback(
	[
		Output(component_id='plot-space', component_property='children'),
    ],
	[
		Input(component_id='state', component_property='value'),
		Input(component_id='county', component_property='value'),
	]
)
def update_output_div(state, counties):
	figs = []
	if state:
		if not counties:
			counties = ['Queens', 'Westchester']
		for county in counties:
			figs.append(go.Figure(
				data=[
					dict(
						x=westchester[westchester['date']>='2020-03-08']['date'],
						y=westchester[westchester['date']>='2020-03-08']['cases'],
						name='cases',
						mode='lines+markers',
						line=dict(width=2.5)),
				],
				layout=dict(
					hovermode='x',
					title="Total COVID-19 cases in <b>{county} County, {state}</b>".format(county=county, state=state),
					xaxis=dict(range=[min_date + datetime.timedelta(days=47) - datetime.timedelta(hours=18), max_date + datetime.timedelta(days=3)], showgrid=False),
					shapes=[
						dict(type='line', x0=pd.Timestamp('2020-03-15') - datetime.timedelta(weeks=1), x1=pd.Timestamp('2020-03-15') - datetime.timedelta(weeks=1), y0=0.75, y1=1, yref='y', line=dict(width=1)),
						dict(type='line', x0=pd.Timestamp('2020-03-15'), x1=pd.Timestamp('2020-03-15'), y0=0.75, y1=1, yref='y', line=dict(width=1)),
						dict(type='line', x0=pd.Timestamp('2020-03-15') + datetime.timedelta(weeks=1), x1=pd.Timestamp('2020-03-15') + datetime.timedelta(weeks=1), y0=0.75, y1=1, yref='y', line=dict(width=1)),
						dict(type='line', x0=pd.Timestamp('2020-03-15') + datetime.timedelta(weeks=2), x1=pd.Timestamp('2020-03-15') + datetime.timedelta(weeks=2), y0=0.75, y1=1, yref='y', line=dict(width=1)),
						dict(type='line', x0=pd.Timestamp('2020-03-15') + datetime.timedelta(weeks=3), x1=pd.Timestamp('2020-03-15') + datetime.timedelta(weeks=3), y0=0.75, y1=1, yref='y', line=dict(width=1)),
					] + [
						dict(type='line', x0=pd.Timestamp('2020-03-16') + datetime.timedelta(weeks=1), x1=pd.Timestamp('2020-03-16') + datetime.timedelta(weeks=1), y0=0.57, y1=0.67, yref='paper', line=dict(dash='dot', color=grey, width=1)),
						dict(type='line', x0=pd.Timestamp('2020-03-16') + datetime.timedelta(weeks=2), x1=pd.Timestamp('2020-03-16') + datetime.timedelta(weeks=2), y0=0.67, y1=0.77, yref='paper', line=dict(dash='dot', color=grey, width=1)),
						dict(type='line', x0=pd.Timestamp('2020-03-16') + datetime.timedelta(weeks=3), x1=pd.Timestamp('2020-03-16') + datetime.timedelta(weeks=3), y0=0.72, y1=0.80, yref='paper', line=dict(dash='dot', color=grey, width=1)),
						dict(type='line', x0=pd.Timestamp('2020-03-22') + datetime.timedelta(weeks=1), x1=pd.Timestamp('2020-03-22') + datetime.timedelta(weeks=1), y0=0.81, y1=0.90, yref='paper', line=dict(dash='dot', color=grey, width=1)),
						dict(type='line', x0=pd.Timestamp('2020-03-22') + datetime.timedelta(weeks=2), x1=pd.Timestamp('2020-03-22') + datetime.timedelta(weeks=2), y0=0.85, y1=1.025, yref='paper', line=dict(dash='dot', color=grey,  width=1)),
					],
					annotations=[
						dict(
							text=my_eve[date][0],
							x=date,
							y=my_eve[date][1],
							yref='paper',
							showarrow=my_eve[date][3],
							ax=0,
							ay=-my_eve[date][2],
							arrowwidth=1,
							font=dict(color=my_eve[date][4]))
						for date in my_eve
					],
					yaxis=dict(
						dtick=1,
						title='Total cases (log scale)',
						rangemode='normal',
						range=[-0.2,5.04],
						gridcolor='rgb(230, 230, 230)'
					),
					yaxis_type="log",
					paper_bgcolor='white',
					plot_bgcolor='white',
					template='plotly_white',
					height=600,
					font=dict(
						family="Roboto",
						size=16,
					)
				)
			))
	return [dcc.Graph(id='main-plot-{}'.format(i), figure=fig) for i, fig in enumerate(figs)],

if __name__ == '__main__':
    app.run_server(debug=True)
