import dash_bootstrap_components as dbc
from dash import Dash

app = Dash(__name__, external_stylesheets = [dbc.themes.CERULEAN],
                    suppress_callback_exceptions=True,
                    meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

cores = {'fundo':'#242A44',
         'branco':'#FFFFFF',
         'azul': '#1EAFE3',
         'azul_escuro': '#2F7BC1',
         'verde': '#69A753',
         'cinza': '#fafafa',
         'preto': '#000000',
         'cinza-escuro': '#DCDCDC',
         'azul-marinho':'#99AEBB'
         }