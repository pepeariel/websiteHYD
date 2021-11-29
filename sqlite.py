import sqlite3
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import *
import psycopg2


con = psycopg2.connect(
host = 'ec2-54-173-138-144.compute-1.amazonaws.com',
port = '5432',
database = 'd760mjbvtmnope',
user = 'wfsbyjnowfdhuo',
password = 'e59ec4f443436cb52396ff6721fb5c3033b1a3d8d82f75bd9d8264463aff9217'
)
cur = con.cursor()
query = 'INSERT INTO public. "SENSOR_JOINVILLE_ESPINHEIROS" ("Data_id", "Pressao")' \
         'VALUES (%s, %s) '
sql = ("2021-11-24 12:07:15 ",18.187)
cur.execute('SELECT * FROM public."SENSOR_JOINVILLE_ESPINHEIROS"')
print('escrevendo no postgree..')
# cur.execute(query,sql)
# con.commit()
print('dados enviados com sucesso')

df= pd.read_sql('SELECT * FROM public."SENSOR_JOINVILLE_ESPINHEIROS"', con)
print(df.tail())


# conn = sqlite3.connect('data.sqlite')
# c = conn.cursor()
#
# # #conexão a base sqlite3
# engine = create_engine('sqlite:///data.sqlite')
# db = SQLAlchemy()



#class for the tables creation

# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     login = db.Column(db.String(15), unique=True, nullable = False)
#     senha = db.Column(db.String(80))

# class Eficiencia(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Data_id = db.Column(db.Text)
#     Consumo_Horario = db.Column(db.Float)
#     Vd_ls = db.Column(db.Float)
#     Pressao = db.Column(db.Float)
#     B1 = db.Column(db.Float)


# Eficiencia_tbl = Table('Eficiencia', Eficiencia.metadata)
# #fuction to create table using Users class
# def create_Eficiencia_table():
#     Eficiencia.metadata.create_all(engine)
# #create the table
# create_Eficiencia_table()


################################################## MOSTRA A TABELA users DO SQLITE3
# df = pd.read_sql('select * from users', conn)
#
# print(df)


################################################# INSERE DADOS NA TABLEA users
# query = ''' INSERT INTO users(login,senha)
#              VALUES(?,?) '''
# sql = ('Garuva', 'Projeto_garuva2021')
# c.execute(query,sql)
# conn.commit()





################################################## METODO ALTERNATIVO AUTENTICAÇÃO USUARIOS
# # Connecta ao sqlite3, banco data
# conn = sqlite3.connect('data.sqlite')
# engine = create_engine('sqlite:///data.sqlite')
# db = SQLAlchemy() # seta a database
# config = configparser.ConfigParser()

# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     login = db.Column(db.String(15), unique=True, nullable = False)
#     senha = db.Column(db.String(80))
# Users_tbl = Table('users', Users.metadata)

# Inicia o app do Dash



#Cria a interação entre o servidor e o banco sqlite
#Secret Key é usada para iniciar a sessão (pode ser qualquer coisa)
# server.config.update(
#     SECRET_KEY= 'AJNSU8271872jjs_pp',
#     SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite',
#     SQLALCHEMY_TRACK_MODIFICATIONS=False
# )
# db.init_app(server)