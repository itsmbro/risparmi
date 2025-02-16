import requests
import json

# GitHub token e repository
GITHUB_TOKEN = "secrets.GITHUB_TOKEN"  # Utilizza il token salvato nei secrets
REPO_OWNER = "itsmbro"
REPO_NAME = "risparmi"
FILE_PATH = "budget_data.json"

# Header per l'autenticazione
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.raw",
}

# Funzione per leggere i dati dal file JSON su GitHub
def leggi_dati():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        content = response.json()
        file_content = requests.get(content['download_url']).text
        print("Dati letti correttamente:", file_content)  # Aggiungi questa riga per debug
        return json.loads(file_content)
    else:
        print(f"Errore nel leggere il file: {response.status_code}")  # Debugging
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
    
    print(f"Stato della scrittura: {response.status_code}")  # Debugging
    return response.status_code
