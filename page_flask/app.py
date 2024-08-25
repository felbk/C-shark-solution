from flask import Flask, render_template, request
from GeraGrafico import gerarGraficos
from tratamento_dados import calcula_total , gera_cupom , get_subset_empresa
import pandas as pd

document_id= "453832840298988785"
dfTotal = pd.DataFrame(calcula_total(document_id))
x= ["Dom","Seg","Ter","Qua","Qui","Sex","Sab"]
y= dfTotal["sum"]
gerarGraficos("static\images\GraficoSemanal.png",x,y)


subset = pd.DataFrame(get_subset_empresa(document_id=document_id))
#gera cupons
cupons = {}
for i , notnone in enumerate(subset["card_number"]!=None):
    if notnone:
        client_id = subset["card_number"].iloc[i,:]
        cupons[client_id]=gera_cupom(document_id,client_id)
print (cupons)


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

