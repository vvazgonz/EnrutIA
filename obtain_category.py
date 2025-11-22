from dotenv import load_dotenv
import os
from groq import Groq



# groq key and client
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def obtain_category(input, Ratio, categories):
    #Para cada pregunta, llamamos a la API de Groq, elegimos un modelo y creamos un prompt
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
            "role": "user",
            "content": f"Input text: {input} \n Return me only the most similar category between the text and this ones: 'engineering', 'math', 'economics', 'chemistry', 'health', 'business', 'biology', 'philosophy', 'other', 'computer science', 'history', 'psychology', 'law', 'physics'. Remember return only the word without any other text or dots."
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None
    )

    # Recibimos la respuesta y la guardamos en la lista
    respuesta = ""
    for chunk in completion:
        
        content = chunk.choices[0].delta.content
        if content:
            respuesta += content
    recibido = respuesta.strip().lower()

    # Debido a la posibilidad de que la respuesta no sea exactamente la categoria, comprobamos si la respuesta del
    # modelo contiene la categoria y la guardamos en la lista. Si no, obviamos la respuesta.
    flag = True
    if recibido not in categories:
        flag = False
        for cat in categories:
            if cat in recibido:
                recibido = cat
                flag = True
    return recibido