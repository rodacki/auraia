

"""
===============================================================================
MÓDULO DE ROTAS PARA GERENCIAMENTO DE PDFs
===============================================================================
Este módulo define as rotas da API relacionadas à criação e disponibilização de
arquivos PDF contendo avaliações geradas automaticamente pelo sistema ProvaIA.

===============================================================================
FUNCIONALIDADES
===============================================================================
1. **Geração de PDF:**
   - Gera um arquivo PDF com questões específicas utilizando o serviço de geração
     de PDFs (`pdf_service`).

2. **Download de PDFs:**
   - Disponibiliza arquivos PDF previamente gerados para download pelo usuário.

===============================================================================
ROTAS DISPONÍVEIS
===============================================================================

- **POST /pdf/gerar**
    - Gera um PDF contendo questões específicas para um determinado aluno.

- **GET /pdf/baixar/{filename}**
    - Realiza o download do arquivo PDF especificado pelo nome do arquivo.

===============================================================================
EXEMPLOS DE USO
===============================================================================

- **Geração de PDF:**

  ```json
  POST /pdf/gerar
  {
    "aluno": "João Silva",
    "questoes": [
      {"enunciado": "Qual é a saída do seguinte código?", "alternativa_a": "..."}
    ]
  }
  ```

- **Download de PDF:**

  ```bash
  GET /pdf/baixar/{filename}
  ```

===============================================================================
DEPENDÊNCIAS
===============================================================================
- FastAPI
- `fastapi.responses.FileResponse`
- Serviços:
    - `pdf_service`
- Schemas:
    - `QuestaoObjetiva`

===============================================================================
AUTOR
===============================================================================
- Autor: Paulo César Rodacki Gomes
- Email: rodacki@gmail.com
- Última atualização: 10/03/2025
===============================================================================
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.provaia.services.pdf_service import create_pdf
from src.provaia.schemas.questoes import QuestaoObjetiva

# ----------------------------------------
# CONFIGURAÇÃO DO ROUTER
# ----------------------------------------
router = APIRouter(prefix="/pdf", tags=["pdf"])

# ----------------------------------------
# ROTAS
# ----------------------------------------
@router.post("/gerar")
async def gerar_pdf(aluno: str, questoes: list[QuestaoObjetiva]):
    """
    Gera um arquivo PDF com questões personalizadas para o aluno especificado.

    Parâmetros:
        aluno (str): Nome completo do aluno.
        questoes (List[QuestaoObjetiva]): Lista de questões para a prova.

    Retorno:
        dict: Caminho do arquivo PDF gerado.
    """
    pdf_path = create_pdf(aluno, questoes)
    return {"pdf": pdf_path}


@router.get("/baixar/{filename}")
async def baixar_pdf(filename: str):
    """
    Baixa um arquivo PDF previamente gerado.

    Parâmetros:
        filename (str): Nome do arquivo PDF.

    Retorno:
        FileResponse: Arquivo PDF solicitado.
    """
    filepath = f"output/{filename}"
    return FileResponse(filepath, filename=filename, media_type="application/pdf")

# ----------------------------------------
# FIM DO MÓDULO
# ----------------------------------------







# @router.post("/gerar")
# async def gerar_pdf(aluno: str, questao: QuestaoObjetiva):
#     """Gera um PDF com a questão e retorna o caminho do arquivo."""
#     pdf_path = create_pdf(aluno, [questao])
#     return {"pdf": pdf_path}

# @router.get("/baixar/{filename}")
# async def baixar_pdf(filename: str):
#     """Baixa um PDF gerado."""
#     filepath = f"output/{filename}"
#     return FileResponse(filepath, filename=filename, media_type="application/pdf")