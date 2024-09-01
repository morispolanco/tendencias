import streamlit as st
import requests

# Carga las claves API desde los secretos de Streamlit
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

# Configura la API de Serper
serper_url = "https://google.serper.dev/search"
serper_headers = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}

# Configura la API de Together
together_url = "https://api.together.xyz/v1/chat/completions"
together_headers = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

# Función para buscar tendencias actuales con la API de Serper
def buscar_tendencias(query):
    data = {"q": query}
    response = requests.post(serper_url, headers=serper_headers, json=data)
    return response.json()

# Función para generar un análisis o informe con la API de Together
def generar_analisis(texto):
    data = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": [],
        "max_tokens": 2512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["\""],
        "stream": True
    }
    response = requests.post(together_url, headers=together_headers, json=data)
    return response.text

# Interfaz de usuario
st.title("Análisis de tendencias actuales")
query = st.text_input("Ingrese una palabra clave o frase para buscar tendencias")

if st.button("Buscar"):
    tendencias = buscar_tendencias(query)
    texto = ""
    if "results" in tendencias:
        for tendencia in tendencias["results"]:
            texto += tendencia.get("title", "") + "\n" + tendencia.get("description", "") + "\n\n"
    else:
        texto = "No se encontraron resultados"
    analisis = generar_analisis(texto)
    st.write(analisis)
