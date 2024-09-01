import streamlit as st
import requests
import json

# Configuración de las claves de API
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

def search_trends(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def analyze_trends(trends_data):
    url = "https://api.together.xyz/inference"
    payload = json.dumps({
        "model": "togethercomputer/llama-2-70b-chat",
        "prompt": f"Analiza las siguientes tendencias y genera un informe conciso:\n\n{trends_data}\n\nInforme:",
        "max_tokens": 500,
        "temperature": 0.7
    })
    headers = {
        'Authorization': f'Bearer {TOGETHER_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['output']['choices'][0]['text']

def main():
    st.title("Análisis de Tendencias Actuales")

    # Input para la búsqueda de tendencias
    search_query = st.text_input("Ingrese un tema para buscar tendencias:", "Tendencias tecnológicas 2024")

    if st.button("Buscar y Analizar"):
        with st.spinner("Buscando tendencias..."):
            trends_data = search_trends(search_query)
            
        st.subheader("Resultados de la búsqueda:")
        st.json(trends_data)

        with st.spinner("Analizando tendencias..."):
            analysis = analyze_trends(json.dumps(trends_data, indent=2))

        st.subheader("Análisis de las tendencias:")
        st.write(analysis)

if __name__ == "__main__":
    main()
