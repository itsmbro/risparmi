import streamlit as st
import pandas as pd
from openpyxl import Workbook
import os

# Funzione che calcola il piano d'accumulo con interessi composti giornalieri
def calcola_piano(stipendio_tuo, stipendio_ragazza, percentuale, durata_mesi, tasso_annuo):
    try:
        tasso_giornaliero = tasso_annuo / 365
        versamento_tuo = stipendio_tuo * percentuale
        versamento_ragazza = stipendio_ragazza * percentuale
        versamento_totale = versamento_tuo + versamento_ragazza

        saldo = 0
        dati = []
        giorni_totali = durata_mesi * 30  # Approccio semplificato: 30 giorni al mese

        # Calcolo giorno per giorno
        for giorno in range(1, giorni_totali + 1):
            interesse = saldo * tasso_giornaliero
            saldo += interesse

            # Versamento mensile ogni 30 giorni
            if giorno % 30 == 0:
                saldo += versamento_totale

                # Aggiunta dei dati solo per i mesi completi
                dati.append({
                    "Mese": giorno // 30,
                    "Versamento tuo (€)": round(versamento_tuo, 2),
                    "Versamento ragazza (€)": round(versamento_ragazza, 2),
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
st.title("Piano d'Accumulazione Risparmi (Interesse Giornaliero)")

# Input dell'utente
stipendio_tuo = st.number_input("Stipendio tuo (€)", min_value=0.0, format="%.2f")
stipendio_ragazza = st.number_input("Stipendio ragazza (€)", min_value=0.0, format="%.2f")
percentuale = st.number_input("Percentuale da versare (%)", min_value=0.0, max_value=100.0, format="%.2f")
durata_mesi = st.number_input("Numero mesi", min_value=1, max_value=600, format="%d")
tasso_annuo = st.number_input("Tasso di interesse annuo (%)", min_value=0.0, format="%.2f")

# Bottone per calcolare
if st.button("Calcola Piano"):
    if stipendio_tuo > 0 and stipendio_ragazza > 0 and percentuale > 0 and durata_mesi > 0 and tasso_annuo >= 0:
        df, result = calcola_piano(stipendio_tuo, stipendio_ragazza, percentuale / 100, durata_mesi, tasso_annuo / 100)
        if df is not None:
            st.dataframe(df)  # Visualizza il DataFrame con i risultati

            # Messaggio di successo
            st.success(f"File Excel creato con successo: {result}")
        else:
            st.error(result)
    else:
        st.error("Assicurati di inserire valori validi per tutti i campi.")
