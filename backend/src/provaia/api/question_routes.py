"""
===============================================================================
ROTAS DA API - QUESTÕES GERADAS POR IA (openai_routes.py)
===============================================================================

Este módulo define as rotas relacionadas à geração automática de questões 
utilizando a integração com a API da OpenAI. As questões são geradas com 
base no conteúdo submetido pelos alunos por meio do Google Classroom.

===============================================================================
FUNCIONALIDADES
===============================================================================

- **Geração automática de questões:**
  - Recebe submissões feitas por alunos no Google Classroom.
  - Utiliza a API da OpenAI para gerar questões personalizadas.
  - Retorna questões estruturadas em formato adequado para avaliação.

===============================================================================
ROTAS DISPONÍVEIS
===============================================================================

- **`GET /{course_id}/{coursework_id}/{submission_id}`**
    - Gera questões adaptadas ao conteúdo enviado pelo aluno em um coursework 
        específico.

===============================================================================
EXEMPLO DE USO
===============================================================================

### Gerar questões a partir de uma submissão:

```http
GET /classroom/{course_id}/{coursework_id}/{submission_id}

Resposta esperada (exemplo):
{
    "aluno": "Maria Silva",
    "questoes": [
        {"tipo": "objetiva", "enunciado": "...", ...},
        {"tipo": "verdadeiro_falso", "enunciado": "...", ...},
        {"tipo": "subjetiva", "enunciado": "...", ...}
    ],
    "pdf": "caminho/do/arquivo.pdf"
}
```

===============================================================================
DEPENDÊNCIAS
===============================================================================

- **FastAPI:** Para criação das rotas da API.
- **openai_service:** Para integração com a API da OpenAI e geração de questões.
- **schemas:** Definições estruturais das questões geradas.

===============================================================================
AUTOR
===============================================================================

- Autor: Paulo César Rodacki Gomes
- Email: rodacki@gmail.com
- Última atualização: 10 de março de 2025

===============================================================================
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
from fastapi import APIRouter, HTTPException
from src.provaia.services.questoes_service import gerar_questoes_para_aluno
from src.provaia.schemas.geral import SourceCodeRequest
from src.provaia.schemas.questoes import ConjuntoQuestoes
from src.provaia.services.openai_service import generate_questions

# ----------------------------------------
# CONFIGURAÇÃO DO ROUTER
# ----------------------------------------
router = APIRouter(prefix="/questions", tags=["questoes"])

# ----------------------------------------
# ROTAS
# ----------------------------------------

@router.get("/{course_id}/{coursework_id}/{submission_id}")
async def gerar_questoes(course_id: str, coursework_id: str, submission_id: str):
    """
    Gera questões personalizadas baseadas na submissão de um aluno específico do Google Classroom.

    Parâmetros:
        - course_id (str): ID do curso no Google Classroom.
        - coursework_id (str): ID do trabalho (atividade) específico do curso.
        - submission_id (str): ID da submissão feita pelo aluno.

    Retorna:
        dict: Um dicionário contendo:
            - Nome do aluno.
            - Lista de questões geradas.
            - Caminho do PDF com as questões geradas.

    Exceções:
        - HTTPException (404): Caso não seja possível gerar questões ou localizar dados necessários.
    """
    resultado = gerar_questoes_para_aluno(course_id, coursework_id, submission_id)

    if "erro" in resultado:
        raise HTTPException(status_code=404, detail=resultado["erro"])

    return resultado

@router.post("/salvar_prova")
async def salvar_prova(conteudo: dict):
    """
    Salva os dados da prova no backend e valida o conteúdo antes do processamento.

    **Parâmetros:**
    - `conteudo (dict)`: Dados submetidos pelo aluno, contendo `conteudo_resposta`.

    **Retorno:**
    - Mensagem de sucesso.

    **Erros:**
    - Retorna 400 se `conteudo_resposta` estiver ausente ou vazio.
    """
    if "conteudo_resposta" not in conteudo or not conteudo["conteudo_resposta"].strip():
        raise HTTPException(status_code=400, detail="Campo 'conteudo_resposta' é obrigatório e não pode estar vazio.")

    # 🚀 Futuramente, podemos armazenar em um banco de dados

    return {"status": "success", "mensagem": "Dados da prova salvos com sucesso!"}


@router.post("/gerar", response_model=ConjuntoQuestoes)
async def generate_questions_endpoint(request: SourceCodeRequest):
    """
    Gera três tipos de questões a partir de um código-fonte:
    - Objetivas
    - Verdadeiro/Falso
    - Dissertativas
    """

    if not request.sourceCode.strip():
        raise HTTPException(status_code=400, detail="Código-fonte não pode estar vazio.")

    try:
        return await generate_questions(request.sourceCode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar questões: {str(e)}")
