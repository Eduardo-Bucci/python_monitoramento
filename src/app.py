from flask import Flask, jsonify, render_template
import database.banco as banco
import datetime as dt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/status')
def status():

    resultado = banco.buscarUltimoValor()
    fluxo_dia = banco.carros_dia() or 0
    agora = dt.datetime.now()

    if not resultado:
        return jsonify({"status": "aguardando dados"})
    
    vagas_ocupadas: int = resultado["vaga_1"] + resultado["vaga_2"] + resultado["vaga_3"]
    vagas_livres: int = 3 - vagas_ocupadas
    porcentagem_vagas_o = round(vagas_ocupadas / 3 * 100, 1)

    hora_coleta = resultado["data_hora"]
    hora_coleta_py = dt.datetime.strptime(hora_coleta, "%Y-%m-%d %H:%M:%S")
    tempo_ultima_coleta = agora - hora_coleta_py


    vaga_1 = resultado["vaga_1"] = "Ocupada" if resultado["vaga_1"] == 1 else "Livre" 
    vaga_2 = resultado["vaga_2"] = "Ocupada" if resultado["vaga_2"] == 1 else "Livre" 
    vaga_3 = resultado["vaga_3"] = "Ocupada" if resultado["vaga_3"] == 1 else "Livre" 

    lotado = (vagas_ocupadas == 3)

    return jsonify({
        "vagas_livres": vagas_livres,
        "ultima_coleta": hora_coleta,
        "lotado": lotado,
        "vaga_1": vaga_1,
        "vaga_2": vaga_2,
        "vaga_3": vaga_3,
        "entrada_dia": fluxo_dia,
        "porcentagem_ocupado": porcentagem_vagas_o,
    })


@app.route('/historico')
def historico():

    resultado = banco.buscarUltimosValores(20)

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)