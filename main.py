import streamlit as st
import json
import requests

# GitHub token e repository
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # Usa il token dal secrets di Streamlit
REPO_OWNER = "itsmbro"  # Sostituisci con il tuo username GitHub
REPO_NAME = "risparmi"  # Sostituisci con il nome del tuo repository
FILE_PATH = "budget_data.json"  # Percorso del file JSON nel repository

# Header per l'autenticazione GitHub
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.raw",
}

# Funzione per leggere i dati dal file JSON su GitHub
def leggi_dati():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return file_content = response.json()
        #file_content = requests.get(content['download_url']).text
        #return json.loads(file_content)
    else:
        st.error(f"Errore nel leggere il file: {response.status_code}")
        return {}

# Funzione per scrivere i dati nel file JSON su GitHub
def scrivi_dati(dati):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    file_content = json.dumps(dati, indent=4)
    data = {
        "message": "Aggiornamento dati budget",
        "content": file_content.encode('utf-8').decode('utf-8'),
        "branch": "main"
    }
    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code == 201:
        st.success("Dati aggiornati con successo!")
    else:
        st.error(f"Errore nel salvare i dati: {response.status_code}")

# Funzione per aggiungere una nuova voce di spesa
def aggiungi_voce_spesa(dati, categoria, importo):
    if categoria not in dati:
        dati[categoria] = importo
    else:
        st.warning(f"La categoria {categoria} esiste già.")
    return dati

# Funzione per rimuovere una voce di spesa
def rimuovi_voce_spesa(dati, categoria):
    if categoria in dati:
        del dati[categoria]
    else:
        st.warning(f"La categoria {categoria} non esiste.")
    return dati

# Leggi i dati dal repository GitHub
dati_budget = leggi_dati()

# UI Streamlit
st.title("Gestione Spese Pre-Convivente e Convivenza")
st.sidebar.header("Seleziona la funzionalità")

# Sezione per la gestione pre-convivenza
if st.sidebar.radio("Seleziona la fase:", ["Pre-Convivente", "Convivenza"]) == "Pre-Convivente":
    st.subheader("Gestione delle spese pre-convivenza")
    
    # Visualizza le voci di spesa attuali
    st.write("Spese attuali:", dati_budget.get("preconvivenza", {}).get("categorie", {}))
    
    # Aggiungi una nuova voce di spesa
    categoria = st.text_input("Categoria di spesa")
    importo = st.number_input("Importo", min_value=0, step=1)
    if st.button("Aggiungi voce di spesa"):
        if categoria and importo:
            dati_budget["preconvivenza"]["categorie"] = aggiungi_voce_spesa(
                dati_budget.get("preconvivenza", {}).get("categorie", {}), categoria, importo
            )
            scrivi_dati(dati_budget)
        else:
            st.error("Compila tutti i campi.")

    # Rimuovi una voce di spesa
    categoria_da_rimuovere = st.text_input("Categoria da rimuovere")
    if st.button("Rimuovi voce di spesa"):
        if categoria_da_rimuovere:
            dati_budget["preconvivenza"]["categorie"] = rimuovi_voce_spesa(
                dati_budget.get("preconvivenza", {}).get("categorie", {}), categoria_da_rimuovere
            )
            scrivi_dati(dati_budget)
        else:
            st.error("Compila tutti i campi.")

# Sezione per la gestione delle spese quotidiane (convivenza)
elif st.sidebar.radio("Seleziona la fase:", ["Pre-Convivente", "Convivenza"]) == "Convivenza":
    st.subheader("Gestione delle spese quotidiane")
    
    # Visualizza le voci di spesa attuali
    st.write("Spese attuali:", dati_budget.get("convivenza", {}).get("categorie", {}))

    # Aggiungi una nuova voce di spesa
    categoria = st.text_input("Categoria di spesa")
    importo = st.number_input("Importo", min_value=0, step=1)
    if st.button("Aggiungi voce di spesa"):
        if categoria and importo:
            dati_budget["convivenza"]["categorie"] = aggiungi_voce_spesa(
                dati_budget.get("convivenza", {}).get("categorie", {}), categoria, importo
            )
            scrivi_dati(dati_budget)
        else:
            st.error("Compila tutti i campi.")

    # Rimuovi una voce di spesa
    categoria_da_rimuovere = st.text_input("Categoria da rimuovere")
    if st.button("Rimuovi voce di spesa"):
        if categoria_da_rimuovere:
            dati_budget["convivenza"]["categorie"] = rimuovi_voce_spesa(
                dati_budget.get("convivenza", {}).get("categorie", {}), categoria_da_rimuovere
            )
            scrivi_dati(dati_budget)
        else:
            st.error("Compila tutti i campi.")
