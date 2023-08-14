from google.oauth2 import service_account
import google.auth
import google.auth.transport.requests
from googleapiclient.discovery import build
import json

# Configura las credenciales de autenticación
creds = service_account.Credentials.from_service_account_file(
    'config.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# Load configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Crea una instancia del servicio de Google Sheets
service = build('sheets', 'v4', credentials=creds)

auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)
access_token = creds.token