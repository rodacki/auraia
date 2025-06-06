"""
===============================================================================
MÓDULO DE GERENCIAMENTO DE TOKEN (TOKEN SERVICE)
===============================================================================

Este módulo oferece funções utilitárias para o gerenciamento de tokens de autenticação
do Google OAuth2. Os tokens são salvos em formato JSON no sistema de arquivos e podem
ser posteriormente carregados para uso na autenticação das APIs do Google.

===============================================================================
FUNCIONALIDADES
===============================================================================

1. **Salvar Token em Arquivo:**
   - Salva o token recebido no formato JSON em um arquivo especificado.
   - Garante que o caminho absoluto seja corretamente gerado.

2. **Carregar Token do Arquivo:**
   - Carrega o token salvo em formato JSON do arquivo especificado.
   - Verifica a integridade e validade do token antes do uso.

===============================================================================
PRINCIPAIS FUNÇÕES
===============================================================================
- `save_token_to_file(token_data)`: Salva os dados do token no arquivo.
- `load_token_from_file()`: Recupera o token salvo, realizando verificações 
    para garantir integridade e validade.

===============================================================================
EXEMPLOS
===============================================================================

Salvar token:
```python
save_token_to_file(token_data)
```

Carregar token:
```python
token = load_token_from_file()
if token:
    print("Token carregado:", token)
else:
    print("Token não disponível ou inválido.")
```

===============================================================================
DEPENDÊNCIAS
===============================================================================

- Bibliotecas Python:
  - `json`: para leitura e escrita do token em arquivo.
  - `os`: para manipulação de caminhos de arquivos.
  
===============================================================================
AUTOR
===============================================================================
- Paulo César Rodacki Gomes
- Email: rodacki@gmail.com
- Data: 10/03/2025
===============================================================================
"""

# def save_token_to_file(token_data: TokenSchema):
#     """
#     Salva o token OAuth2 em um arquivo JSON.

#     Args:
#         token_data (TokenSchema): Dados do token a serem salvos.

#     Side Effects:
#         - Cria ou sobrescreve o arquivo `token.json` com os dados do token.
#         - Exibe uma mensagem indicando sucesso ou falha na operação.
#     """
#     try:
#         os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)

#          # Converter expires_at para string ISO antes de salvar
#         token_dict = token_data.model_dump()
#         token_dict["expires_at"] = token_dict["expires_at"].isoformat()

#         with open(TOKEN_FILE, "w") as f:
#             json.dump(token_dict, f, indent=4)
#         print(f"✅ Token salvo com sucesso em: {TOKEN_FILE}")
#     except Exception as e:
#         print(f"❌ Erro ao salvar token: {e}")


# def load_token_from_file() -> Optional[TokenSchema]:
#     """
#     Carrega o token OAuth2 do arquivo JSON.

#     Returns:
#         TokenSchema | None: Retorna o objeto TokenSchema caso exista e esteja válido.
#                              Retorna None em caso de erro ou token inválido.

#     Raises:
#         JSONDecodeError: Se o arquivo JSON estiver corrompido.
#     """
#     if not os.path.exists(TOKEN_FILE):
#         print("⚠️ Arquivo de token não encontrado.")
#         return None

#     try:
#         with open(TOKEN_FILE, "r") as f:
#             token_data = json.load(f)

#         # Verifica se o token possui a chave necessária antes de tentar processá-lo
#         if "expires_at" not in token_data:
#             print("❌ Erro: O token não contém a chave 'expires_at'.")
#             return None

#         expires_at = datetime.fromisoformat(token_data["expires_at"])
#         if expires_at < datetime.utcnow():
#             print("⚠️ Token expirado, precisa de renovação!")
#             return None  # Token expirado

#         print(f"✅ Token carregado com sucesso: expira em {expires_at}")
#         return TokenSchema(**token_data)

#     except json.JSONDecodeError:
#         print(f"❌ Erro: O arquivo de token '{TOKEN_FILE}' está corrompido. Exclua-o e faça login novamente.")
#         return None
#     except Exception as e:
#         print(f"❌ Erro inesperado ao carregar o token: {e}")
#         return None

# ----------------------------------------
# IMPORTS
# ----------------------------------------
import json
import os
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from typing import Optional
from pydantic import ValidationError


# ----------------------------------------
# CONFIGURAÇÕES
# ----------------------------------------
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "token.json")
TOKEN_FILE = os.path.abspath(TOKEN_FILE)

# ----------------------------------------
# FUNÇÕES
# ----------------------------------------

def token_exists() -> bool:
    """
    Verifica se o arquivo de token existe.

    Returns:
        bool: True se o arquivo de token existir, False caso contrário.
    """
    return os.path.exists(TOKEN_FILE)


# def load_token() -> Optional[Credentials]:
#     """
#     Carrega o token OAuth2 do arquivo JSON.

#     Returns:
#         Credentials | None: Retorna o objeto Credentials caso exista e esteja válido.
#                             Retorna None em caso de erro ou token inválido.
#     """
#     if not token_exists():
#         print("⚠️ auth_service.py - load_token - Arquivo de token não encontrado.")
#         return None

#     try:
#         with open(TOKEN_FILE, "r") as f:
#             token_data = json.load(f)

#         creds = Credentials.from_authorized_user_info(token_data)

#         # Verifica a expiração do token
#         if creds.expired and creds.refresh_token:
#             print("🔄 Token expirado. Tentando renovação...")
#             creds.refresh(Request())
#             save_token(creds)  # Salva o novo token após renovação
#             print(f"✅ auth_service.py - load_token - Token renovado com sucesso. Expira em: {creds.expiry}")
#         elif creds.expired:
#             print("⚠️ auth_service.py - load_token - Token expirado e não pode ser renovado. Autentique-se novamente.")
#             return None

#         print(f"✅ auth_service.py - load_token - Token carregado com sucesso: expira em {creds.expiry}")
#         return creds

#     except json.JSONDecodeError:
#         print(f"❌ auth_service.py - load_token - Erro: O arquivo de token '{TOKEN_FILE}' está corrompido. Exclua-o e faça login novamente.")
#         return None
#     except ValidationError as e:
#         print(f"❌ auth_service.py - load_token - Erro de validação ao carregar o token: {e}")
#         return None
#     except Exception as e:
#         print(f"❌ auth_service.py - load_token - Erro inesperado ao carregar o token: {e}")
#         return None


def save_token(creds: Credentials):
    """
    Salva as credenciais OAuth2 em um arquivo JSON.

    Args:
        creds (Credentials): Objeto de credenciais do Google.

    Side Effects:
        - Cria ou sobrescreve o arquivo `token.json` com os dados do token.
        - Exibe uma mensagem indicando sucesso ou falha na operação.
    """
    try:
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)

        # Usa `creds.to_json()` para garantir o formato correto
        with open(TOKEN_FILE, "w") as f:
            json.dump(json.loads(creds.to_json()), f, indent=4)

        print(f"✅ token_service.py - save_token - Token salvo com sucesso em: {TOKEN_FILE}")

    except Exception as e:
        print(f"❌ token_service.py - save_token - Erro ao salvar token: {e}")


def delete_token():
    """
    Remove o arquivo de token, se existir.

    Side Effects:
        - Exclui o arquivo `token.json`, se presente.
        - Exibe uma mensagem indicando sucesso ou falha na operação.
    """
    try:
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
            print(f"🗑️ token_service.py - delete_token - Token removido com sucesso: {TOKEN_FILE}")
        else:
            print("⚠️ token_service.py - delete_token - Nenhum token encontrado para remover.")

    except Exception as e:
        print(f"❌ token_service.py - delete_token - Erro ao remover token: {e}")

    


# def load_token() -> Optional[Credentials]:
#     if not token_exists():
#         print("⚠️ token_service.py - load_token - Arquivo de token não encontrado.")
#         return None

#     try:
#         with open(TOKEN_FILE, "r") as f:
#             token_data = json.load(f)

#         creds = Credentials.from_authorized_user_info(token_data)

#         # Verifica se o token pode ser renovado
#         if creds.expired and creds.refresh_token:
#             print("🔄 Token expirado. Tentando renovação...")
#             creds.refresh(Request())
#             save_token(creds)
#             print(f"✅ token_service.py - load_token - Token renovado com sucesso.")
#         elif creds.expired:
#             print("⚠️ token_service.py - load_token - Token expirado e não pode ser renovado.")
#             return None

#         return creds

#     except json.JSONDecodeError:
#         print(f"❌ token_service.py - load_token - Erro: O arquivo de token '{TOKEN_FILE}' está corrompido.")
#         return None
#     except Exception as e:
#         print(f"❌ token_service.py - load_token - Erro inesperado ao carregar o token: {e}")
#         return None


def load_token() -> Optional[Credentials]:
    if not token_exists():
        print("⚠️ token_service.py - load_token - Arquivo de token não encontrado.")
        return None

    try:
        with open(TOKEN_FILE, "r") as f:
            token_data = json.load(f)

        creds = Credentials.from_authorized_user_info(token_data)

        # Se o token estiver expirado mas puder ser renovado, renova
        if creds.expired and creds.refresh_token:
            print("🔄 Token expirado. Tentando renovação...")
            creds.refresh(Request())
            save_token(creds)
            print(f"✅ token_service.py - load_token - Token renovado com sucesso.")
        elif creds.expired:
            print("⚠️ token_service.py - load_token - Token expirado e não pode ser renovado.")
            return None

        return creds

    except json.JSONDecodeError:
        print(f"❌ token_service.py - load_token - Erro: O arquivo de token está corrompido. Exclua-o e faça login novamente.")
        return None  # NÃO INICIA NOVO LOGIN AQUI
    except Exception as e:
        print(f"❌ token_service.py - load_token - Erro inesperado: {e}")
        return None