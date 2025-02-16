import streamlit as st
from data_handler import leggi_dati, scrivi_dati

# Funzione per visualizzare e aggiornare le spese di convivenza
def gestione_spese_convivenza():
    st.title("Gestione Spese di Convivenza")
    
    # Carica i dati dal JSON
    dati = leggi_dati()
    convivenza = dati.get('convivenza', {})
    categorie = convivenza.get('categorie', {})
    
    # Visualizza le categorie e i relativi budget
    for categoria, valore in categorie.items():
        st.write(f"{categoria}: {valore}€")
    
    # Aggiungi o modifica una categoria
    categoria = st.text_input("Nome categoria da aggiungere/modificare")
    valore = st.number_input("Importo per la categoria", min_value=0, step=50)
    
    if st.button("Aggiungi/Modifica Categoria"):
        scrivi_dati(categoria, valore, 'convivenza')
        st.success(f"Categoria '{categoria}' aggiornata con {valore}€")
