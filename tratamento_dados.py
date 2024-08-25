import gdown
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


document_id = "453832840298988785"
client_id = "8570859491088080896"
print(preve_valor(document_id, client_id))

