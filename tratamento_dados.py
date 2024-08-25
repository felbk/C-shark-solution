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


Cupons = {'UpMean': [0.5,0.8,1],
           
'OffPrice': [0.2,0.1,0.3],
"Day" : ["Sunday","Saturday","Monday"],

 'Used': [True,False,True]}

Cupons = pd.DataFrame(Cupons)

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

translate = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

#Função para gerar cupom
def gera_cupom(df_pred):
    df_pred = pd.DataFrame(df_pred)
    #Dia com menor ticket médio = dia para usar cupom
    day = df_pred["date_time"][df_pred["value_previsto"].idxmin()]

    #Gerar opções de UpMean e Offprice aleatorias e testar para ver se o cliente usaria com base no dict Cupons
    test = {
        "UpMean":[],
        "OffPrice":[],
        "Day":[]
    }
    for i in range(200):
        test['Day'].append(day)
        test["UpMean"].append(random.randint(1,100)/100)
        test["OffPrice"].append(random.randint(1,50)/100)
    
    test = pd.DataFrame(test)

    
    # Pré-processamento
    df_encoded = pd.get_dummies(Cupons, columns=['Day'], drop_first=False)
    df_encoded.loc[:,['UpMean',"OffPrice"]] = Cupons[["UpMean","OffPrice"]]
    x = df_encoded.drop(columns=['Used'])
    y = df_encoded['Used']
    
    # Treinamento do modelo
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(x, y)
    
    # DataFrame para previsão
    df_predict = test
    
    # Pré-processamento para previsão
    df_predict_encoded = pd.get_dummies(df_predict, columns=['Day'], drop_first=False)
    df_predict_encoded = df_predict_encoded.reindex(columns=x.columns, fill_value=0)
    
    # Previsões
    df_predict['Used_Previsto'] = rf_model.predict(df_predict_encoded)
    
    Mean = df_pred["value_previsto"].min()
    UpMean = df_predict["UpMean"][df_predict["Used_Previsto"].idxmax()]
    OffPrice = df_predict["OffPrice"][df_predict["Used_Previsto"].idxmax()]
    Cupom = f"Cupom de R${(Mean*(1+UpMean)*OffPrice):.2f} em compras acima de R${(Mean*(1+UpMean)):.2f} para usar {translate[day]}!"
    # Exibir resultados
    print(df_predict)

    return Cupom
    


document_id = "453832840298988785"
client_id = "8570859491088080896"
print(gera_cupom(preve_valor(document_id, client_id)))

