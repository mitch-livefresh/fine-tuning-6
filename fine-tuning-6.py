import openai
import streamlit as st
from dotenv import load_dotenv
import os
import re  

# UMgebungsvariablen werden geladen
load_dotenv()

# API-Schlüssel lesen
openai.api_key = os.getenv('OPENAI_API_KEY')

# LiveFresh-Logo
logo_path = 'logo-liveFresh.png'

# Titel und Logo der Streamlit Seite/App anzeigen
st.image(logo_path, width=200)  # Logo-Größe anpassen
st.title('LiveFresh Berater')
st.caption('Produkt und Gesundheitsberater für LiveFresh / kein medizinischer Ratgeber. Stelle mir Fragen zu Produkten von LiveFresh oder gesundheitlichen Themen')

# CSS integrieren
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Chatverlauf initialisieren
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Funktion, um URLs in anklickbare Links umzuwandeln
def clickable_links(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(lambda url: f'<a href="{url.group()}">{url.group()}</a>', text)

# Funktion, um eine Antwort vom OpenAI-Assistenten zu erhalten
def gpt_response(question):
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-1106:personal:lf-gpt-8:99W9n6EB",  # Fine-tuning Model ID (Name)
        messages=[{"role": "system", "content": "Du bist ein hilfreicher LiveFresh Assistent für Produkt- und Gesundheitsberatung."},
                  *st.session_state['messages'],
                  {"role": "user", "content": question}],
    )
    return response.choices[0].message['content']

# Funktion, die ausgeführt wird, wenn der Senden-Button gedrückt wird
def send():
    if st.session_state.user_input:  # Stellt sicher, dass die Eingabe nicht leer ist

        # Eine Antwort vom Fine-Tuning Model erhalten und zum Chatverlauf hinzufügen
        answer = gpt_response(st.session_state.user_input)
        # Füge die Nutzereingabe und die Antwort am Anfang der Liste hinzu, damit die neueste Interaktion zuerst erscheint
        st.session_state['messages'] = [{"role": "user", "content": st.session_state.user_input}, {"role": "assistant", "content": clickable_links(answer)}] + st.session_state['messages']
        # Bereite das Texteingabefeld für die nächste Nachricht vor
        st.session_state.user_input = ""

# Texteingabefeld für die Nutzereingabe
st.text_input("Deine Nachricht:", key="user_input", on_change=send)

# Button, um die Nachricht zu senden
st.button('Senden', on_click=send)

# Chatverlauf anzeigen (neueste Nachrichten zuerst)
for message in st.session_state['messages']:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    role_label = "Du:" if message["role"] == "user" else "Assistent:"
    # URLs in der Nachricht anklickbar machen
    message_content = clickable_links(message["content"]) if message["role"] == "assistant" else message["content"]
    st.markdown(f'<div class="chat-message {role_class}"><b>{role_label}</b> {message_content}</div>', unsafe_allow_html=True)
