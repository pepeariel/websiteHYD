import pandas as pd
import datetime as dt
import sqlalchemy
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.express as px
import dash_bootstrap_components as dbc
from app import app
import plotly.graph_objects as go
import psycopg2

# Dicionário de cores para a página
cores = {'fundo':'#242A44',
         'branco':'#FFFFFF',
         'azul': '#1EAFE3',
         'azul_escuro': '#2F7BC1',
         'verde': '#69A753',
         'cinza': '#EEEEEE'
         }

# Layout da pagina
layout = dbc.Container([
    html.Br(),
    html.H3('Dashboard eficiência energética Eta Cubatão', style={'color':cores['azul']}),
    html.Br(),
    html.Div(dcc.DatePickerRange(id='calendario',
        min_date_allowed=dt.date(2020, 10, 1),
        max_date_allowed=dt.date.today(),
        initial_visible_month=dt.date.today(),
        end_date=dt.date.today(),
        display_format= 'DD/MM/YYYY',
        start_date_placeholder_text = 'Data início'
                        )),
    html.Br(),
    dbc.Row([
                dbc.Col([
                    dbc.Card(dcc.Graph(id = 'barras'),color= 'primary'),
                    html.Br(),
                    dbc.Card(dcc.Graph(id = 'linha2'),color='primary')]
                    ,lg={'size':8}),
                dbc.Col([

                    dbc.Card(dcc.Graph(id= 'veloc'),color='primary'),
                    html.Br(),
                    dbc.Card(dcc.Graph(id= 'KPI'),color='primary')


                             ],lg={'size':4})
            ]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id= 'boxplot'),color='primary'),lg={'size':4}),
        dbc.Col(dbc.Card(dcc.Graph(id='consumo'),color='primary'),lg={'size':4}),
        dbc.Col(dbc.Card(dcc.Graph(id= 'pie'),color='primary'),lg={'size':4})
                ]),
    html.Br(),
    dcc.Interval(id='meu_intervalo',interval=1000*3600*24)

],fluid=True, style={"height": "80vh"})

# Cria a interação entre usuário e dash (callback)
@app.callback(
    [
        Output(component_id='barras', component_property='figure'),
        Output(component_id='linha2',component_property='figure'),
        Output(component_id = 'boxplot', component_property='figure'),
        Output(component_id='consumo',component_property='figure'),
        Output(component_id='veloc', component_property='figure'),
        Output(component_id='KPI',component_property='figure'),
        Output(component_id='pie', component_property='figure')
    ],
    [
        Input(component_id='calendario',component_property='start_date'),
        Input(component_id='calendario',component_property='end_date'),
        Input(component_id='meu_intervalo',component_property='n_intervals')
    ]
                )

def meu_input(start_date,end_date,n_intervals):

    print(start_date)
    print(end_date)

    con = psycopg2.connect(
        host='ec2-54-173-138-144.compute-1.amazonaws.com',
        port='5432',
        database='d760mjbvtmnope',
        user='wfsbyjnowfdhuo',
        password='e59ec4f443436cb52396ff6721fb5c3033b1a3d8d82f75bd9d8264463aff9217'
    )
    db = pd.read_sql('SELECT * FROM public."COPIA_EFICIENCIA"', con)
    db['Rendimento'] = ((0.2725 * db['VD_ls'] * 3.6 * db['Pressao']) / (db['Consumo_Horario'] * 100))
    db['Total_bombas'] = db['B1']+db['B2']+db['B3']+db['B4']+db['B5']+db['B6']+db['B7']+db['B8']
    db['Custo_celesc'] = 0.391 * db['Consumo_Horario']
    df_indexado = db.copy()
    df_indexado.index = df_indexado['Data_id']

    if start_date and end_date is not None:


        dff = df_indexado.loc[start_date:end_date]
        pie = dff.iloc[:, 5:13]
        pie_values = pie.reset_index()
        pie_values = pie_values.iloc[1:, 1:]

        B1 = pie_values['B1'].mean()
        B2 = pie_values['B2'].mean()
        B3 = pie_values['B3'].mean()
        B4 = pie_values['B4'].mean()
        B5 = pie_values['B5'].mean()
        B6 = pie_values['B6'].mean()
        B7 = pie_values['B7'].mean()
        B8 = pie_values['B8'].mean()
        pie_columns = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']
        x = [B1, B2, B3, B4, B5, B6, B7, B8]



        fig1 = px.bar(dff,x='Data_id',y='VD_ls', title='Vazão de saída adutora')
        fig1.update_traces(marker_color='rgb(30,175,227)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=0.5, opacity=0.6)
        fig1.update_layout(
            plot_bgcolor=cores['branco'], # cor das linhas do grafico
            paper_bgcolor=cores['branco'], # Cor da moldura
            font_color = cores['azul']
        )

        figx = px.line(dff, x='Data_id', y='Rendimento', title='Eficiência motobombas')
        figx.update_traces(line_color='#1EAFE3')
        figx.update_layout(
            plot_bgcolor=cores['branco'],
            paper_bgcolor=cores['branco'],
            font_color=cores['azul']
        )

        fig2 = px.box(dff,x='Rendimento',title='Boxplot Rendimento')
        fig2.update_traces(marker_color='rgb(30,175,227)',
                           marker_line_color='rgb(8,48,107)',
                           marker_line_width=0.5, opacity=0.6)
        fig2.update_layout(
            plot_bgcolor=cores['branco'],
            paper_bgcolor=cores['branco'],
            font_color=cores['azul']
        )

        fig3 = px.line(dff, x='Data_id', y='Consumo_Horario', title='Consumo KHW', height=300)
        fig3.update_traces(line_color='#1EAFE3')
        fig3.update_layout(
            plot_bgcolor=cores['branco'],
            paper_bgcolor=cores['branco'],
            font_color=cores['azul']
        )

        fig4 = go.Figure(go.Indicator(
            mode="gauge+number",
            value= dff['Total_bombas'].mean(),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Bombas ligadas"},
            gauge={'bar': {'color': cores['azul']}}
        ))
        fig4.update_traces(
            title_font_size=25
        )
        fig4.update_layout(
            plot_bgcolor=cores['branco'],
            paper_bgcolor=cores['branco'],
            font_color=cores['azul']
        )

        fig5 = go.Figure(go.Indicator(
            mode="number+delta",
            value=dff['Custo_celesc'].sum(),
            number={'prefix': "$"},
            delta={'position': "top", 'reference': 100000},
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': 'Custo Celesc'}))
        fig5.update_traces(
            title_font_size=25
        )
        fig5.update_layout(
            paper_bgcolor=cores['branco'],
            font_color=cores['azul'])

        fig6 = go.Figure(data=[go.Pie(labels=pie_columns, values=x, hole=.3)],layout=go.Layout(height=300))
        fig6.update_layout(
            title_text='Resumo motobombas',
            title_font_color='#1EAFE3'
                            )
        fig6.update_traces(hoverinfo='label+percent',
                           textfont_size=15,
                           marker=dict(colors=['gold', 'mediumturquoise', 'darkorange', '#1EAFE3', 'lightcyan',
                                               'cyan', 'royalblue', 'darkblue'])
                            )

        return fig1,figx, fig2, fig3, fig4, fig5, fig6

    else:

        pie_columns = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']
        x = [1, 1, 1, 1, 1, 1, 1, 1]

        fig1 = px.bar(df_indexado, x='Data_id', y='VD_ls', title='Vazão saída adutora', height=250)
        fig1.update_layout(
            plot_bgcolor=cores['branco'],
            paper_bgcolor=cores['branco'],
            font_color=cores['azul']

        )

        figx = px.line(df_indexado, x ='Data_id', y ='Rendimento',title='Eficiência motobombas', height=250)
        figx.update_traces(line_color='#1EAFE3')
        figx.update_layout(
            plot_bgcolor=cores['branco'],
            paper_bgcolor=cores['branco'],
            font_color=cores['azul']
        )

        fig2 = px.box(df_indexado, x='Rendimento',title='BoxPlot Rendimento', height=300)
        fig2.update_traces(marker_color='rgb(30,175,227)', marker_line_color='rgb(8,48,107)',
                           marker_line_width=0.5, opacity=0.6)
        fig2.update_layout(
            plot_bgcolor=cores['branco'],
            paper_bgcolor=cores['branco'],
            font_color=cores['azul']
        )
        fig3 = px.line(df_indexado, x='Data_id', y='Consumo_Horario', title='Consumo KHW',height=300)
        fig3.update_traces(line_color='#1EAFE3')
        fig3.update_layout(
            plot_bgcolor=cores['branco'],
            paper_bgcolor=cores['branco'],
            font_color=cores['azul']
        )

        fig4 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=df_indexado['Total_bombas'].mean(),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Bombas ligadas"},
            gauge={'bar': {'color': cores['azul']}}
        ),layout=go.Layout(height=250))
        fig4.update_traces(
            title_font_size=25
        )
        fig4.update_layout(
            plot_bgcolor=cores['branco'],
            paper_bgcolor=cores['branco'],
            font_color=cores['azul']
        )

        fig5 = go.Figure(go.Indicator(
        mode = "number+delta",
        value = df_indexado['Custo_celesc'].sum(),
        number = {'prefix': "$"},
        delta = {'position': "top", 'reference': 100000},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title= {'text': 'Custo Celesc'}),layout=go.Layout(height=250))

        fig5.update_traces(
            title_font_size=25
        )

        fig5.update_layout(
            paper_bgcolor=cores['branco'],
            font_color=cores['azul'])

        fig6 = go.Figure(data=[go.Pie(labels=pie_columns, values=x,hole=.3)],layout=go.Layout(height=300))
        fig6.update_layout(
            title_text = 'Resumo motobombas',
            title_font_color = '#1EAFE3'
        )
        fig6.update_traces(hoverinfo='label+percent',
                           textfont_size=15,
                           marker=dict(colors= ['gold', 'mediumturquoise', 'darkorange', '#1EAFE3','lightcyan',
                                               'cyan','royalblue','darkblue']
                                               )
                           )


        return fig1,figx, fig2, fig3, fig4, fig5, fig6