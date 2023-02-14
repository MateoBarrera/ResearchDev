import numpy as np
import pandas as pd
from criteria import Criteria
from statistics import geometric_mean
from prettytable import PrettyTable

def normalice_criteria(array:list, type:str):
    """Normaliza el arreglo que recibe teniendo en cuenta su característica de tipo costo o beneficio.

    Args:
        array (list): arreglo que se desea normalizar.
        type (str): tipo de criterio: 0 -> Costo (Minimizar); 1 -> Beneficio (Maximizar) 

    Returns:
        list: arreglo normalizado
    """
    array = np.array(array)
    if type==0:      
      min_array = min(array)/array
      return list(min_array/sum(min_array))
    elif type==1:
      max_array = array/max(array)
      return list(max_array/sum(max_array))

def normalice(array:list, type:str):
    """Normaliza el arreglo que recibe teniendo en cuenta su característica de tipo costo o beneficio.

    Args:
        array (list): arreglo que se desea normalizar.
        type (str): tipo de criterio: 0 -> Costo (Minimizar); 1 -> Beneficio (Maximizar) 

    Returns:
        list: arreglo normalizado
    """
    array = np.array(array)
    if type==0:      
      min_array = [(x-min(array))/(max(array)-min(array)) for x in array]
      return list(min_array/sum(min_array))
    elif type==1:
      max_array = [(max(array)-x)/(max(array)-min(array)) for x in array]
      return list(max_array/sum(max_array))

def criteria_aggregation(df, method=0):
    geo_mean = ["geometric_mean", 0, "geo"]
    columns =  df.columns.tolist()
    criteria_agg = dict()
    columns.pop(0)
    columns.pop(1)
    columns.pop()
    columns.pop()
    columns.pop()
    if method in geo_mean:
      for column in columns:
          aux_0, aux_1, aux_2 = list(), list(), list()
          values = df[column].tolist()
          for value in values:
              aux_0.append(value[0])
              aux_1.append(value[1])
              aux_2.append(value[2])
          criteria_agg[column] = [geometric_mean(aux_0), geometric_mean(aux_1), geometric_mean(aux_2)]
    else:
      for column in columns:
          aux_0, aux_1, aux_2 = list(), list(), list()
          values = df[column].tolist()
          ci = df["CI_"+column].tolist()
          ci = [x if x!=0 else 1e-3 for x in ci]
          ci_norm = normalice_criteria(ci, type=0)
          i = 0
          for value in values:
              aux_0.append(value[0]*ci_norm[i])
              aux_1.append(value[1]*ci_norm[i])
              aux_2.append(value[2]*ci_norm[i])
              i+=1
          criteria_agg[column] = [sum(aux_0), sum(aux_1), sum(aux_2)]
    return criteria_agg

if __name__ == "__main__":
    test_obj = Criteria()
    test_obj.show_all = False
    test_obj.from_excel(path="../Repo/Articulo1/Encuesta/Resultados-9-02-2023.xlsx")
    result = criteria_aggregation(test_obj.weight_criteria, method=0)
    
    table = PrettyTable()
    table.title = "Resultado pesos agregados - media geométrica"
    table.field_names = ['Criterio(s)', 'Vector de pesos']
    for key in result:
       table.add_row([key, result[key]])
    print(table)
    result = criteria_aggregation(test_obj.weight_criteria, method=1)
    
    table = PrettyTable()
    table.title = "Resultado pesos agregados - media geométrica"
    table.field_names = ['Criterio(s)', 'Vector de pesos']
    for key in result:
       table.add_row([key, result[key]])
    print(table)
    #test_obj.show_info()