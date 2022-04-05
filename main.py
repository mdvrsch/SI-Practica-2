from flask import Flask
from flask import render_template
from flask import request

import json
import plotly.graph_objects as go
import sqlite3
import pandas as pd


app = Flask(__name__)

def dataframe_contra(con):
    df_contra = pd.read_sql_query("SELECT * FROM contrasenaTable GROUP BY nombre", con)
    return df_contra

def dataframe_users(con):
    df_users = pd.read_sql_query(
        "SELECT nombre, email_phishing, email_cliclados FROM usuariosTable GROUP BY nombre",con)
    return df_users

def dataframe_desactualizadas(con):
    df_desactualizadas = pd.read_sql_query("SELECT nombre, cookies, aviso, proteccion FROM legalTable GROUP BY nombre",con)
    return df_desactualizadas

@app.route('/index')
def index():
   return render_template('index.html')


@app.route('/ejercicio2/usuarios/criticos')
def ejercicio2_usuariosCriticos():
    con = sqlite3.connect('database.db')

    df_contra = dataframe_contra(con)
    df_users = dataframe_users(con)

    # TOP X USUARIOS CRITICOS
    df_contra["vulnerable"] = df_contra["vulnerable"].astype(int)
    df_critico = df_contra.merge(df_users, on="nombre")
    df_contra_debil = df_critico[df_critico["vulnerable"] == 1]
    df_contra_debil["probabilidad"] = (df_contra_debil["email_cliclados"].astype(float) / df_contra_debil["email_phishing"].astype(float)) * 100
    df_contra_debil = df_contra_debil.sort_values("probabilidad", ascending=False)
    df_contra_debil = df_contra_debil.head(n=10)
    df_contra_debil = df_contra_debil.drop(["vulnerable"], axis=1)

    fig = go.Figure(
        data=[go.Bar(x=df_contra_debil["nombre"],y=df_contra_debil["probabilidad"])],
        layout_title_text="Gráfica resultante"
    )

    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON_user = json.dumps(fig, cls=a)
    return render_template('ejercicio2User.html', graphJSON_user=graphJSON_user)


@app.route('/ejercicio2/webs/vulnerables')
def ejercicio2_websVulnerables():
    con = sqlite3.connect('database.db')

    df_desactualizadas = dataframe_desactualizadas(con)

    # TOP X DE PAGINAS WEBS VULNERABLES
    df_desactualizadas["cookies"] = df_desactualizadas["cookies"].astype(int)
    df_desactualizadas["aviso"] = df_desactualizadas["aviso"].astype(int)
    df_desactualizadas["proteccion"] = df_desactualizadas["proteccion"].astype(int)
    df_desactualizadas["desactualizadas"] = 3 - (df_desactualizadas[["cookies", "aviso", "proteccion"]].sum(axis=1))
    df_desactualizadas = df_desactualizadas.sort_values("desactualizadas", ascending=False)
    df_desactualizadas = df_desactualizadas.head(n=5)
    df_desactualizadas = df_desactualizadas.drop(["desactualizadas"], axis=1)

    fig = go.Figure(
        data=[go.Bar(x=df_desactualizadas["nombre"])],
        layout_title_text="Gráfica resultante"
    )

    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON_webs = json.dumps(fig, cls=a)
    return render_template('ejercicio2Web.html', graphJSON_webs=graphJSON_webs)

if __name__ == '__main__':
   app.run(debug=True)