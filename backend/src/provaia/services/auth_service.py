# provaia/src/provaia/services/auth_service.py

"""
===============================================================================
SERVIÇOS DE AUTENTICAÇÃO COM O GOOGLE (auth_service.py)
===============================================================================
Este módulo contém serviços relacionados à autenticação OAuth2 utilizando as
credenciais do Google, necessárias para integração com Google Classroom e outras
APIs do ecossistema Google.

===============================================================================
FUNCIONALIDADES
===============================================================================
- Autenticação OAuth2 com Google Classroom.
- Gerenciamento automático de tokens de acesso (armazenamento e renovação).
- Troca de código OAuth por token de acesso.

===============================================================================
PRINCIPAIS FUNÇÕES
===============================================================================
- get_google_credentials():
    Obtém credenciais OAuth2 para acessar serviços do Google. Gerencia o
    armazenamento local e a renovação dos tokens automaticamente.

- exchange_code_for_token(code: str):
    Recebe um código de autenticação OAuth2 do Google e o troca por um token
    de acesso válido.

===============================================================================
COMO UTILIZAR
===============================================================================
1. Obter credenciais OAuth2:
   ```python
   credentials = get_google_credentials()
   ```

2. Trocar código OAuth por token:
   ```python
   token_info = exchange_code_for_token("código_de_autorização")
   ```

===============================================================================
DEPENDÊNCIAS
===============================================================================
- google-auth-oauthlib
- google-auth
- requests
- pydantic (via config.py)

===============================================================================
AUTOR
===============================================================================
- Desenvolvido por: Paulo César Rodacki Gomes
- Email: rodacki@gmail.com
- Última atualização: 10/03/2025
===============================================================================
"""

# # ----------------------------------------
# # IMPORTS
# # ----------------------------------------
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
# import os
# import requests
# from src.provaia.config import settings

# # ----------------------------------------
# # CONFIGURAÇÕES
# # ----------------------------------------
# TOKEN_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "token.json")
# TOKEN_PATH = os.path.abspath(TOKEN_PATH)
# print(f"Auth_service -TOKEN_PATH: {TOKEN_PATH} ")

# ----------------------------------------
# FUNÇÕES
# ----------------------------------------
# def get_google_credentials():
#     """
#     Obtém credenciais OAuth2 do Google necessárias para acessar o Google Classroom.

#     Verifica se há um token salvo localmente; caso contrário, inicia o fluxo OAuth2
#     para autenticar o usuário e obter um novo token.

#     Returns:
#         Credentials: Objeto contendo as credenciais OAuth2 válidas.
#     """
    
#     creds = None

#     # Carrega as credenciais salvas, se existirem
#     if os.path.exists(TOKEN_PATH):
#         creds = Credentials.from_authorized_user_file(TOKEN_PATH, settings.GOOGLE_SCOPES)

#     # Renova ou gera novas credenciais se necessário
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 settings.GOOGLE_CREDENTIALS_PATH, settings.GOOGLE_SCOPES
#             )
#             creds = flow.run_local_server(port=0)

#         # Salva as novas credenciais no arquivo local
#         with open(TOKEN_PATH, "w") as token_file:
#             token_file.write(creds.to_json())

#     return creds

# def get_google_credentials():
#     """
#     Obtém credenciais OAuth2 do Google necessárias para acessar o Google Classroom.

#     Verifica se há um token salvo localmente; caso contrário, inicia o fluxo OAuth2
#     para autenticar o usuário e obter um novo token.

#     Returns:
#         Credentials: Objeto contendo as credenciais OAuth2 válidas.
#     """

#     print(f"🔍 Verificando token em: {TOKEN_PATH}")

#     creds = None

#     # Verifica se o token já existe
#     if os.path.exists(TOKEN_PATH):
#         try:
#             creds = Credentials.from_authorized_user_file(TOKEN_PATH, settings.GOOGLE_SCOPES)
#             print(f"✅ Token carregado com sucesso de {TOKEN_PATH}")
#         except Exception as e:
#             print(f"⚠️ Erro ao carregar token: {e}")
#             creds = None  # Ignora token inválido

#     # Renova ou gera novas credenciais se necessário
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             print("🔄 Token expirado, tentando renovação...")
#             try:
#                 creds.refresh(Request())
#                 print("✅ Token renovado com sucesso.")
#             except Exception as e:
#                 print(f"⚠️ Erro ao renovar token: {e}")
#         else:
#             print("🔑 Iniciando novo fluxo de autenticação...")
#             print(f"📂 Carregando credenciais de {settings.GOOGLE_CREDENTIALS_PATH}")

#             if not os.path.exists(settings.GOOGLE_CREDENTIALS_PATH):
#                 print(f"❌ Arquivo de credenciais não encontrado: {settings.GOOGLE_CREDENTIALS_PATH}")
#                 return None  # Não há credenciais disponíveis

#             try:
#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     settings.GOOGLE_CREDENTIALS_PATH, settings.GOOGLE_SCOPES
#                 )
#                 creds = flow.run_local_server(port=0)
#                 print("✅ Autenticação concluída com sucesso.")
#             except Exception as e:
#                 print(f"❌ Erro na autenticação: {e}")
#                 return None

#         # Salva o novo token
#         try:
#             os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
#             with open(TOKEN_PATH, "w") as token_file:
#                 token_file.write(creds.to_json())
#             print(f"✅ Token salvo com sucesso em: {TOKEN_PATH}")
#         except Exception as e:
#             print(f"❌ Erro ao salvar token: {e}")

#     return creds


# import json
# import os
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
# from src.provaia.config import settings

# # Caminho do token salvo
# TOKEN_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "token.json")
# TOKEN_PATH = os.path.abspath(TOKEN_PATH)
# print(f"Auth_service -TOKEN_PATH: {TOKEN_PATH} ")

# # Caminho das credenciais do Google
# CREDENTIALS_PATH = settings.GOOGLE_CREDENTIALS_PATH


# def get_google_credentials():
#     """
#     Obtém credenciais OAuth2 do Google necessárias para acessar o Google Classroom.

#     - Verifica se há um token salvo localmente e se ele é válido.
#     - Caso contrário, inicia o fluxo OAuth2 e gera um novo token.
#     - Lê client_id e client_secret diretamente do credentials.json para evitar erros de configuração.

#     Returns:
#         Credentials: Objeto contendo as credenciais OAuth2 válidas ou None se houver erro.
#     """

#     print(f"🔍 Verificando token em: {TOKEN_PATH}")

#     creds = None

#     # Verifica se o token já existe
#     if os.path.exists(TOKEN_PATH):
#         try:
#             creds = Credentials.from_authorized_user_file(TOKEN_PATH, settings.GOOGLE_SCOPES)
#             print(f"✅ Token carregado com sucesso de {TOKEN_PATH}")
#         except Exception as e:
#             print(f"⚠️ Erro ao carregar token: {e}")
#             creds = None  # Ignora token inválido

#     # Se o token for inválido ou precisar de renovação, tenta corrigir
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             print("🔄 Token expirado, tentando renovação...")
#             try:
#                 creds.refresh(Request())
#                 print("✅ Token renovado com sucesso.")
#             except Exception as e:
#                 print(f"⚠️ Erro ao renovar token: {e}")
#                 creds = None  # Se não puder renovar, força novo login

#         if not creds:
#             print("🔑 Iniciando novo fluxo de autenticação...")
#             print(f"📂 Carregando credenciais de {CREDENTIALS_PATH}")

#             if not os.path.exists(CREDENTIALS_PATH):
#                 print(f"❌ Arquivo de credenciais não encontrado: {CREDENTIALS_PATH}")
#                 return None  # Sem credenciais disponíveis

#             try:
#                 # Carrega as credenciais do JSON
#                 with open(CREDENTIALS_PATH, "r") as cred_file:
#                     creds_data = json.load(cred_file)

#                 # Verifica se client_id e client_secret estão presentes
#                 client_id = creds_data.get("installed", {}).get("client_id")
#                 client_secret = creds_data.get("installed", {}).get("client_secret")

#                 if not client_id or not client_secret:
#                     print("❌ Erro: client_id ou client_secret ausentes no credentials.json")
#                     return None

#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     CREDENTIALS_PATH, settings.GOOGLE_SCOPES
#                 )
#                 creds = flow.run_local_server(port=0)
#                 print("✅ Autenticação concluída com sucesso.")

#             except Exception as e:
#                 print(f"❌ Erro na autenticação: {e}")
#                 return None

#         # Salva o novo token
#         try:
#             os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
#             token_dict = json.loads(creds.to_json())

#             # Adiciona client_id e client_secret para evitar erros ao recarregar
#             token_dict["client_id"] = client_id
#             token_dict["client_secret"] = client_secret

#             with open(TOKEN_PATH, "w") as token_file:
#                 json.dump(token_dict, token_file, indent=4)
#             print(f"✅ Token salvo com sucesso em: {TOKEN_PATH}")

#         except Exception as e:
#             print(f"❌ Erro ao salvar token: {e}")

#     return creds


# def exchange_code_for_token(code: str):
#     """
#     Troca o código OAuth2 obtido durante a autenticação por um token de acesso.

#     Args:
#         code (str): Código de autenticação fornecido pelo Google após autorização do usuário.

#     Returns:
#         dict: Informações sobre o token de acesso ou detalhes do erro caso a operação falhe.
#     """
#     token_url = "https://oauth2.googleapis.com/token"
#     data = {
#         "code": code,
#         "client_id": settings.GOOGLE_CLIENT_ID,
#         "client_secret": settings.GOOGLE_CLIENT_SECRET,
#         "redirect_uri": settings.GOOGLE_REDIRECT_URI,
#         "grant_type": "authorization_code"
#     }

#     response = requests.post(token_url, data=data)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"error": "Falha ao trocar código por token", "details": response.json()}
    





# def get_google_credentials():
#     """
#     Obtém credenciais OAuth2 do Google necessárias para acessar o Google Classroom.

#     - Verifica se há um token salvo localmente e se ele é válido.
#     - Caso contrário, inicia o fluxo OAuth2 e gera um novo token.
#     - Lê client_id e client_secret diretamente do credentials.json para evitar erros de configuração.

#     Returns:
#         Credentials: Objeto contendo as credenciais OAuth2 válidas ou None se houver erro.
#     """

#     print(f"🔍 Verificando token em: {TOKEN_PATH}")

#     creds = None

#     # Verifica se o token já existe
#     if os.path.exists(TOKEN_PATH):
#         try:
#             creds = Credentials.from_authorized_user_file(TOKEN_PATH, settings.GOOGLE_SCOPES)
#             print(f"✅ Token carregado com sucesso de {TOKEN_PATH}")
#         except Exception as e:
#             print(f"⚠️ Erro ao carregar token: {e}")
#             creds = None  # Ignora token inválido

#     # Se o token for inválido ou precisar de renovação, tenta corrigir
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             print("🔄 Token expirado, tentando renovação...")
#             try:
#                 creds.refresh(Request())
#                 print("✅ Token renovado com sucesso.")
#             except Exception as e:
#                 print(f"⚠️ Erro ao renovar token: {e}")
#                 creds = None  # Se não puder renovar, força novo login

#         if not creds:
#             print("🔑 Iniciando novo fluxo de autenticação...")
#             print(f"📂 Carregando credenciais de {CREDENTIALS_PATH}")

#             if not os.path.exists(CREDENTIALS_PATH):
#                 print(f"❌ Arquivo de credenciais não encontrado: {CREDENTIALS_PATH}")
#                 return None  # Sem credenciais disponíveis

#             try:
#                 # Carrega as credenciais do JSON
#                 with open(CREDENTIALS_PATH, "r") as cred_file:
#                     creds_data = json.load(cred_file)

#                 # Verifica se client_id e client_secret estão presentes
#                 client_id = creds_data.get("installed", {}).get("client_id")
#                 client_secret = creds_data.get("installed", {}).get("client_secret")

#                 if not client_id or not client_secret:
#                     print("❌ Erro: client_id ou client_secret ausentes no credentials.json")
#                     return None

#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     CREDENTIALS_PATH, settings.GOOGLE_SCOPES
#                 )
#                 creds = flow.run_local_server(port=0)
#                 print("✅ Autenticação concluída com sucesso.")

#             except Exception as e:
#                 print(f"❌ Erro na autenticação: {e}")
#                 return None

#         # Salva o novo token
#         try:
#             os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)

#             with open(TOKEN_PATH, "w") as token_file:
#                 token_file.write(creds.to_json())  # ✅ Usa o formato original

#             print(f"✅ Token salvo com sucesso em: {TOKEN_PATH}")

#         except Exception as e:
#             print(f"❌ Erro ao salvar token: {e}")

#             # token_dict = json.loads(creds.to_json())

#             # # Adiciona client_id e client_secret para evitar erros ao recarregar
#             # token_dict["client_id"] = client_id
#             # token_dict["client_secret"] = client_secret

#             # with open(TOKEN_PATH, "w") as token_file:
#             #     json.dump(token_dict, token_file, indent=4)
#             # print(f"✅ Token salvo com sucesso em: {TOKEN_PATH}")

       

#     return creds




# import json
# import os
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
# from src.provaia.config import settings

# # Caminho do token salvo
# TOKEN_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "token.json")
# TOKEN_PATH = os.path.abspath(TOKEN_PATH)
# print(f"Auth_service -TOKEN_PATH: {TOKEN_PATH} ")

# # Caminho das credenciais do Google
# CREDENTIALS_PATH = settings.GOOGLE_CREDENTIALS_PATH



import os
import requests
from fastapi import HTTPException
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from src.provaia.config import settings
from src.provaia.services.token_service import load_token, save_token, delete_token  # ✅ Uso do token_service

# Caminho das credenciais do Google
CREDENTIALS_PATH = settings.GOOGLE_CREDENTIALS_PATH
print(f"📂 Auth_service.py -  Caminho gerado para credentials.json: {CREDENTIALS_PATH}")

def get_google_credentials():
    """
    Obtém credenciais OAuth2 do Google necessárias para acessar o Google Classroom.

    - Verifica se há um token salvo localmente e se ele é válido.
    - Caso contrário, inicia o fluxo OAuth2 e gera um novo token.

    Returns:
        Credentials: Objeto contendo as credenciais OAuth2 válidas ou None se houver erro.
    """

    print("🔍 Verificando credenciais do Google...")

    creds = load_token()  # ✅ Agora usamos `load_token()` em vez de ler o JSON diretamente

    # Verifica se o token existe e é válido
    if creds and creds.valid:
        print(f"✅ Token válido encontrado. Expira em: {creds.expiry}")
        return creds

    if creds and creds.expired and creds.refresh_token:
        print("🔄 Token expirado. Tentando renovar...")
        try:
            creds.refresh(Request())
            save_token(creds)  # ✅ Agora salvamos usando `save_token()`
            print("✅ Token renovado com sucesso.")
            return creds
        except Exception as e:
            print(f"⚠️ Erro ao renovar token: {e}")
            delete_token()  # Remove token inválido
            return None

    print("🔑 Iniciando novo fluxo de autenticação...")
    print(f"📂 Carregando credenciais de {CREDENTIALS_PATH}")

    if not os.path.exists(CREDENTIALS_PATH):
        print(f"❌ Erro: Arquivo de credenciais não encontrado: {CREDENTIALS_PATH}")
        return None

    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_PATH, settings.GOOGLE_SCOPES
        )
        creds = flow.run_local_server(port=0)
        print("✅ Autenticação concluída com sucesso.")
        
        save_token(creds)  # ✅ Agora salvamos usando `save_token()`
        return creds

    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        return None


def exchange_code_for_token(code: str):
    """
    Troca o código OAuth2 obtido durante a autenticação por um token de acesso.

    Args:
        code (str): Código de autenticação fornecido pelo Google após autorização do usuário.

    Returns:
        dict: Informações sobre o token de acesso ou detalhes do erro caso a operação falhe.
    """
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Falha ao trocar código por token", "details": response.json()}


def verificar_autenticacao_google() -> str:
    """
    Verifica se há um token de autenticação do Google válido.
    Se o token estiver expirado e puder ser renovado, ele é renovado automaticamente.

    Returns:
        str: Token de acesso válido.

    Raises:
        HTTPException: Se o token não for encontrado ou não puder ser renovado.
    """
    creds = load_token()

    if not creds:
        raise HTTPException(status_code=401, detail="Token de autenticação não encontrado. Faça login novamente.")

    # Se o token estiver expirado e tiver um refresh_token, tenta renová-lo
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            save_token(creds)
            print("✅ Token renovado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao renovar token: {e}")
            raise HTTPException(status_code=401, detail="Token expirado e não pode ser renovado. Faça login novamente.")

    return creds.token  # Retorna o token válido