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
        html.P(html.H3('Dashboard Zona Industrial Norte', style={'color':cores['azul'],'font-size':28})),
        dbc.Card(),
        html.Br(),
        html.H5('Selecione a data de análise:', style={'color':cores['preto'],'font-size':18}),
        html.Br(),
        dcc.DatePickerRange(id='calendario',
                                    min_date_allowed=dt.date(2021, 7, 21),
                                    max_date_allowed=dt.date.today(),
                                    initial_visible_month=dt.date.today(),
                                    end_date=dt.date.today(),
                                    display_format= 'DD/MM/YYYY',
                                    start_date_placeholder_text = 'Data início'
                                            ),
        html.Br(),
        html.Br(),
        html.H5('Baixe o arquivo:', style={'color':cores['preto'],'font-size':18}),
        html.Br(),
        dbc.Button('Download excel', id='joinville_excel',color='primary',outline=True),
                    ],lg={'size':4},style={'background-color':cores['branco']}),
    dbc.Col([
            html.Br(),
            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(id='velocimetro_joinville')),lg={'size':6}),
                dbc.Col(dbc.Card(dcc.Graph(id='pressao_joinville')),lg={'size':6})

                ]),
            html.Br(),
            dbc.Card(dcc.Graph(id = 'sensor_joinville_a')),
            html.Br(),

            ],lg={'size':8}),
            ]),
    html.Br(),
    html.Br(),
    dbc.Row(),
    dcc.Download(id='arquivo_joinville_excel'),
    # html.H6('COPYRIGHT © 2021 HYD - TODOS OS DIREITOS RESERVADOS',
    #         style={'text-align':'center','color':cores['azul'],'font-size':'10px'}),
    dcc.Interval(id='meu_intervalo',interval=1000*3600*24)


    ], fluid=True,style={'background-color':cores['cinza']})


@app.callback(
    [
        Output(component_id='velocimetro_joinville', component_property='figure'),
        Output(component_id='pressao_joinville',component_property='figure'),
        Output(component_id='sensor_joinville_a', component_property='figure')


     ],
    [
        Input(component_id='calendario',component_property='start_date'),
        Input(component_id='calendario',component_property='end_date'),
        Input(component_id='meu_intervalo', component_property='n_intervals')
    ]
            )

# Sempre que houver um INPUT é necessario declarar uma função com um parâmetro para cada INUPT
def meu_grafico(start_date, end_date, n_intervals):

    print(start_date)
    print(end_date)

    con = psycopg2.connect(
        host='ec2-54-173-138-144.compute-1.amazonaws.com',
        port='5432',
        database='d760mjbvtmnope',
        user='wfsbyjnowfdhuo',
        password='e59ec4f443436cb52396ff6721fb5c3033b1a3d8d82f75bd9d8264463aff9217'
                            )
    db_sensor_joinville_a = pd.read_sql('SELECT * FROM public."SENSOR_JOINVILLE_A"', con) # Conexão com a base dados do sensor de Joinville
    db_pressao_joinville_a = db_sensor_joinville_a.copy() # Cópia do dataframe por segurança
    db_pressao_joinville_a.index = db_pressao_joinville_a['Data_id'] # Coloca a coluna de data como index, para poder filtrar depois

# TITULO DO GRÁFICO DINÂMICO
    titulo = 'Gráfico em linha - Rua Balneário de Camboriú'

    if start_date and end_date is not None:

        dff2= db_pressao_joinville_a.loc[start_date:end_date,:]

        if len(dff2) > 0:
            return funcoes.dashboard(dff2, titulo)
        else:
            return funcoes.dashboard(db_pressao_joinville_a, titulo)
    else:
        return funcoes.dashboard(db_pressao_joinville_a, titulo)

@app.callback(
        Output(component_id='arquivo_joinville_excel',component_property='data'),
        Input(component_id='joinville_excel',component_property='n_clicks'),
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
        df_to_excel= pd.read_sql('SELECT * FROM public."SENSOR_JOINVILLE_A"', con)
        df_to_excel = df_to_excel[['Data_id','Pressao']]
        return dcc.send_data_frame(df_to_excel.to_excel, 'Pressao_Zona_Industrial.xlsx')

