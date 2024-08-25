from flask import Flask, render_template, request
from GeraGrafico import gerarGraficos
from tratamento_dados import calcula_total , gera_cupom
import pandas as pd

document_id= "453832840298988785"
dfTotal = pd.DataFrame(calcula_total(document_id))
x= ["Dom","Seg","Ter","Qua","Qui","Sex","Sab"]
y= dfTotal["sum"]
gerarGraficos("static\images\GraficoSemanal.png",x,y)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    entrada = request.form['entrada']
    
    # Aqui você pode adicionar seu código Python para processar a entrada
    resultado = entrada[::-1]  # Exemplo simples: inverter o texto
    
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)

