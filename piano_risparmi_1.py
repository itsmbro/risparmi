import streamlit as st
import pandas as pd
import os

# Funzione che calcola il piano d'accumulo
def calcola_piano(stipendio_tuo, stipendio_ragazza, percentuale, durata_mesi, tasso_annuo, frequenza_interessi):
    try:
        versamento_tuo = stipendio_tuo * percentuale
        versamento_ragazza = stipendio_ragazza * percentuale
        saldo = 0
        dati = []
        
        # Impostazione del numero di giorni totali
        giorni_totali = durata_mesi * 30  

        # Calcolo del tasso di interesse in base alla frequenza selezionata
        if frequenza_interessi == "Giornaliero":
            tasso_periodico = tasso_annuo / 365
            intervallo = 1
        elif frequenza_interessi == "Mensile":
            tasso_periodico = tasso_annuo / 12
            intervallo = 30
        elif frequenza_interessi == "Semestrale":
            tasso_periodico = tasso_annuo / 2
            intervallo = 180
        else:  # Annuale
            tasso_periodico = tasso_annuo
            intervallo = 365

        # Calcolo giorno per giorno
        for giorno in range(1, giorni_totali + 1):
            versamento_totale = versamento_tuo + versamento_ragazza if giorno % 30 == 1 else 0  # Versamento ogni mese
            
            # Calcolo interessi solo quando si raggiunge l'intervallo scelto
            interesse = saldo * tasso_periodico if giorno % intervallo == 0 else 0
            saldo += versamento_totale + interesse

            # Aggiunta dei dati per ogni giorno
            dati.append({
                "Giorno": giorno,
                "Versamento tuo (€)": round(versamento_tuo if giorno % 30 == 1 else 0, 2),
                "Versamento ragazza (€)": round(versamento_ragazza if giorno % 30 == 1 else 0, 2),
                "Totale versato (€)": round(versamento_totale, 2),
                "Interesse maturato (€)": round(interesse, 2),
                "Saldo finale (€)": round(saldo, 2)
            })

        # Creazione del DataFrame
        df = pd.DataFrame(dati)

        # Salvataggio su file Excel
        file_path = os.path.join(os.getcwd(), 'piano_accumulo_risparmi.xlsx')
        df.to_excel(file_path, index=False)

        return df, file_path

    except ValueError:
        return None, "Errore nei dati inseriti. Assicurati di inserire valori numerici validi."


# Interfaccia utente con Streamlit
st.title("Piano d'Accumulazione Risparmi")

# Input dell'utente
stipendio_tuo = st.number_input("Stipendio tuo (€)", min_value=0.0, format="%.2f")
stipendio_ragazza = st.number_input("Stipendio ragazza (€)", min_value=0.0, format="%.2f")
percentuale = st.number_input("Percentuale da versare (%)", min_value=0.0, max_value=100.0, format="%.2f")
durata_mesi = st.number_input("Numero mesi", min_value=1, max_value=600, format="%d")
tasso_annuo = st.number_input("Tasso di interesse annuo (%)", min_value=0.0, format="%.2f")

# Scelta della frequenza degli interessi
frequenza_interessi = st.selectbox(
    "Frequenza di calcolo degli interessi",
    ["Giornaliero", "Mensile", "Semestrale", "Annuale"]
)

# Bottone per calcolare
if st.button("Calcola Piano"):
    if stipendio_tuo > 0 and stipendio_ragazza > 0 and percentuale > 0 and durata_mesi > 0 and tasso_annuo >= 0:
        df, result = calcola_piano(stipendio_tuo, stipendio_ragazza, percentuale / 100, durata_mesi, tasso_annuo / 100, frequenza_interessi)
        if df is not None:
            st.dataframe(df)  # Visualizza il DataFrame con i risultati

            # Messaggio di successo
            st.success(f"File Excel creato con successo: {result}")
        else:
            st.error(result)
    else:
        st.error("Assicurati di inserire valori validi per tutti i campi.")
