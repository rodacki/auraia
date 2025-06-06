# # provaia/src/provaia/api/classroom_routes.py
"""
===============================================================================
ROTAS DE INTEGRAÇÃO COM GOOGLE CLASSROOM
===============================================================================
Este módulo define as rotas da API relacionadas à integração com o Google Classroom.

Permite acessar cursos, trabalhos, alunos e submissões do Google Classroom,
utilizando autenticação via OAuth2.

===============================================================================
FUNCIONALIDADES
===============================================================================
1. **Listagem de Cursos**:
   - Recupera os cursos disponíveis para o usuário autenticado.

2. **Gerenciamento de Trabalhos**:
   - Listagem dos trabalhos (coursework) de um curso específico.

3. **Gerenciamento de Alunos**:
   - Listagem de alunos matriculados em cursos específicos.

4. **Processamento de Submissões**:
   - Recupera e processa submissões de alunos, gerando questões personalizadas.

===============================================================================
ROTAS DISPONÍVEIS
===============================================================================
- `GET /classroom/cursos` → Lista cursos disponíveis.
- `GET /classroom/curso/{course_id}` → Retorna detalhes de um curso.
- `GET /curso/{course_id}/trabalhos` → Lista trabalhos de um curso.
- `GET /curso/{course_id}/trabalho/{coursework_id}/submissoes` → Lista submissões de alunos.
- `GET /curso/{course_id}/trabalho/{coursework_id}/submissao/{submission_id}/processar` → 
    Processa submissão e gera questões personalizadas.
- `GET /curso/{course_id}/alunos` → Lista alunos de um curso.
- `GET /curso/{course_id}/trabalho/{coursework_id}/submissao/{submission_id}/arquivos` → 
    Retorna arquivos anexados em uma submissão.
- `GET /arquivo/{file_id}/conteudo` → Baixa o conteúdo de um arquivo do Google Drive.

===============================================================================
AUTOR
===============================================================================
- Autor: Paulo César Rodacki Gomes
- Email: rodacki@gmail.com
- Data: 11/03/2025

===============================================================================
""" 

# ----------------------------------------
# IMPORTS
# ----------------------------------------
from fastapi import APIRouter, HTTPException, Depends
from src.provaia.services.classroom_service import (
    listar_cursos, 
    listar_alunos, 
    obter_detalhes_curso, 
    obter_detalhes_submissao,
    listar_trabalhos, 
    listar_submissoes
)
from src.provaia.services.questoes_service import processar_submissao
from src.provaia.services.file_service import obter_arquivos_submissao, baixar_arquivo_drive
from src.provaia.services.auth_service import verificar_autenticacao_google
from src.provaia.schemas.geral import Attachment
from src.provaia.utils.logger import get_logger  


# ----------------------------------------
# CONFIGURAÇÃO DO LOGGER (para debug)
# ----------------------------------------
logger = get_logger(__name__)

# ----------------------------------------
# CONFIGURAÇÕES DO ROUTER
# ----------------------------------------
router = APIRouter(prefix="/classroom", tags=["classroom"])


# ----------------------------------------
# ROTAS
# ----------------------------------------

@router.get("/cursos")
async def obter_cursos():
    """
    Retorna a lista de cursos do Google Classroom disponíveis para o usuário autenticado.

    Returns:
        dict: {"cursos": [...]}
    """
    logger.info("📌 Buscando lista de cursos no Google Classroom...")
    cursos = listar_cursos()
    logger.info(f"✅ {len(cursos)} cursos encontrados.")
    return {"cursos": cursos}

@router.get("/curso/{course_id}")
async def obter_curso(course_id: str):
    """Retorna os detalhes do curso identificado por `course_id`."""
    curso = obter_detalhes_curso(course_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso

@router.get("/curso/{course_id}/trabalhos")
async def obter_trabalhos(course_id: str):
    """Lista os trabalhos disponíveis no curso identificado por `course_id`."""
    trabalhos = listar_trabalhos(course_id)
    return {"trabalhos": trabalhos}

@router.get("/curso/{course_id}/trabalho/{coursework_id}/submissoes")
async def obter_submissoes(course_id: str, coursework_id: str):
    """Lista as submissões feitas por alunos para o trabalho identificado por 
    `coursework_id` no curso identificado por `course_id`."""
    submissoes = listar_submissoes(course_id, coursework_id)
    return {"submissoes": submissoes}


@router.get("/curso/{course_id}/trabalho/{coursework_id}/submissao/{submission_id}/processar")
async def processar_resposta_aluno(course_id: str, coursework_id: str, submission_id: str):
    """Processa a submissão específica de um aluno, identificada por `submission_id`, gerando questões personalizadas com base no conteúdo submetido."""
    resultado = await processar_submissao(course_id, coursework_id, submission_id)
    return resultado

@router.get("/curso/{course_id}/alunos")
async def obter_alunos(course_id: str):
    """Retorna a lista de alunos inscritos no curso especificado por `course_id`."""
    alunos = listar_alunos(course_id)
    return {"alunos": alunos} 




@router.get("/curso/{course_id}/trabalho/{coursework_id}/submissao/{submission_id}/arquivos", response_model=list[Attachment])
async def get_submission_files(course_id: str, coursework_id: str, submission_id: str):
    """
    Retorna a lista de anexos (arquivos) enviados em uma submissão de um aluno.
    """

    print(f"🔍 Buscando submissão: curso={course_id}, trabalho={coursework_id}, submissão={submission_id}")

    try:
        # 🔹 Obtém os detalhes da submissão do Google Classroom
        submission = obter_detalhes_submissao(course_id, coursework_id, submission_id)

        if not submission:
            print("❌ Erro: Submissão não encontrada!")
            raise HTTPException(status_code=404, detail="Submissão não encontrada.")

        print(f"✅ Submissão encontrada: {submission}")

        # 🔹 Verifica se a submissão tem o campo 'assignmentSubmission' e se há anexos dentro dele
        if "assignmentSubmission" not in submission:
            print("❌ Erro: Submissão não contém o campo 'assignmentSubmission'.")
            raise HTTPException(status_code=404, detail="Submissão não contém anexos.")

        if "attachments" not in submission["assignmentSubmission"]:
            print("❌ Nenhum anexo encontrado na submissão.")
            raise HTTPException(status_code=404, detail="Nenhum anexo encontrado na submissão.")

        attachments = submission["assignmentSubmission"]["attachments"]

        # 🔹 Processa os arquivos corretamente
        arquivos = obter_arquivos_submissao(attachments)

        if not arquivos:
            print("❌ Nenhum arquivo válido foi encontrado.")
            raise HTTPException(status_code=404, detail="Nenhum arquivo válido encontrado.")

        print(f"✅ Arquivos processados com sucesso: {arquivos}")

        return arquivos

    except Exception as e:
        print(f"❌ ERRO INTERNO: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar arquivos da submissão.")



@router.get("/arquivo/{file_id}/conteudo", response_model=str)
async def baixar_conteudo_arquivo(file_id: str, token: str = Depends(verificar_autenticacao_google)):
    """
    Baixa o conteúdo de um arquivo do Google Drive e o retorna como texto.
    """
    try:
        conteudo = baixar_arquivo_drive(file_id)
        if not conteudo:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado ou vazio.")
        return conteudo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao baixar arquivo: {str(e)}")