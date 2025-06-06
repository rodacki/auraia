import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import openai
import dotenv
from fpdf import FPDF


# ------------------------------------------------------------
# 1) Configurações (escopos, chave OpenAI, etc.)
# ------------------------------------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

print(f"OpenAIKey: {openai.api_key}")

# Exemplo de uso de caminho absoluto baseado no local do script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials-ifc.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'token.json')

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me.readonly",
    'https://www.googleapis.com/auth/classroom.coursework.me'
]



def get_google_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        print(f"Token path: {TOKEN_PATH}")
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
            print("Escopos concedidos:", creds.scopes)
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())
            print(f"Token salvo em: {TOKEN_PATH}")

    return creds

def main():
    # Exemplo de listagem de cursos
    creds = get_google_credentials()
    service = build('classroom', 'v1', credentials=creds)
    results = service.courses().list().execute()
    courses = results.get('courses', [])
    print("Cursos encontrados:")
    for course in courses:
        print(f" - {course.get('name')} (ID: {course.get('id')})")

if __name__ == "__main__":
    main()