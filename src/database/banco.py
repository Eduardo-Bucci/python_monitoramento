import sqlite3 as sql
import datetime

hoje = datetime.datetime.now().strftime("%Y-%m-%d")

def criarTabela():
    db = sql.connect("sensores.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS sensores (id INTEGER PRIMARY KEY AUTOINCREMENT, sensor_entrada INT NOT NULL, sensor_saida INT NOT NULL, vaga_1 INT NOT NULL, vaga_2 INT NOT NULL, vaga_3 INT NOT NULL, data_hora TEXT NOT NULL);")
    db.commit()
    db.close()

def inserirValores(sensor_entrada, sensor_saida, vaga_1, vaga_2, vaga_3):
    db = sql.connect("sensores.db")
    db.row_factory = sql.Row
    cursor = db.cursor()
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO sensores (sensor_entrada, sensor_saida, vaga_1, vaga_2, vaga_3, data_hora) VALUES (?, ?, ?, ?, ?, ?)", (sensor_entrada, sensor_saida, vaga_1, vaga_2, vaga_3, data_hora))
    db.commit()
    db.close()

def buscarValores():
    db = sql.connect("sensores.db")
    db.row_factory = sql.Row
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sensores")
    resultado = cursor.fetchall()
    db.close()
    return [dict(linha) for linha in resultado]

def buscarUltimoValor():
    db = sql.connect("sensores.db")
    db.row_factory = sql.Row
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sensores ORDER BY id DESC LIMIT 1")
    resultado = cursor.fetchone()
    db.close()
    return dict(resultado) if resultado else None

def buscarUltimosValores(n):
    db = sql.connect("sensores.db")
    db.row_factory = sql.Row
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sensores ORDER BY id DESC LIMIT ?", (n,))
    resultado = cursor.fetchall()
    db.close()
    return [dict(linha) for linha in resultado]

def carros_dia():
    db = sql.connect("sensores.db")
    db.row_factory = sql.Row
    cursor = db.cursor()
    cursor.execute("SELECT COALESCE(SUM(sensor_entrada), 0) AS total_dia FROM sensores WHERE data_hora LIKE ?", (f"{hoje}%",))
    resultado = cursor.fetchone()
    db.close()
    return resultado["total_dia"] if resultado["total_dia"] else None
