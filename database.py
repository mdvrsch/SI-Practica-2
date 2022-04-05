import json
import sqlite3

with open('users.json') as file:
    data_users = json.load(file)

with open('legal.json') as file:
    data_legal = json.load(file)

with open('contrasenas.json') as file:
    data_contrasenas = json.load(file)

def sql_create_table(con):
    cursos_obj = con.cursor()

    # TABLA PARA USUARIOS
    cursos_obj.execute(
        "CREATE TABLE IF NOT EXISTS usuariosTable (nombre, telefono, contrasena, provincia, permisos, email_total, email_phishing, email_cliclados)")
    for usuarios in range(len(data_users['usuarios'])):
        for name in data_users['usuarios'][usuarios].keys():
            telefono = str(data_users['usuarios'][usuarios][name]['telefono'])
            contrasena = str(data_users['usuarios'][usuarios][name]['contrasena'])
            provincia = str(data_users['usuarios'][usuarios][name]['provincia'])
            permisos = str(data_users['usuarios'][usuarios][name]['permisos'])
            email_total = str(data_users['usuarios'][usuarios][name]['emails']['total'])
            email_phishing = str(data_users['usuarios'][usuarios][name]['emails']['phishing'])
            email_cliclados = str(data_users['usuarios'][usuarios][name]['emails']['cliclados'])
            cursos_obj.execute(
                "INSERT INTO usuariosTable (nombre, telefono, contrasena, provincia, permisos, email_total, email_phishing, email_cliclados) VALUES (?,?,?,?,?,?,?,?)",
                (name, telefono, contrasena, provincia, permisos, email_total, email_phishing, email_cliclados))
            con.commit()

    # TABLA PARA FECHAS
    cursos_obj.execute("CREATE TABLE IF NOT EXISTS fechasTable (nombre, fechas)")
    for usuarios in range(len(data_users['usuarios'])):
        for name in data_users['usuarios'][usuarios].keys():
            for fecha in data_users['usuarios'][usuarios][name]['fechas']:
                cursos_obj.execute("INSERT INTO fechasTable (nombre, fechas) VALUES (?,?)", (name, str(fecha),))
                con.commit()

    # TABLA PARA IPS
    cursos_obj.execute("CREATE TABLE IF NOT EXISTS ipsTable (nombre, ips)")
    for usuarios in range(len(data_users['usuarios'])):
        for name in data_users['usuarios'][usuarios].keys():
            for ip in data_users['usuarios'][usuarios][name]['ips']:
                cursos_obj.execute("INSERT INTO ipsTable (nombre, ips) VALUES (?,?)", (name, str(ip),))
                con.commit()

    # TABLA PARA LEGAL
    cursos_obj.execute("CREATE TABLE IF NOT EXISTS legalTable (nombre, cookies, aviso, proteccion, creacion)")
    for webs in range(len(data_legal['legal'])):
        for name in data_legal['legal'][webs].keys():
            cookies = str(data_legal['legal'][webs][name]['cookies'])
            aviso = str(data_legal['legal'][webs][name]['aviso'])
            proteccion = str(data_legal['legal'][webs][name]['proteccion_de_datos'])
            creacion = str(data_legal['legal'][webs][name]['creacion'])
            cursos_obj.execute(
                "INSERT INTO legalTable (nombre, cookies, aviso, proteccion, creacion) VALUES (?,?,?,?,?)",
                (name, cookies, aviso, proteccion, creacion))
            con.commit()

    # TABLA PARA CONTRASEÑAS
    cursos_obj.execute("CREATE TABLE IF NOT EXISTS contrasenaTable (nombre, contrasena, vulnerable)")
    for contra in range(len(data_contrasenas['contrasenas'])):
        for name in data_contrasenas['contrasenas'][contra].keys():
            contrasena = str(data_contrasenas['contrasenas'][contra][name]['contrasena'])
            vulnerable = str(data_contrasenas['contrasenas'][contra][name]['vulnerable'])
            cursos_obj.execute("INSERT INTO contrasenaTable (nombre, contrasena, vulnerable) VALUES (?,?,?)",
                               (name, contrasena, vulnerable))
            con.commit()


def sql_print(con):
    cursor_obj = con.cursor()
    cursor_obj.execute('SELECT * FROM usuariosTable')
    rows_user = cursor_obj.fetchall()
    for rowUser in rows_user:
        print(rowUser)

    cursor_obj.execute('SELECT * FROM fechasTable')
    rows_fecha = cursor_obj.fetchall()
    for rowFecha in rows_fecha:
        print(rowFecha)

    cursor_obj.execute('SELECT * FROM ipsTable')
    rows_ip = cursor_obj.fetchall()
    for rowIp in rows_ip:
        print(rowIp)

    cursor_obj.execute('SELECT * FROM legalTable')
    rows_legal = cursor_obj.fetchall()
    for rowLegal in rows_legal:
        print(rowLegal)

    cursor_obj.execute('SELECT * FROM contrasenaTable')
    rows_contra = cursor_obj.fetchall()
    for rowContra in rows_contra:
        print(rowContra)


def sql_delete_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("DROP TABLE IF EXISTS usuariosTable")
    con.commit()
    cursorObj.execute("DROP TABLE IF EXISTS fechasTable")
    con.commit()
    cursorObj.execute("DROP TABLE IF EXISTS ipsTable")
    con.commit()
    cursorObj.execute("DROP TABLE IF EXISTS legalTable")
    con.commit()
    cursorObj.execute("DROP TABLE IF EXISTS contrasenaTable")
    con.commit()


con = sqlite3.connect('database.db')
sql_create_table(con)
# sql_print(con)
# sql_delete_table(con)
con.close()
