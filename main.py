import streamlit as st
import requests
import json

# Funzione per interagire con GitHub API
def get_github_data():
    url = 'https://api.github.com/repos/itsmbro/risparmi/contents/file.json'
    headers = {
        'Authorization': f'token {st.secrets["GITHUB_TOKEN"]}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_content = response.json()['content']
        file_data = json.loads(requests.utils.unquote(file_content))
        return file_data
    else:
        st.error(f"Errore nel recupero dei dati da GitHub: {response.status_code}")
        return None

def update_github_data(data):
    url = 'https://api.github.com/repos/tuo-utente/tuo-repository/contents/file.json'
    headers = {
        'Authorization': f'token {st.secrets["GITHUB_TOKEN"]}',
    }
    data_json = json.dumps(data)
    message = "Aggiornamento del file JSON tramite Streamlit."
    payload = {
        "message": message,
        "content": requests.utils.quote(data_json),
        "sha": get_github_data()['sha']
    }
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code == 200:
        st.success("File aggiornato con successo!")
    else:
        st.error(f"Errore nell'aggiornamento del file su GitHub: {response.status_code}")

# Funzione per visualizzare la dashboard (grafico a torta)
def plot_pie_chart(categories, title):
    import matplotlib.pyplot as plt

    labels = list(categories.keys())
    values = list(categories.values())

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    st.pyplot(fig)

# Funzione per aggiungere una voce di spesa
def add_expense(data, phase, category, amount):
    if category and amount > 0:
        data[phase]["categorie"][category] = amount
        update_github_data(data)
    else:
        st.error("Categoria o importo non validi")

# Funzione per rimuovere una voce di spesa
def remove_expense(data, phase, category):
    if category in data[phase]["categorie"]:
        del data[phase]["categorie"][category]
        update_github_data(data)
    else:
        st.error("Categoria non esistente")

# Funzione principale
def main():
    # Carica i dati iniziali dal file JSON su GitHub
    data = get_github_data()
    if not data:
        return

    # Barra laterale per navigazione
    phase = st.sidebar.radio("Seleziona la fase", ("Pre-convivenza", "Convivenza"))

    # Visualizzazione dei dati per la fase selezionata
    if phase == "Pre-convivenza":
        st.title("Fase Pre-convivenza")
        categories = data["preconvivenza"]["categorie"]
        plot_pie_chart(categories, "Spese Pre-convivenza")

    elif phase == "Convivenza":
        st.title("Fase Convivenza")
        categories = data["convivenza"]["categorie"]
        plot_pie_chart(categories, "Spese Convivenza")

    # Aggiungi o rimuovi voci di spesa
    category = st.text_input("Nome categoria")
    amount = st.number_input("Importo spesa", min_value=0.0, step=0.01)

    if st.button("Aggiungi voce di spesa"):
        if phase == "Pre-convivenza":
            add_expense(data, "preconvivenza", category, amount)
        elif phase == "Convivenza":
            add_expense(data, "convivenza", category, amount)

    remove_category = st.selectbox("Seleziona categoria da rimuovere", options=list(categories.keys()))
    if st.button("Rimuovi voce di spesa"):
        if phase == "Pre-convivenza":
            remove_expense(data, "preconvivenza", remove_category)
        elif phase == "Convivenza":
            remove_expense(data, "convivenza", remove_category)

    # Mostra le spese correnti
    st.write(f"Spese attuali per {phase}:")
    st.write(categories)

if __name__ == "__main__":
    main()
