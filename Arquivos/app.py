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
cupons = []


clients= ["8570859491088080896","3937011235745296896","4968104925029793792","4053289940888395776"]*5
for client_id in clients:
    cupons.append(gera_cupom(document_id,client_id))
print (cupons)
print(f"foram gerados {len(cupons)} cupons")


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',numCupons=len(cupons),CupomText=cupons[3]["cupomText"])

@app.route('/processar', methods=['POST'])
def processar():
    entrada = request.form['entrada']
    
    # Aqui você pode adicionar seu código Python para processar a entrada
    resultado = entrada[::-1]  # Exemplo simples: inverter o texto
    
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)

