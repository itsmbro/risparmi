import streamlit as st
from data_handler import leggi_dati, scrivi_dati

# Funzione per visualizzare e aggiornare le spese pre-convivenza
def gestione_spese_preconvivenza():
    st.title("Gestione Spese Pre-Convivenza")
    
    # Carica i dati dal JSON
    dati = leggi_dati()
    preconvivenza = dati.get('preconvivenza', {})
    categorie = preconvivenza.get('categorie', {})
    
    # Visualizza le categorie e i relativi budget
    for categoria, valore in categorie.items():
        st.write(f"{categoria}: {valore}€")
    
    # Aggiungi o modifica una categoria
    categoria = st.text_input("Nome categoria da aggiungere/modificare")
    valore = st.number_input("Importo per la categoria", min_value=0, step=50)
    
    if st.button("Aggiungi/Modifica Categoria"):
        scrivi_dati(categoria, valore, 'preconvivenza')
        st.success(f"Categoria '{categoria}' aggiornata con {valore}€")
