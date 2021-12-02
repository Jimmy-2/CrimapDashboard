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

#---------------------------------------------------------------
#Taken from https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases
df = pd.read_csv("NYPD_Arrest_Data__Year_to_Date_.csv")

dff = df.groupby('ARREST_PRECINCT', as_index=False)[['PERP_SEX','PERP_RACE']].sum()
print (dff[:5])
pie = px.pie(df, names='PERP_SEX', )
pie.update_layout(paper_bgcolor="plum")

pie2 = px.pie(df, names='PERP_RACE')
pie2.update_layout(paper_bgcolor="powderblue")
fig = go.Figure()
#---------------------------------------------------------------
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
                    html.Div([
                        dcc.Dropdown(id='linedropdown',
                                     options=[
                                         {'label': 'Sex', 'value': 'PERP_SEX'},
                                         {'label': 'Race', 'value': 'PERP_RACE'}
                                     ],
                                     value='deaths',
                                     multi=False,
                                     clearable=False
                                     ),
                    ], className='six columns'),

                    html.Div([
                        dcc.Dropdown(id='piedropdown',
                                     options=[
                                         {'label': 'Sex', 'value': 'PERP_SEX'},
                                         {'label': 'Race', 'value': 'PERP_RACE'}
                                     ],
                                     value='cases',
                                     multi=False,
                                     clearable=False
                                     ),
                    ], className='six columns'),

                ], className='row'),

                html.Div([
                    html.Div([
                        dcc.Graph(id='linechart'),
                    ], className='six columns'),

                    html.Div([
                        dcc.Graph(id='piechart'),
                    ], className='six columns'),

                ], className='row'),
            ], style={
                'padding': '10px 5px'
            }),

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

#------------------------------------------------------------------
@app.callback(
    [Output('piechart', 'figure'),
     Output('linechart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def create_time_series(dff, axis_type, title):
    fig = px.bar(dff, x='ARREST_PRECINCT', y='PERP_SEX', color="PERP_SEX")

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10}, paper_bgcolor="rosybrown")

    return fig

def update_data(chosen_rows,piedropval,linedropval):
    if len(chosen_rows)==0:
        df_filterd = dff[dff['AGE_GROUP'].isin(['China','Iran','Spain','Italy'])]
    else:
        print(chosen_rows)
        df_filterd = dff[dff.index.isin(chosen_rows)]

    pie_chart=px.pie(
            data_frame=df_filterd,
            names='countriesAndTerritories',
            values=piedropval,
            hole=.3,
            labels={'countriesAndTerritories':'Countries'}
            )


    #extract list of chosen countries
    list_chosen_countries=df_filterd['countriesAndTerritories'].tolist()
    #filter original df according to chosen countries
    #because original df has all the complete dates
    df_line = df[df['countriesAndTerritories'].isin(list_chosen_countries)]

    line_chart = px.line(
            data_frame=df_line,
            x='ARREST_DATE',
            y=linedropval,
            color='countriesAndTerritories',
            labels={'countriesAndTerritories':'Countries', 'dateRep':'date'},
            )
    line_chart.update_layout(uirevision='foo')

    return (pie_chart,line_chart)

#------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
