import pandas as pd
import pickle
import os




def excel2pandas(archivo_origen, k):
    carpeta = archivo_origen.split("/")[0]
    os.makedirs('data', exist_ok=True)
    data = pd.read_excel(archivo_origen) # Leer el excel a un DataFrame
    npreguntas_categoria = data.groupby('CATEGORY').size() # Contar el numero de preguntas de cada categoria
    categories = data['CATEGORY'].unique() # Obtener las categorias del dataset
    # Contar el numero de respuestas correctas por modelo y categoria. 1, 2 y 3 son los códigos para cada modelo.
    ncorrectas_1 = data[data['o4-mini'] == data['correct_answer']].groupby('CATEGORY').size() 
    ncorrectas_2 = data[data['GPT-4o-mini'] == data['correct_answer']].groupby('CATEGORY').size()
    ncorrectas_3 = data[data['Llama-3.1-8B'] == data['correct_answer']].groupby('CATEGORY').size()

    # Juntar  las series que acabamos de crear para obtener el numero de respuestas correctas por modelo y categoria (DataFrame)
    resultados = pd.DataFrame({
        'o4-mini': ncorrectas_1,
        'GPT-4o-mini': ncorrectas_2,
        'Llama-3.1-8B': ncorrectas_3
    }).fillna(0).astype(int)

    # Calcular la probabilidad de que el modelo haya acertado en cada categoría (frecuencias). 
    probabilidades = resultados.div(npreguntas_categoria, axis=0)

    # Creamos un dataFrame con los costes de cada modelo 
    costes = pd.DataFrame({'o4-mini': [55], 'GPT-4o-mini': [7.5], 'Llama-3.1-8B': [0.5]}, index = ['Coste Total'])

    # Creamos una métrica para realizar comparaciones entre modelos, por categoria.
    # Para ello, creamos una constante k y definimos una operación: p * k / c + p
    # con p las probabilidades y c los costes
    Ratio = probabilidades.mul(k).div(costes.iloc[0], axis=1)+ probabilidades
    dfs = {"data": data, "categorias": categories, "ncorrectas": resultados, "frecuecias": probabilidades, "costes": costes, "ratio_k": Ratio}
    with open("data/backup.pkl", "wb") as f:
        pickle.dump(dfs, f)
    with open("data/usage.pkl", "wb") as f:
        pickle.dump({"categorias": categories, "ratio_k": Ratio}, f)
