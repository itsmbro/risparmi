import streamlit as st
from ui_preconvivenza import gestione_spese_preconvivenza
from ui_convivenza import gestione_spese_convivenza

# Funzione principale per la navigazione tra le sezioni
def main():
    st.title("Gestione Budget Convivenza")
    
    menu = ["Gestione Pre-Convivenza", "Gestione Convivenza"]
    scelta = st.sidebar.selectbox("Seleziona una sezione", menu)
    
    if scelta == "Gestione Pre-Convivenza":
        gestione_spese_preconvivenza()
    elif scelta == "Gestione Convivenza":
        gestione_spese_convivenza()

if __name__ == "__main__":
    main()
