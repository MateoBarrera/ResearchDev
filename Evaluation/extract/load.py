import pandas as pd


def __open_csv(path, header="infer"):
    return pd.read_csv(path, header=header)


def __split_date(file):
    file['Fecha'] = pd.to_datetime(file['Fecha'])
    return file


def __filter_csv(file):
    return __split_date(file.filter(items=['CodigoEstacion', 'Municipio', 'IdParametro', 'Fecha', 'Valor', 'Frecuencia']))


def __filter_csv_pw_nasa(file, _type=None):
    if _type == 'pv':
        parameter = 'ALLSKY_SFC_SW_DWN'
    elif _type == 'wind':
        parameter = 'WS10M'
        
    file = file.filter(items=['YEAR', 'MO', 'DY', parameter])
    file = file.rename(
        columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day', parameter: 'Valor'})
    file['Fecha'] = pd.to_datetime(file[['year', 'month', 'day']])
    file['Frecuencia'] = 'Daily'
    file.drop(['year', 'month', 'day'], axis=1)
    return __split_date(file)


def __get_stations(file):
    return file.drop_duplicates(subset=['CodigoEstacion'])['CodigoEstacion'].to_list()


def __extract_info(file, _type):
    info = {}

    if _type == 'pv':
        info['unit']= 'kWh/m^2/day'
    elif _type == 'hydro':
        info['unit'] = 'm^3/s'
    elif _type == 'wind':
        info['unit'] = 'm/s'
    else:
        info['unit'] = 'm^3/s'
    
    info['date_start'] = file['Fecha'].min()
    info['date_end'] = file['Fecha'].max()
    info['frequency'] = 'Monthly' if file['Frecuencia'][0] == 'Mensual' else file['Frecuencia'][0]
    
    return info


def __load_data(file, station):
    return file.loc[file['CodigoEstacion'] == station].filter(
        items=['Fecha', 'Valor'])  # .to_dict('records')


def __load_data_pw_nasa(file):
    return file.filter(items=['Fecha', 'Valor'])  # .to_dict('records')


def read_ideam_data(path, _type, station):
    dictionary = {}
    
    file = __open_csv(path=path)
    file = __filter_csv(file)
    dictionary['data'] = __load_data(file, station)
    dictionary['info'] = __extract_info(file, _type)

    return dictionary


def read_pw_nasa_data(path, _type):
    dictionary = {}

    file = __open_csv(path=path)
    file = __filter_csv_pw_nasa(file, _type)
    dictionary['data'] = __load_data_pw_nasa(file)
    dictionary['info'] = __extract_info(file, _type)

    return dictionary
