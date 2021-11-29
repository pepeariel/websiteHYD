# useful functions
import plotly.graph_objects as go
import plotly.express as px
from app import cores
import pandas as pd


def arrumadb (db, value, titulo):
    if value == 'minima':
        pressao_atual = db['Pressao'].min()
        db['linha'] = pressao_atual
        return dashboard(db, titulo)

    elif value == 'maxima':
        pressao_atual = db['Pressao'].max()
        db['linha'] = pressao_atual
        return dashboard(db, titulo)

    elif value == 'mediana':
        pressao_atual = db['Pressao'].median()
        db['linha'] = pressao_atual
        return dashboard(db, titulo)

    else:
        value = 'media'
        pressao_atual = db['Pressao'].mean()
        db['linha'] = pressao_atual
        return dashboard(db, titulo)

def dashboard (db, titulo):
    try:
        value = float(db['Pressao'].tail(1).round(1).values)
        if value < 10:
            cor_do_indicador ='#F33112  '
        elif value >= 10 and value <= 15:
            cor_do_indicador = '#FFC300'
        else:
            cor_do_indicador = '#69A753'

        fig1 = px.line(db, x='Data_id', y='Pressao',
                       title=f'{titulo}', height=300)
        fig1.update_traces(line_color='#1EAFE3', hoverlabel_font_color='#FFFFFF')
        fig1.add_scatter(x=db['Data_id'], y=db['linha'],showlegend=False,line=dict(color="#DCDCDC"))
        fig1.update_layout(
            plot_bgcolor=cores['branco'],  # Cor das linhas do grafico
            paper_bgcolor=cores['branco'],  # Cor da moldura
            font_color=cores['azul'],
            xaxis_title="Data",
            yaxis_title="Pressão [mca]",
        )

        db['Data_id'] = pd.to_datetime(db['Data_id'])
        db['Mes'] = db['Data_id'].dt.month_name()
        df = db.groupby(['Mes'])['Pressao'].mean().round(0)
        df = pd.DataFrame(df)
        pressao = px.bar(x=df.index, y=df['Pressao'],title='Pressão Média Mensal',height=300)
        pressao.update_traces(marker_color='rgb(30,175,227)', marker_line_color='#FFFFFF',
                           marker_line_width=0.5, opacity=0.6, texttemplate='%{y}', textposition='inside',textfont_color='#FFFFFF')
        pressao.update_layout(
            plot_bgcolor=cores['branco'],  # cor das linhas do grafico
            paper_bgcolor=cores['branco'],  # Cor da moldura
            font_color=cores['azul'],
            xaxis_title="Mês",
            yaxis_title="Pressão [mca]",
        )

        indicador = go.Figure(go.Indicator(
            mode="gauge+number",
            value= value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Pressão Atual"},
            gauge= {'bar': {'color': cor_do_indicador}}
        ),layout=go.Layout(height=300))
        indicador.update_traces(
            title_font_size=22,
            title_font_color=cor_do_indicador
        )
        indicador.update_layout(
            plot_bgcolor=cores['branco'],
            paper_bgcolor=cores['branco'],
            font_color=cor_do_indicador
        )

        return fig1, pressao, indicador

    except:
        return ['Erro' for i in range(3)]


#######################################################################################
# ESSA FUNÇÃO AINDA NÃO FOI IMPLEMENTADA!#
#######################################################################################
def indicadores_diversos():
    pie_columns = ['Reais', 'Aparentes']
    x = [7, 3]

    fnd = go.Figure(go.Indicator(
        mode="number",
        value=13.6,
        title='FND',
        domain={'x': [0, 1], 'y': [0, 1]},
    ), layout=go.Layout(height=150))
    fnd.update_traces(
        title_font_size=25,
        number_font_size=40
    )
    fnd.update_layout(
        paper_bgcolor=cores['azul'],
        font_color=cores['branco'])

    perda = go.Figure(go.Indicator(
        mode="number",
        value=197.8,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': 'Vazão vazamentos'}), layout=go.Layout(height=150))

    perda.update_traces(
        title_font_size=25,
        number_font_size=40,
        number_suffix=' l/lig'
    )
    perda.update_layout(
        paper_bgcolor=cores['branco'],
        font_color=cores['azul'])

    pressao = go.Figure(go.Indicator(
        mode="number",
        value=pressao_media,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': 'Pressão média'}), layout=go.Layout(height=150))
    pressao.update_traces(
        title_font_size=25,
        number_font_size=40,
        number_suffix=' mca'
    )
    pressao.update_layout(
        paper_bgcolor=cores['branco'],
        font_color=cores['azul'])

    fig1 = px.line(db_pressao_garuva, x='Data_id', y='Pressao',
                   title='Gráfico de pressão em linha - Estrada das palmeiras', height=300)
    fig1.update_traces(line_color='#1EAFE3')
    fig1.update_layout(
        plot_bgcolor=cores['branco'],  # Cor das linhas do grafico
        paper_bgcolor=cores['branco'],  # Cor da moldura
        font_color=cores['azul'])

    fig2 = go.Figure(data=[go.Pie(labels=pie_columns, values=x)], layout=go.Layout(height=300))
    fig2.update_layout(
        title_text='Distribuição perdas',
        title_font_color='#1EAFE3'
    )
    fig2.update_traces(hoverinfo='label+percent',
                       textfont_size=15,
                       marker=dict(colors=['lightcyan', 'cyan']
                                   ))

    return fnd, perda, pressao, fig1, fig2  # sempre retornar o mesmo numero de OTPUTS na ordem exata

