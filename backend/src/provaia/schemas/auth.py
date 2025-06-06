# provaia/src/schemas/auth.py
"""
===============================================================================
SCHEMAS PARA AUTENTICAÇÃO DE USUÁRIOS - ProvaIA
===============================================================================

Este módulo define os schemas Pydantic utilizados para validação e serialização 
dos dados relacionados à autenticação de usuários no sistema ProvaIA. 

Os modelos aqui definidos são utilizados para representar tokens de 
autenticação e perfis de usuários provenientes do fluxo OAuth2 do Google.

===============================================================================
FUNCIONALIDADES
===============================================================================
1. **Validação dos Dados**:
    - Assegura que os dados relacionados aos tokens e usuários estejam 
        sempre no formato correto e completo ao serem manipulados pela aplicação.

2. **Serialização de Dados**:
    - Facilita a conversão automática de dados Python em formatos JSON e 
        vice-versa durante a comunicação com o frontend e APIs externas.

===============================================================================
CLASSES E SCHEMAS
===============================================================================

- `UserProfile`
    - Representa informações básicas do perfil do usuário autenticado.

- `TokenSchema`
    - Contém informações sobre o token OAuth2 retornado após autenticação bem-sucedida.

===============================================================================
COMO UTILIZAR
===============================================================================

Esses schemas são tipicamente usados em endpoints do FastAPI para validar 
respostas e requisições envolvendo autenticação de usuários:

Exemplo de uso em uma rota FastAPI:
```python
@app.post("/login")
def login(token: TokenSchema):
    # Processa autenticação com o token fornecido
```

===============================================================================
AUTOR
===============================================================================
- Autor: Paulo César Rodacki Gomes
- E-mail: rodacki@gmail.com
- Data: 10/03/2025
===============================================================================
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# ----------------------------------------
# SCHEMAS PARA AUTENTICAÇÃO
# ----------------------------------------

class UserProfile(BaseModel):
    """
    Representa as informações do perfil do usuário autenticado via Google OAuth2.

    Atributos:
        id (str): Identificador único do usuário no Google.
        email (Optional[str]): Endereço de e-mail do usuário, opcionalmente fornecido.
    """
    id: str
    name: str
    email: Optional[str] = None


# class TokenSchema(BaseModel):
#     """
#     Representa o schema do token OAuth2 gerado após a autenticação bem-sucedida do usuário.

#     Atributos:
#         access_token (str): Token de acesso utilizado para autenticação nas requisições subsequentes.
#         refresh_token (Optional[str]): Token para atualizar o token de acesso após expiração.
#         expires_at (datetime): Data e hora em que o token de acesso expira.
#         user_id (str): Identificador único do usuário autenticado.
#     """
#     access_token: str
#     refresh_token: Optional[str] = None
#     expires_at: datetime
#     user_id: str

class TokenSchema(BaseModel):
    """
    Representa o schema do token OAuth2 gerado após a autenticação bem-sucedida do usuário.

    Atributos:
        token (str): Token de acesso utilizado para autenticação nas requisições subsequentes.
        refresh_token (Optional[str]): Token para atualizar o token de acesso após expiração.
        token_uri (str): URL para renovação do token de acesso.
        client_id (str): Identificador do cliente autenticado.
        client_secret (str): Segredo do cliente para autenticação OAuth2.
        scopes (List[str]): Lista de escopos concedidos ao token.
        universe_domain (Optional[str]): Domínio associado ao serviço autenticado (ex.: "googleapis.com").
        account (Optional[str]): Conta autenticada associada ao token.
        expiry (datetime): Data e hora em que o token expira (formato ISO 8601).
    """

    token: str  # ✅ Altera "access_token" para "token" para compatibilidade
    refresh_token: Optional[str] = None
    token_uri: str
    client_id: str
    client_secret: str
    scopes: List[str]
    universe_domain: Optional[str] = "googleapis.com"
    account: Optional[str] = None
    expiry: datetime  # ✅ Nome alinhado ao JSON correto

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}  # ✅ Garante ISO format no JSON



# ----------------------------------------
# FIM DO MÓDULO
# ----------------------------------------