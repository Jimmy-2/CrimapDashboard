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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("NYPD_Arrest_Data__Year_to_Date_.csv")

available_indicators = df['PERP_SEX'].unique()

fig = go.Figure()
mean_age = df['ARREST_PRECINCT'].mean()
median_age = df['ARREST_PRECINCT'].median()
min_age = df['ARREST_PRECINCT'].min()
max_age = df['ARREST_PRECINCT'].max()

fig.add_trace(go.Indicator(
    value=mean_age,
    title={"text": "Mean age of all individuals shot from 2015 - 2019<br><span style='font-size:0.8em;color:gray'>"},
    domain={'x': [0, 0.5], 'y': [0, 0.5]},
    delta={'reference': 400, 'relative': True, 'position': "top"}))

fig.add_trace(go.Indicator(
    value=median_age,
    title={"text": "Median age of all individuals shot from 2015 - 2019<br><span style='font-size:0.8em;color:gray'>"},
    delta={'reference': 400, 'relative': True},
    domain={'x': [0, 0.5], 'y': [0.5, 1]}))

fig.add_trace(go.Indicator(
    value=max_age,
    title={"text": "Max age of all individuals shot from 2015 - 2019<br><span style='font-size:0.8em;color:gray'>"},
    domain={'x': [0.5, 1], 'y': [0.5, 1]},
    delta={'reference': 400, 'relative': True, 'position': "top"}))
fig.add_trace(go.Indicator(
    value=min_age,
    title={"text": "Min age of all individuals shot from 2015 - 2019<br><span style='font-size:0.8em;color:gray'>"},
    delta={'reference': 400, 'relative': True},
    domain={'x': [0.5, 1], 'y': [0, 0.5]}))
fig.update_layout(paper_bgcolor="palegoldenrod")

pie = px.pie(df, names='PERP_SEX', )
pie.update_layout(paper_bgcolor="plum")

pie2 = px.pie(df, names='PERP_RACE')
pie2.update_layout(paper_bgcolor="powderblue")

app.layout = html.Div([
    html.Div(
        children=[

            html.H1(
                children="NYPD Arrest Data (Year to Date)", className="header-title"
            ),

        ],
        className="header",
    ),

    dcc.Tabs([
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
                    html.P(children="Bar graph",

                           ),
                    dcc.Dropdown(
                        id='crossfilter-xaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='other'
                    ),

                    dcc.RadioItems(

                        id='crossfilter-xaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                    )
                ],
                    style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    html.P(children="Line Graph",

                           ),
                    dcc.Dropdown(
                        id='crossfilter-yaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='other'
                    ),

                    dcc.RadioItems(
                        id='crossfilter-yaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                    )
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
            ], style={
                'padding': '10px 5px'
            }),
            html.Div([
                dcc.Graph(id='x-time-series'),

            ], style={'display': 'inline-block', 'width': '49%'}),
            html.Div([
                dcc.Graph(id='y-time-series'),

            ], style={'display': 'inline-block', 'width': '49%'}),
            dcc.Graph(
                figure=fig,
                id='crossfilter-indicator-scatter',
                hoverData={'points': [{'customdata': 'shot'}]}

            )

        ]),
        dcc.Tab(

            label='Map', children=[


            ]),

    ]),

])


def create_time_series(dff, axis_type, title):
    fig = px.bar(dff, x='ARREST_PRECINCT', y='PERP_SEX', color="PERP_SEX")

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10}, paper_bgcolor="rosybrown")

    return fig


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Shooting.Manner'] == country_name]
    dff = dff[dff['PERP_RACE'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format('Age of Individuals Shot in Police Shootings by Race', xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Shooting.Manner'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['PERP_SEX'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)


if __name__ == '__main__':
    app.run_server(debug=True)
