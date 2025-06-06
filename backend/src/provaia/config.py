# import os
# from pydantic_settings import BaseSettings
# from typing import List

# class Settings(BaseSettings):
#     OPENAI_API_KEY: str
#     GOOGLE_CLIENT_ID: str
#     GOOGLE_CLIENT_SECRET: str
#     GOOGLE_CREDENTIALS_PATH: str
#     GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
#     GOOGLE_SCOPES: List[str] = [
#         'https://www.googleapis.com/auth/classroom.courses.readonly',
#         'https://www.googleapis.com/auth/classroom.topics.readonly',
#         'https://www.googleapis.com/auth/classroom.coursework.students',
#         'https://www.googleapis.com/auth/drive.readonly',
#         'https://www.googleapis.com/auth/classroom.rosters.readonly', 
#     ]

#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"

# settings = Settings()

"""
===============================================================================
CONFIGURAÇÕES DO SISTEMA PROVAIA
===============================================================================
Este módulo define as configurações globais necessárias para o funcionamento do
sistema ProvaIA, incluindo chaves de API e parâmetros para integração com serviços
externos como OpenAI e Google APIs.

===============================================================================
FUNCIONALIDADES
===============================================================================
1. **Gerenciamento de variáveis de ambiente**:
   - Utiliza `pydantic_settings` para validação automática das variáveis de ambiente.
   - Centraliza todas as configurações sensíveis e globais do sistema.

2. **Chaves e URLs para APIs Externas**:
   - Gerencia credenciais para acesso às APIs da OpenAI e do Google.
   - Define escopos específicos para integração com o Google Classroom e Drive.

===============================================================================
USO
===============================================================================
- As variáveis devem ser definidas em um arquivo `.env` na raiz do projeto, 
  seguindo o formato chave=valor.

Exemplo do arquivo `.env`:

```bash
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_CREDENTIALS_PATH=path_to_google_credentials.json
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
```

===============================================================================
ATRIBUTOS DA CLASSE SETTINGS
===============================================================================
- `OPENAI_API_KEY` (str): Chave API para acesso à OpenAI.
- `GOOGLE_CLIENT_ID` (str): Identificador do cliente OAuth2 do Google.
- `GOOGLE_CLIENT_SECRET` (str): Segredo do cliente para OAuth2.
- `GOOGLE_CREDENTIALS_PATH` (str): Caminho para o arquivo JSON com as credenciais do Google.
- `GOOGLE_REDIRECT_URI` (str): URL de callback para OAuth2.
- `GOOGLE_SCOPES` (List[str]): Escopos de permissão solicitados ao Google Classroom e Google Drive.

===============================================================================
EXEMPLO DE USO
===============================================================================
Para utilizar as configurações, basta importar o objeto `settings` deste módulo:

```python
from src.provaia.config import settings

api_key = settings.OPENAI_API_KEY
client_id = settings.GOOGLE_CLIENT_ID
```

===============================================================================
DEPENDÊNCIAS
===============================================================================
- `pydantic-settings`: para gerenciar variáveis de ambiente e configurações.

===============================================================================
AUTOR
===============================================================================
- Autor: Paulo César Rodacki Gomes
- Email: rodacki@gmail.com
- Data: 10 de março de 2025
===============================================================================
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
import os
import json
from pydantic_settings import BaseSettings
from typing import List, ClassVar

# ----------------------------------------
# CLASSE DE CONFIGURAÇÕES
# ----------------------------------------
# class Settings(BaseSettings):
#     """
#     Classe para gerenciamento de configurações e variáveis de ambiente do ProvaIA.

#     Atributos:
#         OPENAI_API_KEY (str): Chave de API da OpenAI.
#         GOOGLE_CLIENT_ID (str): ID do cliente Google para autenticação OAuth2.
#         GOOGLE_CLIENT_SECRET (str): Segredo do cliente Google para OAuth2.
#         GOOGLE_CREDENTIALS_PATH (str): Caminho para o arquivo de credenciais do Google.
#         GOOGLE_REDIRECT_URI (str): URI para redirecionamento OAuth2.
#         GOOGLE_SCOPES (List[str]): Escopos necessários para acesso às APIs do Google.
#     """
#     #BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do próprio script
#     BASE_DIR: ClassVar[str] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     OPENAI_API_KEY: str
#     GOOGLE_CLIENT_ID: str
#     GOOGLE_CLIENT_SECRET: str
#     GOOGLE_CREDENTIALS_PATH: str = os.path.join(BASE_DIR, "../data/credentials.json")
#     GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
#     GOOGLE_SCOPES: List[str] = [
#         'https://www.googleapis.com/auth/classroom.courses.readonly',
#         'https://www.googleapis.com/auth/classroom.topics.readonly',
#         'https://www.googleapis.com/auth/classroom.coursework.students',
#         'https://www.googleapis.com/auth/drive.readonly',
#         'https://www.googleapis.com/auth/classroom.rosters.readonly',
#         'https://www.googleapis.com/auth/classroom.profile.emails',  # 🔥 Permite acessar e-mails dos perfis
#         'https://www.googleapis.com/auth/classroom.profile.photos',  # 🔥 Permite acessar nomes e fotos dos alunos

#     ]

    
#     class Config:
#         """
#         Configuração interna para carregamento automático das variáveis a partir de arquivos `.env`.
#         """
#         env_file = ".env"

# # ----------------------------------------
# # INSTÂNCIA GLOBAL DE CONFIGURAÇÕES
# # ----------------------------------------
# settings = Settings()



class Settings(BaseSettings):
    """Configurações globais do sistema."""

    BASE_DIR: ClassVar[str] = os.path.dirname(os.path.abspath(__file__))
    CREDENTIALS_PATH: ClassVar[str] = os.path.join(BASE_DIR, "data/credentials-provaia-ifc3.json")

    
    print(f"📂 Config.py -  Caminho gerado para credentials.json: {CREDENTIALS_PATH}")

    OPENAI_API_KEY: str

    GOOGLE_SCOPES: list[str] = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.topics.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/classroom.rosters.readonly',
    'https://www.googleapis.com/auth/classroom.profile.emails', # teste
	'https://www.googleapis.com/auth/classroom.profile.photos', # teste 
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile', 
    'https://www.googleapis.com/auth/contacts.readonly', 
    'openid', 
]

    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    # Carregar CLIENT_ID e CLIENT_SECRET diretamente do credentials.json
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_CREDENTIALS_PATH: str = CREDENTIALS_PATH

    @classmethod
    def from_credentials(cls):
        """Carrega CLIENT_ID e CLIENT_SECRET de credentials.json."""
        if not os.path.exists(cls.CREDENTIALS_PATH):
            raise FileNotFoundError(f"❌ Arquivo de credenciais não encontrado: {cls.CREDENTIALS_PATH}")

        print(f"📂 Config.py -  Caminho gerado para credentials.json: {cls.CREDENTIALS_PATH}")
        with open(cls.CREDENTIALS_PATH, "r") as cred_file:
            creds_data = json.load(cred_file)

        client_id = creds_data.get("installed", {}).get("client_id")
        client_secret = creds_data.get("installed", {}).get("client_secret")
        print(f"Config.py\nGOOGLE_CLIENT_ID: {client_id}\nGOOGLE_CLIENT_SECRET: {client_secret} ")

        if not client_id or not client_secret:
            raise ValueError("❌ client_id ou client_secret ausentes no credentials.json")

        return cls(
            GOOGLE_CLIENT_ID=client_id,
            GOOGLE_CLIENT_SECRET=client_secret,
            GOOGLE_CREDENTIALS_PATH=cls.CREDENTIALS_PATH
        )

# Carregar configurações
settings = Settings.from_credentials()
print(f"📂 Config.py - Caminho final de GOOGLE_CREDENTIALS_PATH: {settings.GOOGLE_CREDENTIALS_PATH}")