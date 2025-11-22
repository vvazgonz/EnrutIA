#imports
import pandas as pd
import os
import pickle
from obtain_category import obtain_category
from excel_to_pandas import excel2pandas



carpeta = 'benchmark/train.xlsx'

# Servicio
def enrutador(k, input):
    if not os.path.isdir(carpeta):
        excel2pandas(carpeta, k)
    
    with open("data/usage.pkl", "rb") as f:
        data = pickle.load(f)

    Ratio = data["ratio_k"]
    categories = data["categorias"]

    #Obtenemos la categoria mediante un LLM
    categoria = obtain_category(input, Ratio, categories)

    # Si hemos hallado alguna categoria en la respuesta, obtenemos el modelo con mayor ratio en esa categoria
    return Ratio.loc[categoria].idxmax()





