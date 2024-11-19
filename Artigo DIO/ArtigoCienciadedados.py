import streamlit as st
import requests
from docx import Document
import os

# Substitua pela sua chave de assinatura
subscription_key = "ERmb94eTqwUbsS5yW2radKeAeoR6PNdNK8orj39l7DLenLL0DtYPJQQJ99AKACYeBjFXJ3w3AAAbACOGOIG3"
endpoint = 'https://api.cognitive.microsofttranslator.com/translate'
location = "eastus"
target_language = 'pt-br'

def translator_text(text, target_language):
    headers = {
        'Ocp-Apim-Subscription-key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-Type': 'application/json'
    }
    
    body = [{'text': text}]
    
    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': target_language
    }
    
    request = requests.post(endpoint, params=params, headers=headers, json=body)
    
    if request.status_code != 200:
        st.error(f"Erro na tradução: {request.text}")
        return None
    
    response = request.json()
    return response[0]["translations"][0]["text"]

def translate_document(path):
    document = Document(path)
    full_text = []
    for paragraph in document.paragraphs:
        translated_text = translator_text(paragraph.text, target_language)
        if translated_text:  # Verifica se a tradução foi bem-sucedida
            full_text.append(translated_text)
    
    return full_text

st.title("Tradutor de Documentos")

uploaded_file = st.file_uploader("Escolha um arquivo .docx", type="docx")

if uploaded_file is not None:
    with open("temp.docx", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    translated_text = translate_document("temp.docx")
    
    st.subheader("Texto Traduzido:")
    if translated_text:
        for line in translated_text:
            st.write(line)
    else:
        st.warning("Nenhum texto traduzido disponível.")

    os.remove("temp.docx")  # Remove o arquivo temporário
