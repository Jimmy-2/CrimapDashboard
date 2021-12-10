#Name:  Jimmy Wu

#Email: Removed for github upload

#RESOURCES: Dataset: https://data.cityofnewyork.us/Public-Safety/NYPD-Arrest-Data-Year-to-Date-/uip8-fykc
#Dash HTML Guide: https://dash.plotly.com/dash-html-components
#'Plotly Histogram Guide: https://plotly.com/python/histograms/
#Map Guide: https://towardsdatascience.com/scatter-plots-on-maps-using-plotly-79f16aee17d0
#Heroku Guide: https://www.youtube.com/watch?v=b-M2KQ6_bM4

#URL: https://jimmy-testing.herokuapp.com/

#TITLE: Crimap Dashboard

import pandas as pd
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go


app = dash.Dash(__name__)
server = app.server

df = pd.read_csv("https://data.cityofnewyork.us/api/views/uip8-fykc/rows.csv?accessType=DOWNLOAD&bom=true&format=true")

dff = df.groupby('ARREST_PRECINCT', as_index=False)[['PERP_SEX','PERP_RACE']].sum()
print (dff[:5])
pie = px.pie(df, names='PERP_SEX', )
pie.update_layout(paper_bgcolor="plum")

pie2 = px.pie(df, names='PERP_RACE')
pie2.update_layout(paper_bgcolor="powderblue")
fig = go.Figure()
fig2 = px.histogram(df, x='PERP_RACE', nbins=20, color="PERP_RACE")
fig3 = px.histogram(df, x='PERP_SEX', nbins=20, color="PERP_SEX")

px.set_mapbox_access_token("pk.eyJ1IjoiZWNjaGlmdWNrZXIiLCJhIjoiY2t3endqbGhxMGtpeTJ2bXJqOGg2b2RkZiJ9.PzATagpmMHlKAM4KB6AO9A")
df['Description'] = ' '+ df['PERP_SEX'] + ', ' + df['PERP_RACE'] + ', ' + df['AGE_GROUP'] + ', ' + df['PD_DESC'].astype(str)
fig5 = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="ARREST_PRECINCT", text = "Description",)


app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
app.layout = html.Div([
    html.Div(
        children=[

            html.H1(
                children="Crimap Dashboard", className="header-title"
            ),
            html.Div(html.Img(src='/assets/arrestImage.jpg'), style={'display': 'inline-block', 'height': '200px'}),
            html.Div('NYPD Arrest Data (Year to Date)', style={'display': 'inline-block', 'height': '200px'})





        ],
        className="header",
    ),
    dcc.Tabs([
        dcc.Tab(

            label='Overview', children=[
                html.Div([

                    html.Div([
                        html.H6(children="Hypothesis"),
                        html.P('While creating visual representations of the arrests data, I have come to a conclusion that the people that get arrested are more likely to be male than female.'),

                    ],
                    style={'width': '49%', 'display': 'inline-block'}),
                    html.Div([
                        html.H6(children="Dataset Analysis"),
                        html.P('While I was able to easily create a scatterplot map with the latitude and longtitude columns, I was unable to easily create a non-histogram chart/graph due to the lack of columns with numerical data. The only columns with numerical data are area descriptions/locations.'),

                    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
                ]),
                html.Div([
                    html.Div([
                        html.H6(children="Techniques"),
                        html.P('The entire project is coded in Python DASH and deployed through heroku. The graphs, charts and map are created with the help of plotly.'),
                    ],
                        style={'width': '49%', 'display': 'inline-block'}),

                    html.Div([

                        html.H6(children="Citations"),
                        html.Label(['Dataset: ',  html.A('https://data.cityofnewyork.us/Public-Safety/NYPD-Arrest-Data-Year-to-Date-/uip8-fykc', href = 'https://data.cityofnewyork.us/Public-Safety/NYPD-Arrest-Data-Year-to-Date-/uip8-fykc')]),
                        html.Label(['Dash HTML Guide: ',  html.A('https://dash.plotly.com/dash-html-components', href = 'https://dash.plotly.com/dash-html-components')]),
                        html.Label(['Plotly Histogram Guide: ',  html.A('https://plotly.com/python/histograms/', href = 'https://plotly.com/python/histograms/')]),
                        html.Label(['Map Guide: ',  html.A('https://towardsdatascience.com/scatter-plots-on-maps-using-plotly-79f16aee17d0', href = 'https://towardsdatascience.com/scatter-plots-on-maps-using-plotly-79f16aee17d0')]),
                        html.Label(['Heroku Guide: ', html.A('https://www.youtube.com/watch?v=b-M2KQ6_bM4',  href='https://www.youtube.com/watch?v=b-M2KQ6_bM4')])
                    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})

                ]),

                html.Div([
                    html.Div([
                        html.H6(children="Code:"),
                        html.Label(['Github Link: ', html.A('https://github.com/Jimmy-2/CrimapDashboard', href = 'https://github.com/Jimmy-2/CrimapDashboard')])
                    ],
                        style={'width': '49%', 'display': 'inline-block'}),



                ]),

            ]),
        dcc.Tab(label='Graphs and Charts', children=[

            html.Div([
                html.Div([
                    dcc.Graph(figure=pie),
                ],
                    style={'width': '49%', 'display': 'inline-block'}),

                html.Div([

                    dcc.Graph(figure=pie2),
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})

            ]),
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig3)

                ],
                    style={'width': '49%', 'display': 'inline-block'}),

                html.Div([

                    dcc.Graph(figure=fig2)
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})

            ]),

            html.Div([
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    page_size=15
                ),

            ]),




        ]),
        dcc.Tab(

            label='Map', children=[
                html.Div([

                    dcc.Graph(figure=fig5),
                ],)
            ]),

    ]),




])


@app.callback(
    Output('graph1', 'figure'),
    [Input('dropdown1', 'value')]
)
# graph plot and styling
def update_graph(value):
    if value == 'cus':
        xx = ['North indian', 'chinese', 'continental', 'cafe', 'fast food', 'south indian', 'italian', 'desserts',
              'biryani', 'beverages']
        y1 = x1
        col = 'lightcoral'
    if value == 'dish':
        xx = ['pasta', 'burgers', 'cocktails', 'pizza', 'biryani', 'coffee', 'mocktails', 'sandwiches', 'paratha',
              'noodles']
        y1 = s1
        col = 'skyblue'
    return {'data': [go.Bar(
        x=xx,
        y=y1,
        marker_color=col),

    ],
        'layout': go.Layout(
            title='Top 10 cuisines',
            plot_bgcolor='#26332a',
            paper_bgcolor='#26332a',
            xaxis_tickangle=-17,

            xaxis=dict(
                # type='line',
                title='Most liked dish',
                showgrid=True,
                showline=True,
                color='white',
                linewidth=1,

            ),
            yaxis=dict(
                title='Count',
                showgrid=True,
                showline=True,
                gridcolor='#bdbdbd',
                color='white',
                linewidth=1
            ),
            margin={'l': 60, 'b': 40, 't': 30, 'r': 60},
            # legend={'x': 0.5, 'y': 1},
            hovermode='closest',

        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
