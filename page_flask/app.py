from flask import Flask, render_template, request

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