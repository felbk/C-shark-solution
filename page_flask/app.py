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
clients= [ "1000164842220266112",'1000184940349350528','1000216457854768000','1000297234729290496','999604941954856320','999681003681560704','999688527568146048','999979815675401344','8570859491088080896']
for client_id in clients:
    client_id = str(client_id)
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

