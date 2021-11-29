import pandas as pd
import datetime as dt
import sqlalchemy
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import plotly.offline as py
from app import app
import psycopg2
from app import cores
import plotly.express as px

# Conexao com banco de dados Postgreesql
con = psycopg2.connect(
        host='ec2-54-173-138-144.compute-1.amazonaws.com',
        port='5432',
        database='d760mjbvtmnope',
        user='wfsbyjnowfdhuo',
        password='e59ec4f443436cb52396ff6721fb5c3033b1a3d8d82f75bd9d8264463aff9217'

    )
# Funcao que retorna dataframe do ultimo dado lido pelo sensor
def FormataDados(sql,con):
    df = pd.read_sql_query(sql, con=con)
    data = pd.to_datetime(df['Data_id'])
    data = data.dt.strftime('%d/%m %H:%M').tail(1)  # ultima data
    df_final = pd.concat([data, df['Pressao'].tail(1)], axis=1) # junta ultima data com pressão
    return df_final

# SQL querys para funcao FormataDados
sql_espinheiros = 'SELECT * FROM public. "SENSOR_JOINVILLE_ESPINHEIROS"'
sql_garuva = 'SELECT * FROM public."SENSOR_GARUVA1"'
sql_joinville_a = 'SELECT * FROM public."SENSOR_JOINVILLE_A"'

layout = html.Div([
    html.Br(),
    dcc.Graph(id = 'mapa',config={'displayModeBar': False, 'scrollZoom': True},
                style={'background':'#00FC87','padding-bottom':'2px','padding-left':'2px','height':'100vh'}),
    html.Br(),
    html.H5('COPYRIGHT © 2021 HYD – TODOS OS DIREITOS RESERVADOS.',style=
                            {'text-align':'center',
                             'color':cores['cinza-escuro'],
                             'font-size':10}),
    html.Br(),
    html.Br(),
    dcc.Interval(id='meu_intervalo',interval=1000*3600*24)

])

@app.callback(
    Output(component_id='mapa', component_property='figure'),
    Input(component_id='meu_intervalo', component_property='n_intervals')
)

def meu_mapa(n):


    lat_lon = pd.DataFrame([[-26.123068966191596, -48.85756589207343, 18],
                        [-26.256781, -48.852898, 18],
                        [-26.29128802525531, -48.77738213290111, 18]],
                       columns=['lat', 'lon', 'size']
                       )

    espinheiros = FormataDados(sql_espinheiros,con)
    garuva = FormataDados(sql_garuva,con)
    joinville_a = FormataDados(sql_joinville_a,con)

    df_mapa = pd.concat([garuva, joinville_a, espinheiros], axis=0).reset_index()
    df_mapa = pd.concat([df_mapa,lat_lon],axis=1)
    df_mapa['Leitura'] = df_mapa['Data_id']

    map = go.Figure(px.scatter_mapbox(
        df_mapa,
        lat = 'lat',
        lon = 'lon',
        hover_name = ['Sensor Garuva', 'Sensor Zona Industrial', 'Sensor Espinheiros'],
        size='size',
        hover_data = {'lat':False, 'lon':False, 'Leitura':True, 'Pressao':True, 'size':False}
                        ))

    map.update_layout(
            uirevision= 'foo', # preserva o estado da figura/mapa apos ativação do callback
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=10,
            mapbox=dict(
                accesstoken= 'pk.eyJ1IjoicGVwZW1hdHVyYW5hIiwiYSI6ImNrcmYxamV1ODVzMGEzMXBhODRjYm40YWMifQ.8T4DGGlv19yM6PqMtEpKLg',
                bearing=0,
                style='light',
                center=dict(
                    lat= -26.226430,
                    lon= -48.898974
                            ),
                pitch=40,
                zoom=10,
                        ),
            mapbox_style='open-street-map',
            title=dict(text="Geolocalização")
        )

    map.update_traces(
        marker_color = '#1EAFE3',
        hoverlabel_font_color = '#FFFFFF'
    )

    return map






