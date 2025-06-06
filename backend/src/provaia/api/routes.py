"""
===============================================================================
ROTAS DA API DO SISTEMA PROVAIA
===============================================================================
Este módulo realiza o agrupamento das rotas do sistema **ProvaIA** em uma única 
instância de `APIRouter` do FastAPI, facilitando o gerenciamento e a organização
dos endpoints disponíveis.

Cada conjunto específico de funcionalidades (autenticação, integração com Google
Classroom, geração de questões via OpenAI e geração de PDFs) é mantido em um 
arquivo de rotas separado para melhor organização e clareza.

===============================================================================
FUNCIONALIDADES
===============================================================================
- **Rotas de Autenticação**: 
  - Gerencia autenticação OAuth2 com Google.

- **Rotas do Google Classroom**:
  - Acessa informações de cursos, trabalhos e submissões dos alunos.

- **Rotas de geração de questões (OpenAI)**:
  - Cria questões personalizadas com uso de IA generativa (OpenAI).

- **Rotas de Geração de PDFs**:
  - Gera arquivos PDF com avaliações personalizadas.

===============================================================================
COMO UTILIZAR
===============================================================================
- O arquivo `routes.py` centraliza e inclui as rotas específicas definidas em
  arquivos separados, facilitando a manutenção e expansão futura.

- Cada rota específica deve ser implementada no respectivo arquivo:
  - `auth_routes.py`
  - `classroom_routes.py`
  - `question_routes.py`
  - `openai_routes.py`
  - `pdf_routes.py`

===============================================================================
EXEMPLOS
===============================================================================
- Para adicionar uma nova rota:
  ```python
  from src.provaia.api.novas_rotas import router as novo_router
  router.include_router(novo_router)
  ```

===============================================================================
DEPENDÊNCIAS
===============================================================================
- FastAPI

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
from fastapi import APIRouter
from src.provaia.api.auth_routes import router as auth_router
from src.provaia.api.question_routes import router as question_router
from src.provaia.api.classroom_routes import router as classroom_router
from src.provaia.api.openai_routes import router as openai_router
from src.provaia.api.pdf_routes import router as pdf_router

# ----------------------------------------
# CONFIGURAÇÃO DAS ROTAS
# ----------------------------------------
router = APIRouter()

# Incluindo rotas específicas organizadas por contexto
router.include_router(auth_router)
router.include_router(question_router)
router.include_router(classroom_router)
router.include_router(openai_router)
router.include_router(pdf_router)
