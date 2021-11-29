import pandas as pd
import datetime as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc
from app import app
from app import cores
import psycopg2
import funcoes

layout = dbc.Container([dbc.Row([
    dbc.Col([
        html.Br(),
        html.P(html.H3('Dashboard Espinheiros', style={'color':cores['azul'],'font-size':28})),
        dbc.Card(),
        html.Br(),
        html.H5('Selecione a data de análise:', style={'color':cores['preto'],'font-size':18}),
        html.Br(),
        dcc.DatePickerRange(id='calendario',
                                    min_date_allowed=dt.date(2021, 8, 23),
                                    max_date_allowed=dt.date.today(),
                                    initial_visible_month=dt.date.today(),
                                    end_date=dt.date.today(),
                                    display_format= 'DD/MM/YYYY',
                                    start_date_placeholder_text = 'Data início'
                                    ),
        html.Br(),
        html.Br(),
        html.H5('Selecione o tipo de pressão:', style={'color':cores['preto'],'font-size':18}),
        html.Br(),
        dcc.Dropdown(id= 'pressao_espinheiros_tipo',
                             options=[
                                {'label': ' Mínima ', 'value': 'minima'},
                                {'label': ' Média ', 'value': 'media'},
                                {'label': ' Máxima ', 'value': 'maxima'},
                                {'label': ' Mediana ', 'value': 'mediana'}
                                    ],
                             placeholder= 'Pressão média',
                             style={'width':'80%'}
                                ),
        html.Br(),
        html.H5('Baixe o arquivo:', style={'color':cores['preto'],'font-size':18}),
        html.Br(),
        dbc.Button('Download excel', id='espinheiros_excel',color='primary',outline=True),
                ],lg={'size':4}),
    dbc.Col([
            html.Br(),
            dbc.Card(dcc.Graph(id = 'sensor_espinheiros')),
            html.Br(),
            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(id='pie_espinheiros')),lg={'size':6}),
                dbc.Col(dbc.Card(dcc.Graph(id='velocimetro_espinheiros')),lg={'size':6})
                ])
            ],lg={'size':8})
            ]),
    html.Br(),
    html.Br(),
    dbc.Row(),
    dcc.Download(id='arquivo_espinheiros_excel'),
    # html.H6('COPYRIGHT © 2021 HYD - TODOS OS DIREITOS RESERVADOS',
    #         style={'text-align':'center','color':cores['azul'],'font-size':'10px'}),
    dcc.Interval(id='meu_intervalo',interval=1000*3600*24)

], fluid=True,style={'background-color':cores['cinza']})

@app.callback(
    [
        Output(component_id='sensor_espinheiros', component_property='figure'),
        Output(component_id='pie_espinheiros',component_property='figure'),
        Output(component_id='velocimetro_espinheiros', component_property='figure')
     ],
    [
        Input(component_id='calendario',component_property='start_date'),
        Input(component_id='calendario',component_property='end_date'),
        Input(component_id='pressao_espinheiros_tipo',component_property='value'),
        Input(component_id='meu_intervalo',component_property='n_intervals')
    ]
            )

# Sempre que houver um INPUT é necessario declarar uma função com um parâmetro para cada INUPT
def meu_grafico(start_date, end_date, value, n_intervals):

    print(start_date)
    print(end_date)

    con = psycopg2.connect(
        host='ec2-54-173-138-144.compute-1.amazonaws.com',
        port='5432',
        database='d760mjbvtmnope',
        user='wfsbyjnowfdhuo',
        password='e59ec4f443436cb52396ff6721fb5c3033b1a3d8d82f75bd9d8264463aff9217'
                            )
    db_sensor_espinheiros = pd.read_sql('SELECT * FROM public."SENSOR_JOINVILLE_ESPINHEIROS"', con) # Conexão com a base dados do sensor de Joinville
    db_pressao_espinheiros= db_sensor_espinheiros.copy() # Cópia do dataframe por segurança
    db_pressao_espinheiros.index = db_sensor_espinheiros['Data_id'] # Coloca a coluna de data como index, para poder filtrar depois

# TITULO DO GRÁFICO DINÂMICO
    titulo = 'Gráfico de pressão em linha - Rua Antônio Gonçalves, 262'

    if start_date and end_date is not None:

        dff2= db_pressao_espinheiros.loc[start_date:end_date,:]

        if len(dff2) > 0:
            return funcoes.arrumadb(dff2, value, titulo)
        else:
            return funcoes.arrumadb(db_pressao_espinheiros, value, titulo)
    else:
        return funcoes.arrumadb(db_pressao_espinheiros, value, titulo)

@app.callback(
        Output(component_id='arquivo_espinheiros_excel',component_property='data'),
        Input(component_id='espinheiros_excel',component_property='n_clicks'),
        prevent_initial_call=True
            )

def meu_arquivo(n_clicks):
    if n_clicks > 0:
        con = psycopg2.connect(
            host='ec2-54-173-138-144.compute-1.amazonaws.com',
            port='5432',
            database='d760mjbvtmnope',
            user='wfsbyjnowfdhuo',
            password='e59ec4f443436cb52396ff6721fb5c3033b1a3d8d82f75bd9d8264463aff9217'
        )
        df_to_excel= pd.read_sql('SELECT * FROM public."SENSOR_JOINVILLE_ESPINHEIROS"', con)
        df_to_excel = df_to_excel[['Data_id','Pressao']]
        return dcc.send_data_frame(df_to_excel.to_excel, 'Pressao_Espinheiros.xlsx')