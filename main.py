import dload
import pandas as pd
import json
import os, csv
import numpy as np

#dload.save_unzip("https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip")

dirpath = os.getcwd()
raw_data = dirpath + "\jodi_gas_csv_beta\jodi_gas_beta.csv"

#criar uma coluna com o id chamado serie_id

df = pd.read_csv(raw_data)
df['series_id'] = df['REF_AREA'] + '-' + df['ENERGY_PRODUCT'] + '-' +  df['FLOW_BREAKDOWN']  + '-' +  df['UNIT_MEASURE'].map(str)
df.head()

#converter o tempo

#criar um array
df = df.assign(points = df[['TIME_PERIOD', 'ASSESSMENT_CODE']].values.tolist())

#Vou usar o campo OBS_VALUE como fields (informações adicionais)
df = df.rename(columns = {'OBS_VALUE':'field_obs_value'})

#selecionar as colunas que realmente preciso
df = pd.DataFrame(df, columns = ['series_id', 'points','field_obs_value'])

#criar e salvar o json
result = df.to_json(orient='records')
parsed = json.loads(result)
print(json.dumps(parsed, indent=4))
#df.to_json('JsonResult.json', orient = 'records')