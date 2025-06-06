# # src/provaia/api/auth_routes.py

"""
===============================================================================
RMÓDULO DE ROTAS DE AUTENTICAÇÃO – Google OAuth2
===============================================================================
Este módulo define as rotas relacionadas à autenticação do usuário usando a 
API OAuth2 do Google. Ele permite autenticar usuários, reutilizar tokens já 
existentes e armazenar novos tokens.

===============================================================================
FUNCIONALIDADES
===============================================================================
- **Autenticação OAuth2:**
  - Realiza autenticação com o Google e gera tokens de acesso.
  - Reutiliza tokens salvos, caso existam e sejam válidos.

- **Gerenciamento de Tokens:**
  - Carrega tokens existentes de arquivo, se disponíveis.
  - Salva novos tokens obtidos via autenticação OAuth2.

===============================================================================
ROTAS DISPONÍVEIS
===============================================================================

- **GET `/auth/login`**: Autentica o usuário e retorna um token de acesso.

===============================================================================
COMO USAR
===============================================================================
1. Autenticação inicial:
    ```
    GET /auth/login
    ```
    - Realiza o fluxo OAuth2 com o Google, se necessário.
    - Retorna o token gerado e salva-o localmente.

2. **Reutilização de Token**:
   - Em acessos subsequentes, reutiliza automaticamente o token salvo se 
   ainda for válido.

===============================================================================
DEPENDÊNCIAS
===============================================================================
- `fastapi`: Framework web para criação de rotas API.
- `src.provaia.services.auth_service`: Serviços de autenticação com Google OAuth2.
- `src.provaia.services.token_service`: Gerenciamento de tokens salvos em arquivos.
- `src.provaia.schemas.auth`: Modelos para validação e serialização de tokens.

===============================================================================
AUTOR
===============================================================================
- Autor: Paulo César Rodacki Gomes
- Email: rodacki@gmail.com
- Data: 10/03/2025
===============================================================================
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
from fastapi import APIRouter, HTTPException
from src.provaia.services.auth_service import get_google_credentials
from src.provaia.services.token_service import save_token, load_token, token_exists
from src.provaia.schemas.auth import TokenSchema
from src.provaia.utils.logger import get_logger 

# ----------------------------------------
# CONFIGURAÇÃO DO LOGGER (para debug)
# ----------------------------------------
logger = get_logger(__name__)

# ----------------------------------------
# CONFIGURAÇÃO DO ROUTER
# ----------------------------------------
router = APIRouter(prefix="/auth", tags=["auth"])

# ----------------------------------------
# ROTAS
# ----------------------------------------
@router.get("/login")
def login():
    """
    Realiza a autenticação do usuário via Google OAuth2.
    
    - Se um token válido já existir, reutiliza o mesmo.
    - Caso contrário, inicia o fluxo de autenticação e salva o novo token.
    
    Retorna:
        - Um dicionário com a mensagem de sucesso e o token de acesso.
        - Em caso de erro, retorna um dicionário com a mensagem de erro.
    """
    logger.info("🔍 Iniciando processo de login")

    # Verifica se já existe um token válido salvo
    if token_exists():
        logger.info("🔄 auth_routes.py - Token já existe, evitando autenticação duplicada.")
        creds = load_token()
        if creds:
            return {"message": "Autenticação reutilizada!", "token": creds.token}

    # Tenta obter novas credenciais via Google OAuth2
    creds = get_google_credentials()
    if not creds:
        logger.error("❌ auth_routes.py - Falha na autenticação com Google.")
        raise HTTPException(status_code=401, detail="Falha na autenticação com o Google")

    logger.info("✅ auth_routes.py - Autenticação concluída com sucesso.")
    save_token(creds)

    return {"message": "Autenticação bem-sucedida!", "token": creds.token}


# ----------------------------------------
# FIM DO MÓDULO
# ----------------------------------------
