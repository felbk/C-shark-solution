import gdown
import pandas as pd
from sklearn.model_selection import train_test_split
#from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
#from sklearn import tree
import pandas as pd
#import matplotlib.pyplot as plt

def trata_dados():

    data = {
        'bank': "1dzL_SWBkBs5xrUxuGQTm04oe3USgkL9u",    # banking data
        'sales': "1QK-VgSU3AxXUw330KjYFUj8S9hzKJsG6",   # sales data
        'mcc': "1JN0bR84sgZ_o4wjKPBUmz45NeEEkVgt7",     # mcc description
    }

    # Download all files from Google Drive
    for name, file_id in data.items():
        gdown.download(f'https://drive.google.com/uc?id={file_id}', name + '.parquet', quiet=False)

    # Read all files and store on a dictionary of pandas dataframes
    df = {}
    for name in data.keys():
        df[name] = pd.read_parquet(name + '.parquet')

    #Cria um subset com as vendas realizadas pelo mesmo 'document_id'

    sales = df['sales']
    subset_empresa = sales[sales['document_id'].astype('str').str.contains("453832840298988785")] 

    #Cria um subset com as vendas realizadas para um mesmo cliente ('card_number')

    subset_cliente = subset_empresa[subset_empresa['card_number'].astype('str').str.contains("8570859491088080896")]

    #Altera a coluna date_time para weekdays

    def weekday_conv(var):
        return var.strftime('%A')
    print(subset_cliente)
    subset_cliente.loc[:,"date_time"] = subset_cliente['date_time'].apply(weekday_conv)
    print(subset_cliente)

    #Filtra as colunas para o algoritmo de aprendizagem

    subset = subset_cliente.groupby('date_time')['value'].agg('mean')
    return 


def preve_valor():

    dados = trata_dados()
    return dados
'''
    df = pd.DataFrame(dados)

    # Converter os dias da semana para variáveis numéricas
    df['date_time'] = df['date_time'].astype('category').cat.codes

    x = df[['date_time']]
    y = df['valor']

    # Passo 2: Dividir os Dados em Treinamento e Teste
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=42)

    # Passo 3: Treinar o Modelo
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    # Passo 4: Fazer Previsões
    y_pred = model.predict(x_test)

    # Avaliar o Modelo
    mse = mean_squared_error(y_test, y_pred)
    print(f"Erro Quadrático Médio: {mse}")

    # Prever os valores para todos os dias da semana
    valores_previstos = model.predict(x)
    df['Valor_Previsto'] = valores_previstos

    return df
'''
print(preve_valor())

