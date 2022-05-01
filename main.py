from flask import Flask
from flask import render_template
from flask import request

import json
import plotly.graph_objects as go
import sqlite3
import pandas as pd
import requests

app = Flask(__name__)


def dataframe_contra(con):
    df_contra = pd.read_sql_query("SELECT * FROM contrasenaTable GROUP BY nombre", con)
    return df_contra


def dataframe_users(con):
    df_users = pd.read_sql_query(
        "SELECT nombre, email_phishing, email_cliclados FROM usuariosTable GROUP BY nombre", con)
    return df_users


def dataframe_desactualizadas(con):
    df_desactualizadas = pd.read_sql_query("SELECT nombre, cookies, aviso, proteccion FROM legalTable GROUP BY nombre",
                                           con)
    return df_desactualizadas


def dataframe_emails(con):
    df_emails = pd.read_sql_query(
        "SELECT * FROM usuariosTable GROUP BY nombre", con)
    return df_emails


@app.route('/index')
def index():
    return render_template('index.html')


# Ejercicio 2
@app.route('/ejercicio2/usuarios/criticos', methods=['GET', 'POST'])
def ejercicio2_usuariosCriticos():
    con = sqlite3.connect('database.db')
    df_contra = dataframe_contra(con)
    df_users = dataframe_users(con)

    x = 0
    if request.method == 'POST':
        # Then get the data from the form
        tag = request.form['tag']
        x = int(tag)

    # TOP X USUARIOS CRITICOS
    df_contra["vulnerable"] = df_contra["vulnerable"].astype(int)
    df_critico = df_contra.merge(df_users, on="nombre")
    df_contra_debil = df_critico[df_critico["vulnerable"] == 1]
    df_contra_debil["probabilidad"] = (df_contra_debil["email_cliclados"].astype(float) / df_contra_debil[
        "email_phishing"].astype(float)) * 100
    df_contra_debil = df_contra_debil.sort_values("probabilidad", ascending=False)
    df_contra_debil = df_contra_debil.head(n=x)
    df_contra_debil = df_contra_debil.drop(["vulnerable"], axis=1)

    fig = go.Figure(
        data=[go.Bar(x=df_contra_debil["nombre"], y=df_contra_debil["probabilidad"])])

    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON_user = json.dumps(fig, cls=a)
    return render_template('ejercicio2User.html', graphJSON_user=graphJSON_user)


@app.route('/ejercicio2/webs/vulnerables', methods=['GET', 'POST'])
def ejercicio2_websVulnerables():
    con = sqlite3.connect('database.db')
    df_desactualizadas = dataframe_desactualizadas(con)

    x = 0
    if request.method == 'POST':
        # Then get the data from the form
        tag = request.form['tag']
        x = int(tag)

    # TOP X DE PAGINAS WEBS VULNERABLES
    df_desactualizadas["cookies"] = df_desactualizadas["cookies"].astype(int)
    df_desactualizadas["aviso"] = df_desactualizadas["aviso"].astype(int)
    df_desactualizadas["proteccion"] = df_desactualizadas["proteccion"].astype(int)
    df_desactualizadas["desactualizadas"] = 3 - (df_desactualizadas[["cookies", "aviso", "proteccion"]].sum(axis=1))
    df_desactualizadas = df_desactualizadas.sort_values("desactualizadas", ascending=False)
    df_desactualizadas = df_desactualizadas.head(n=x)

    fig = go.Figure(
        data=[go.Bar(x=df_desactualizadas["nombre"], y=df_desactualizadas["desactualizadas"])])

    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON_webs = json.dumps(fig, cls=a)
    return render_template('ejercicio2Web.html', graphJSON_webs=graphJSON_webs)


# Ejercicio3
@app.route('/ejercicio3/info/menos50', methods=['GET', 'POST'])
def ejercicio3_menos50():
    con = sqlite3.connect('database.db')
    df_emails = dataframe_emails(con)

    x = 0
    if request.method == 'POST':
        # Then get the data from the form
        tag = request.form['tag']
        x = int(tag)

    df_emails["email_cliclados"] = df_emails["email_cliclados"].astype(float)
    df_emails["email_phishing"] = df_emails["email_phishing"].astype(float)
    df_emails["probabilidad"] = ((df_emails["email_cliclados"] / df_emails["email_phishing"]) * 100).astype(float)
    df_emails_menos = df_emails[df_emails["probabilidad"] < 50]
    df_emails_menos = df_emails_menos.sort_values("probabilidad", ascending=False)
    df_emails_menos = df_emails_menos.head(n=x)

    print(df_emails_menos)

    fig1 = go.Figure(
        data=[go.Bar(x=df_emails_menos["nombre"], y=df_emails_menos["probabilidad"])],
        layout_title_text="Usuarios que han cliclado menos del 50% de emails de spam"
    )

    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON_menos = json.dumps(fig1, cls=a)
    return render_template('ejercicio3menos50.html', graphJSON_menos=graphJSON_menos)


@app.route('/ejercicio3/info/mas50', methods=['GET', 'POST'])
def ejercicio3_mas50():
    con = sqlite3.connect('database.db')
    df_emails = dataframe_emails(con)

    x = 0
    if request.method == 'POST':
        # Then get the data from the form
        tag = request.form['tag']
        x = int(tag)

    df_emails["email_cliclados"] = df_emails["email_cliclados"].astype(float)
    df_emails["email_phishing"] = df_emails["email_phishing"].astype(float)
    df_emails["probabilidad"] = ((df_emails["email_cliclados"] / df_emails["email_phishing"]) * 100).astype(float)
    df_emails_mas = df_emails[df_emails["probabilidad"] >= 50]
    df_emails_mas = df_emails_mas.sort_values("probabilidad", ascending=False)
    df_emails_mas = df_emails_mas.head(n=x)

    fig2 = go.Figure(
        data=[go.Bar(x=df_emails_mas["nombre"], y=df_emails_mas["probabilidad"])],
        layout_title_text="Usuarios que han cliclado más del 50% de emails de spam"
    )

    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON_mas = json.dumps(fig2, cls=a)
    return render_template('ejercicio3mas50.html', graphJSON_mas=graphJSON_mas)


# Ejercicio 4
@app.route('/ejercicio4')
def ejercicio4_vul():
    response = requests.get("https://cve.circl.lu/api/last")

    json_info = response.text
    df_vul = pd.DataFrame()
    df_vul["id"] = pd.read_json(json_info)["id"]
    df_vul["last-modified"] = pd.read_json(json_info)["last-modified"]

    fig = go.Figure(
        data=[go.Line(x=df_vul["id"].head(n=10), y=df_vul["last-modified"].head(n=10))],
        layout_title_text="Últimas 10 vulnerabilidades en tiempo real"
    )

    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON_vul = json.dumps(fig, cls=a)
    return render_template('ejercicio4.html', graphJSON_vul=graphJSON_vul)


if __name__ == '__main__':
    app.run(debug=True)
