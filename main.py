import pandas as pd
from app import app
from app import cores
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output, State
import dash_bootstrap_components as dbc
import eficiencia_energetica
import gestao_perdas
import maps
import joinville
import espinheiros
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from chaves import host,port,database,user,password

server = app.server
db = SQLAlchemy(app.server)
app.config.suppress_callback_exceptions = True
server.config.update(
        SECRET_KEY= 'AJNSU8271872jjs_pp',
        SQLALCHEMY_DATABASE_URI=f"postgresql://{user}:{password}@{host }:{port}/{database}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
                    )

#Cria a classe de usuários
class Users(db.Model):
    __tablename__ = "CHAVES"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40))
    senha = db.Column(db.String(40))

    def __init__(self, id, login, senha):
        self.id = id
        self.login = login
        self.senha = senha

# Cria o LoginManager para o servidor (padrão do Flask)
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

class Users(UserMixin, Users):
    pass

# Página de login
login =  html.Div([
            dcc.Location(id='url_login', refresh=True),
            html.Br(),
            dbc.Row(
                [dbc.Col(),
                 dbc.Col(html.H4('''Bem-vindo!''', id='h1',style={'textAlign': 'center'})),
                 dbc.Col()]
            ),
            html.Br(),
            dbc.Row([
                dbc.Col(lg={'size':5}),
                dbc.Col(dbc.Input(placeholder='Usuário',
                        type='text',
                        id='uname-box',style={'textAlign': 'center'})
                        ,lg={'size':2}),
                dbc.Col(lg={'size':5})
                    ]),
            html.Br(),
            dbc.Row([
                 dbc.Col(lg={'size':5}),
                 dbc.Col(dbc.Input(placeholder='Senha',
                        type='password',
                        id='pwd-box',style={'textAlign': 'center'}),lg={'size':2}),
                 dbc.Col(lg={'size':5})
                 ]),
            html.Br(),
            dbc.Row([
                dbc.Col(lg={'size':5}),
                dbc.Col(dbc.Button(children='Acessar',
                    block= True,
                    n_clicks=0,
                    type='submit',
                    id='login-button',style={'textAlign': 'center'}),lg={'size':2}),
                dbc.Col(lg={'size':5})
                    ]),
            html.Div(children='', id='output-state')
        ])

# Página de retorno caso o input de usuario ou senha sejam inválidos
failed = html.Div([ dcc.Location(id='url_login_df', refresh=True),
            html.Div([
                    html.Br(),
                    html.Div([login]),
                    html.Br(),
                    dbc.Row([
                    dbc.Col(),
                    dbc.Col(dbc.Button(id='back-button', children='Voltar', n_clicks=0),style={'textAlign': 'center'}),
                    dbc.Col()])
                ])
        ])

pag_inicial = html.Div([
                    html.Br(),
                    html.Div(html.Img(id='S1', src=app.get_asset_url('intro.png'), width='80%',height='auto'),
                             style={'text-align': 'center',}),
                    html.Div(html.Img(id='s2', src=app.get_asset_url('s2.png'),width='80%',height='auto' ),
                             style={'text-align': 'center'}),
                    html.Div(html.Img(id='s3', src=app.get_asset_url('s3.png'), width='80%',height='auto'),
                             style={'text-align': 'center'}),
                    html.Div(html.Img(id='sensor', src=app.get_asset_url('s4.png'), width='80%',height='auto'),
                    style={'text-align': 'center'}),
                    html.Div(html.Img(id='s4', src=app.get_asset_url('s5.png'), width='80%',height='auto'),
                         style={'text-align': 'center'}),
                    html.Br(),
                    html.H5('COPYRIGHT © 2021 HYD – TODOS OS DIREITOS RESERVADOS.',style=
                            {'text-align':'center',
                             'color':cores['cinza-escuro'],
                             'font-size':10}),
                    html.Br()
                ])

# Callback para saber qual usuario esta ativo
@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return Users.query.get(int(user_id))

@app.callback(
    Output('url_login', 'pathname')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def successful(n_clicks, input1, input2):
    user = Users.query.filter_by(login=input1).first()
    if user:
        pwd = Users.query.filter_by(senha=input2).first()
        if pwd:
            login_user(user)
            return '/success'
        else:
            pass
    else:
        pass

@app.callback(
    Output('output-state', 'children')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        user = Users.query.filter_by(login=input1).first()
        if user:
            pwd = Users.query.filter_by(senha=input2).first()
            if pwd:
                return ''
            else:
                return html.Div([html.Br(),
                                 html.H6('Senha ou Usuário inválido',style={'text-align':'center'})])
        else:
            return html.Div([html.Br(),
                             html.H6('Senha ou Usuário inválido',style={'text-align':'center'})])
    else:
        return ''

nav_itens = dbc.NavbarSimple([
    dbc.NavItem(dbc.NavLink('Início', href='/Pagina-Inicial')),
    dbc.NavItem(dbc.NavLink('Eficiência',href='/Eficiencia-Energetica')),
    dbc.DropdownMenu([
                        dbc.DropdownMenuItem('Garuva', href= '/Gestao-Perdas'),
                        dbc.DropdownMenuItem('Zona Norte', href='/Joinville'),
                        dbc.DropdownMenuItem('Espinheiros', href='/Espinheiros')
                        ],label='Gestão Água',in_navbar=True,nav=True),
    dbc.NavItem(dbc.NavLink('Mapas',href='/Mapas')),
    dbc.NavItem(dbc.NavLink('Sair', href='/Logout'))
                    ],id='Navbarsimpletest',brand='hyd sensoriamento',color='primary',dark=True)

# Cria o estilo do dash em html
app.layout = html.Div(children=[
    nav_itens,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content', children=[])
    ])

@app.callback(
    Output(component_id='page_content', component_property='children'),
    Input(component_id='url',component_property='pathname')
)

def minha_pagina(pathname):

    if pathname == '/login':
        return login

    elif pathname == '/success':
        if current_user.is_authenticated:
            return pag_inicial
        else:
            return 'Erro 404! por favor volte a página inicial'

    elif pathname == '/Pagina-Inicial':
            return pag_inicial

    elif pathname == '/Eficiencia-Energetica':
        if current_user.is_authenticated:
            return eficiencia_energetica.layout
        else:
            return 'Acesso negado!', failed

    elif pathname == '/Gestao-Perdas':
        if current_user.is_authenticated:
            return gestao_perdas.layout
        else:
            return 'Acesso negado! ', failed

    elif pathname == '/Joinville':
        if current_user.is_authenticated:
            return joinville.layout
        else:
            return 'Acesso negado! ', failed

    elif pathname == '/Mapas':
        if current_user.is_authenticated:
            return maps.layout
        else:
            return 'Acesso negado!' , failed

    elif pathname == '/Logout':
        if current_user.is_authenticated:
            logout_user()
            return failed
        else:
            return login

    elif pathname == '/Espinheiros':
        if current_user.is_authenticated:
            return espinheiros.layout

    elif pathname == '/':
        return login

    else:
        return 'Erro 404! por favor volte a página inicial'

@app.callback(
    Output('url_login_df', 'pathname')
    , [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'

if __name__ == '__main__':
    app.run_server(debug=True)




