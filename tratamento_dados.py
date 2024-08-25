import gdown
import random
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def trata_dados(document_id, client_id):

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
    subset_empresa = sales[sales['document_id'].astype('str').str.contains(document_id)] 

    #Cria um subset com as vendas realizadas para um mesmo cliente ('card_number')

    subset_cliente = subset_empresa[subset_empresa['card_number'].astype('str').str.contains(client_id)]

    #Altera a coluna date_time para weekdays

    def weekday_conv(var):
        return var.strftime('%A')
    print(subset_cliente)
    subset_cliente.loc[:,"date_time"] = subset_cliente['date_time'].apply(weekday_conv)
    print(subset_cliente)

    #Filtra apenas as colunas 'date_time' e 'value'
    subset = subset_cliente[['date_time', 'value']]

    return subset

#Data base para treino do gerador de cupom


Cupons = {'UpMean': [0.83, 0.52, 0.26, 0.53, 0.26, 0.05, 0.27, 0.76, 0.43, 0.39, 0.69, 0.76, 0.14, 0.19, 0.76, 0.36, 0.66, 0.79, 0.89, 0.07, 0.47, 0.39, 0.22, 0.96, 0.94, 0.23, 0.15, 0.87, 0.43, 0.66, 0.94, 0.14, 0.93, 0.88, 0.79, 0.54, 0.26, 0.31, 0.72, 0.07, 0.32, 0.79, 0.41, 0.81, 0.07, 0.6, 0.49, 0.82, 0.27, 0.45, 0.79, 0.23, 0.78, 0.99, 0.44, 0.48, 0.02, 0.37, 0.82, 0.22, 0.56, 0.49, 0.42, 0.01, 0.51, 0.56, 0.99, 0.87, 0.79, 0.78, 0.83, 0.95, 0.72, 0.29, 0.87, 0.3, 0.34, 0.84, 0.54, 0.97, 0.46, 0.77, 0.01, 0.76, 0.89, 0.53, 0.06, 0.1, 0.8, 0.04, 0.52, 0.65, 0.03, 0.96, 0.88, 0.64, 0.5, 0.08, 0.85, 0.41],
           
'OffPrice': [0.3, 0.47, 0.17, 0.03, 0.11, 0.42, 0.45, 0.33, 0.4, 0.49, 0.18, 0.3, 0.45, 0.47, 0.38, 0.36, 0.34, 0.06, 0.17, 0.16, 0.47, 0.48, 0.23, 0.23, 0.28, 0.31, 0.25, 0.25, 0.4, 0.15, 0.31, 0.36, 0.17, 0.21, 0.18, 0.18, 0.09, 0.25, 0.35, 0.43, 0.06, 0.36, 0.27, 0.22, 0.4, 0.07, 0.36, 0.38, 0.44, 0.37, 0.3, 0.3, 0.02, 0.25, 0.17, 0.45, 0.02, 0.02, 0.35, 0.36, 0.28, 0.11, 0.01, 0.34, 0.27, 0.1, 0.42, 0.12, 0.39, 0.33, 0.04, 0.12, 0.26, 0.43, 0.05, 0.16, 0.1, 0.33, 0.44, 0.15, 0.34, 0.12, 0.46, 0.09, 0.05, 0.47, 0.36, 0.11, 0.1, 0.35, 0.3, 0.09, 0.47, 0.07, 0.02, 0.18, 0.13, 0.15, 0.18, 0.16],
"Day" : ['Thursday', 'Friday', 'Monday', 'Monday', 'Sunday', 'Saturday', 'Tuesday', 'Wednesday', 'Sunday', 'Thursday', 'Thursday', 'Wednesday', 'Thursday', 'Wednesday', 'Friday', 'Saturday', 'Wednesday', 'Thursday', 'Wednesday', 'Friday', 'Saturday', 'Sunday', 'Sunday', 'Monday', 'Sunday', 'Tuesday', 'Monday', 'Monday', 'Monday', 'Thursday', 'Thursday', 'Wednesday', 'Sunday', 'Saturday', 'Tuesday', 'Thursday', 'Tuesday', 'Friday', 'Friday', 'Thursday', 'Tuesday', 'Monday', 'Saturday', 'Saturday', 'Sunday', 'Saturday', 'Wednesday', 'Monday', 'Sunday', 'Wednesday', 'Saturday', 'Thursday', 'Tuesday', 'Thursday', 'Sunday', 'Sunday', 'Monday', 'Tuesday', 'Sunday', 'Tuesday', 'Wednesday', 'Thursday', 'Wednesday', 'Friday', 'Sunday', 'Friday', 'Tuesday', 'Wednesday', 'Monday', 'Tuesday', 'Sunday', 'Thursday', 'Friday', 'Saturday', 'Friday', 'Monday', 'Saturday', 'Wednesday', 'Friday', 'Friday', 'Wednesday', 'Thursday', 'Monday', 'Thursday', 'Tuesday', 'Sunday', 'Thursday', 'Wednesday', 'Wednesday', 'Monday', 'Tuesday', 'Friday', 'Tuesday', 'Wednesday', 'Monday', 'Monday', 'Sunday', 'Thursday', 'Tuesday', 'Tuesday'],

 'Used': [True, True, False, False, 
False, False, True, True, False, True, False, True, True, True, False, True, True, True, False, False, True, False, True, False, True, False, False, True, True, True, True, False, True, True, True, False, False, True, True, False, True, True, False, True, False, False, True, True, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, True, False, True, False, False, False, True, False, True, False, True, True, False, False, True, True, True, True, False, True, False, True, 
False, False, True, True, False, False, False, True, True, True, True, False, False, False]}


def preve_valor(document_id, client_id):

    '''
    Dataset de teste usado durante o desenvolvimento // Remover ao término do projeto
    
    dados = {
        'date_time': ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'],
        'value': [200, 100, 300, 150, 100, 200, 100, 300, 150, 100, 120, 200, 100, 300, 150, 100, 120, 10, 200, 100, 300, 150, 100, 200, 100, 300, 150, 100, 120, 200, 100, 300, 150, 100, 120, 10, 200, 100, 300, 150, 100, 200, 100, 300, 150, 100, 120, 200, 100, 300, 150, 100, 120, 10, 200, 100, 300, 150, 100, 200, 100, 300, 150, 100, 120, 200, 100, 300, 150, 100, 120, 10]
    }
    '''
   
    dados = trata_dados(document_id, client_id)   
    
    df = pd.DataFrame(dados)
    
    # Pré-processamento
    df_encoded = pd.get_dummies(df, columns=['date_time'], drop_first=True)
    x = df_encoded.drop(columns=['value'])
    y = df_encoded['value']
    
    # Treinamento do modelo
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(x, y)
    
    # DataFrame para previsão
    df_predict = pd.DataFrame({
        'date_time': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    })
    
    # Pré-processamento para previsão
    df_predict_encoded = pd.get_dummies(df_predict, columns=['date_time'], drop_first=True)
    df_predict_encoded = df_predict_encoded.reindex(columns=x.columns, fill_value=0)
    
    # Previsões
    df_predict['value_previsto'] = rf_model.predict(df_predict_encoded)
    
    # Exibir resultados
    return df_predict

#Função para gerar cupom
def gera_cupom(df_pred):
    df_pred = pd.DataFrame(df_pred)
    #Dia com menor ticket médio = dia para usar cupom
    day = df_pred["date_time"][df_pred["value_previsto"].idxmin()]

    #Gerar UpMean e Offprice aleatorio e testar para ver se o cliente usaria com base no dict Cupons


document_id = "453832840298988785"
client_id = "8570859491088080896"
print(preve_valor(document_id, client_id))

