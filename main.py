#Name:  Jimmy Wu

#Email: jimmy.wu87@myhunter.cuny.edu

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

df = pd.read_csv("NYPD_Arrest_Data__Year_to_Date_.csv")


fig = go.Figure()


px.set_mapbox_access_token("pk.eyJ1IjoiZWNjaGlmdWNrZXIiLCJhIjoiY2t3endqbGhxMGtpeTJ2bXJqOGg2b2RkZiJ9.PzATagpmMHlKAM4KB6AO9A")
df['Description'] = ' '+ df['PERP_SEX'] + ', ' + df['PERP_RACE'] + ', ' + df['AGE_GROUP'] + ', ' + df['PD_DESC'].astype(str)
map = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="ARREST_PRECINCT", text = "Description",height = 1000)


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
                        html.H6(children="Purpose"),
                        html.P('The purpose of my project was to visualize the areas and locations that arrests occurred in and to do so, I had to choose a dataset that contained geographical or latitude and longitude data of arrests in NYC. '),

                    ],
                    style={'width': '49%', 'display': 'inline-block'}),
                    html.Div([
                        html.H6(children="Dataset Analysis"),
                        html.P('One major problem of my dataset was the lack of numerical data as the dataset was entirely of individual arrests and their specific descriptions/location of arrest. This meant that while I am able to create an extremely descriptive map of the individual arrests, I am unable to provide a descriptive visualization of a broader area of arrests. Since I was not provided with much numerical data, I could only make histograms and pie charts of the data provided.'),

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
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    page_size=15
                ),

            ]),
            html.Div([
                html.Div([

                    dcc.Dropdown(id='dropdown1',
                                 options=[
                                     {'label': 'Arrest Borough', 'value': 'ARREST_BORO'},
                                     {'label': 'Arrest Precinct', 'value': 'ARREST_PRECINCT'},
                                     {'label': 'PD Description', 'value': 'PD_DESC'},
                                     {'label': 'Offense Description', 'value': 'OFNS_DESC'},
                                     {'label': 'Age Group', 'value': 'AGE_GROUP'},
                                     {'label': 'Sex', 'value': 'PERP_SEX'},
                                     {'label': 'Race', 'value': 'PERP_RACE'}
                                 ],
                                 value='ARREST_BORO',
                                 disabled=False,
                                 multi=False,
                                 searchable=True,
                                 clearable=True,
                                 optionHeight=20,

                                 ),


                ]),
                dcc.Graph(id='pie1'),


            ]),
            html.Div([
                html.Div([
                    dcc.Dropdown(id='dropdown2',
                                 options=[
                                     {'label': 'Arrest Borough', 'value': 'ARREST_BORO'},
                                     {'label': 'Arrest Precinct', 'value': 'ARREST_PRECINCT'},
                                     {'label': 'Age Group', 'value': 'AGE_GROUP'},
                                     {'label': 'Sex', 'value': 'PERP_SEX'},
                                     {'label': 'Race', 'value': 'PERP_RACE'}
                                 ],
                                 value='ARREST_BORO',
                                 disabled=False,
                                 multi=False,
                                 searchable=True,
                                 clearable=True,
                                 optionHeight=20,

                                 ),



                ]),
                dcc.Graph(id='hist1'),



            ]),




        ]),
        dcc.Tab(

            label='Map', children=[
                html.Div([

                    dcc.Graph(figure=map),
                ],)
            ]),

    ]),




])

@app.callback(
    Output(component_id='pie1', component_property='figure'),
    [Input(component_id='dropdown1', component_property='value')]
)

def build_pie(column):
    dff=df
    fig = px.pie(dff,names=column)
    fig.update_layout(paper_bgcolor="powderblue")
    fig.update_traces(textinfo='percent+label')

    return fig

@app.callback(
    Output(component_id='hist1', component_property='figure'),
    [Input(component_id='dropdown2', component_property='value')]
)

def build_hist(column):
    dff=df
    fig = px.histogram(dff,x=column,color=column)
    fig.update_layout(paper_bgcolor="plum")


    return fig







if __name__ == '__main__':
    app.run_server(debug=True)
