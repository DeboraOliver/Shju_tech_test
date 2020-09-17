import os
import dload
import pandas as pd

def jsonforshooju(url):
    #Let's download and unzip our file
    dload.save_unzip(url)

    #getting its location
    dirpath = os.getcwd()
    raw_data = dirpath + "\jodi_gas_csv_beta\jodi_gas_beta.csv"

    #putting all data into a dataframe and creating a new column for series_id
    df = pd.read_csv(raw_data)
    df['series_id'] = df['REF_AREA'] + '-' + df['ENERGY_PRODUCT'] + '-' +  df['FLOW_BREAKDOWN']  + '-' +  df['UNIT_MEASURE'].map(str)

    #creating a time and assessment code array
    df = df.assign(points = df[['TIME_PERIOD', 'ASSESSMENT_CODE']].values.tolist())

    #let´s use OBS_VALUE as additional field
    df = df.rename(columns = {'OBS_VALUE':'field_obs_value'})

    #selecting only useful columns
    df = pd.DataFrame(df, columns = ['series_id', 'points','field_obs_value'])

    #creating a NDJson also known as Json Line
    df.to_json('JsonResult.json', orient = 'records', lines = True)

if __name__ == '__main__':
    url = "https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip"
    jsonforshooju (url)