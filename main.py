import streamlit as st
import json
import requests
import base64
import matplotlib.pyplot as plt

# Configurazione GitHub
GITHUB_USER = "itsmbro"  # Sostituisci con il tuo nome utente GitHub
GITHUB_REPO = "risparmi"    # Sostituisci con il tuo repository GitHub
GITHUB_BRANCH = "main"       # Sostituisci con il nome del branch del tuo repository
GITHUB_FILE_PATH = "file.json"  # Sostituisci con il percorso del tuo file JSON

# Funzione per caricare il JSON da GitHub
def load_json_from_github():
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{GITHUB_FILE_PATH}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Solleva un'eccezione se il codice di stato non è 200
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"Errore HTTP: {http_err}")
        return None
    except Exception as err:
        st.error(f"Errore: {err}")
        return None

# Funzione per salvare il JSON su GitHub
def save_json_to_github(data):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    headers = {
        "Authorization": f"token {st.secrets['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Otteniamo il "sha" del file esistente per aggiornare il contenuto
    response = requests.get(url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_base64 = base64.b64encode(json_data.encode()).decode()

    data_to_commit = {
        "message": "Aggiornamento delle spese",
        "content": json_base64,
        "branch": GITHUB_BRANCH
    }

    if sha:
        data_to_commit["sha"] = sha

    response = requests.put(url, headers=headers, json=data_to_commit)
    
    if response.status_code in [200, 201]:
        st.success("File JSON aggiornato con successo!")
    else:
        st.error(f"Errore nell'aggiornamento: {response.json()}")

# Caricamento dei dati dal JSON di GitHub
data = load_json_from_github()
if data:
    st.write(data)  # Mostra il JSON caricato

# Menu di navigazione
menu = ["Pre-convivenza", "Convivenza"]
choice = st.sidebar.selectbox("Seleziona una sezione", menu)

# Funzione per la gestione delle spese pre-convivenza
def gestione_pre_convivenza(data):
    st.header("Gestione delle Spese Pre-Convivenza")
    
    if "pre_convivenza" not in data:
        data["pre_convivenza"] = {"categorie": {}}
    
    category = st.text_input("Aggiungi categoria (pre-convivenza)")
    amount = st.number_input("Importo", min_value=0.0)
    
    if st.button("Aggiungi voce di spesa"):
        if category and amount > 0:
            data["pre_convivenza"]["categorie"][category] = amount
            save_json_to_github(data)
        else:
            st.warning("Inserisci un nome e un importo validi.")
    
    # Grafico a torta per la Pre-convivenza
    if "pre_convivenza" in data:
        categories = list(data["pre_convivenza"]["categorie"].keys())
        amounts = list(data["pre_convivenza"]["categorie"].values())

        # Grafico a torta
        fig, ax = plt.subplots()
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)

# Funzione per la gestione delle spese durante la convivenza
def gestione_convivenza(data):
    st.header("Gestione delle Spese Convivenza")
    
    if "convivenza" not in data:
        data["convivenza"] = {"categorie": {}}
    
    category = st.text_input("Aggiungi categoria (convivenza)")
    amount = st.number_input("Importo", min_value=0.0)
    
    if st.button("Aggiungi voce di spesa"):
        if category and amount > 0:
            data["convivenza"]["categorie"][category] = amount
            save_json_to_github(data)
        else:
            st.warning("Inserisci un nome e un importo validi.")
    
    # Grafico a torta per la Convivenza
    if "convivenza" in data:
        categories = list(data["convivenza"]["categorie"].keys())
        amounts = list(data["convivenza"]["categorie"].values())

        # Grafico a torta
        fig, ax = plt.subplots()
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)

# Gestione delle scelte del menu
if choice == "Pre-convivenza":
    gestione_pre_convivenza(data)
elif choice == "Convivenza":
    gestione_convivenza(data)
