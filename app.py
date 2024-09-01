import streamlit as st
import requests
import json

# Carga las claves API desde los secretos de Streamlit
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

# Configura la API de Serper
serper_url = "https://api.serper.io/v1/search"
serper_headers = {
    "Authorization": f"Bearer {SERPER_API_KEY}",
    "Content-Type": "application/json"
}

# Configura la API de Together
together_url = "https://api.together.ai/v1/generate"
together_headers = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

# Función para buscar tendencias actuales con la API de Serper
def buscar_tendencias(query):
    params = {
        "q": query,
        "num": 10,
        "sort": "date"
    }
    response = requests.get(serper_url, headers=serper_headers, params=params)
    return response.json()

# Función para generar un análisis o informe con la API de Together
def generar_analisis(texto):
    payload = {
        "text": texto,
        "length": 200,
        "style": "informal"
    }
    response = requests.post(together_url, headers=together_headers, json=payload)
    return response.json()

# Interfaz de usuario
st.title("Análisis de tendencias actuales")
query = st.text_input("Ingrese una palabra clave o frase para buscar tendencias")

if st.button("Buscar"):
    tendencias = buscar_tendencias(query)
    texto = ""
    for tendencia in tendencias["results"]:
        texto += tendencia["title"] + "\n" + tendencia["description"] + "\n\n"
    analisis = generar_analisis(texto)
    st.write(analisis["text"])
