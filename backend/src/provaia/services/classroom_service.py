# provaia/src/provaia/services/classroom_service.py



"""
===============================================================================
SERVIÇOS DE INTEGRAÇÃO COM GOOGLE CLASSROOM
===============================================================================

Este módulo fornece funções para interação com a API do Google Classroom,
permitindo a listagem de cursos, trabalhos e alunos, além de obter o conteúdo
de submissões realizadas por alunos.

===============================================================================
FUNCIONALIDADES
===============================================================================

- **Autenticação com Google Classroom:**
  - Criação e retorno de cliente autenticado para uso com Google Classroom API.

- **Listagem e Obtenção de Dados:**
  - Cursos disponíveis.
  - Trabalhos (coursework) de cursos específicos.
  - Alunos inscritos em um curso.
  - Conteúdo de anexos das submissões dos alunos.

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
from googleapiclient.discovery import build
from src.provaia.services.auth_service import get_google_credentials
from src.provaia.services.file_service import baixar_arquivo_drive
from src.provaia.schemas.classroom import Student
from fastapi import HTTPException


# ----------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------
def get_classroom_service():
    """
    Retorna um cliente autenticado para interagir com a API do Google Classroom.

    Returns:
        googleapiclient.discovery.Resource: Cliente autenticado do Google Classroom.
    """
    creds = get_google_credentials()
    return build("classroom", "v1", credentials=creds)


# ----------------------------------------
# FUNÇÕES
# ----------------------------------------




def listar_cursos():
    """
    Lista os cursos do Google Classroom acessíveis ao usuário autenticado.

    Retorna:
        list[dict]: Uma lista contendo informações básicas dos cursos encontrados.
    """
    service = get_classroom_service()
    results = service.courses().list().execute()
    return results.get("courses", [])


def listar_trabalhos(course_id: str):
    """
    Lista os trabalhos (courseworks) de um curso específico do Google Classroom.

    Args:
        course_id (str): O identificador único do curso.

    Retorna:
        list[dict]: Uma lista contendo os trabalhos do curso especificado.
    """
    service = get_classroom_service()
    results = service.courses().courseWork().list(courseId=course_id).execute()
    trabalhos = results.get("courseWork", [])
    # Ordenando por `creationTime` do mais antigo para o mais recente
    trabalhos.sort(key=lambda t: t.get("creationTime", ""), reverse=False)
    return trabalhos



def obter_conteudo_submissao(course_id: str, coursework_id: str, submission_id: str):
    """
    Obtém o conteúdo anexado em uma submissão específica do aluno.

    Parâmetros:
        course_id (str): ID do curso no Google Classroom.
        coursework_id (str): ID do trabalho específico.
        submission_id (str): ID da submissão feita pelo aluno.

    Retorna:
        Tuple[str, str] | (None, None): 
            - O primeiro valor é o conteúdo textual do anexo (se disponível).
            - O segundo valor é o ID do arquivo no Google Drive.
    """
    service = get_classroom_service()
    submission = service.courses().courseWork().studentSubmissions().get(
        courseId=course_id, courseWorkId=coursework_id, id=submission_id
    ).execute()

    if "assignmentSubmission" not in submission:
        return None, None  # Retorna None se não houver submissão válida

    attachments = submission["assignmentSubmission"].get("attachments", [])
    for attachment in attachments:
        if "driveFile" in attachment:
            file_id = attachment["driveFile"]["id"]
            conteudo = baixar_arquivo_drive(file_id)
            return conteudo, file_id  # Retorna o conteúdo do arquivo e o ID do arquivo

    return None, None  # Caso não haja anexo válido



def obter_nome_aluno(submission):
    """
    Tenta obter o nome do aluno a partir dos metadados da submissão no Google Drive.
    """
    try:
        # Pegando o ID do primeiro arquivo anexado à submissão
        attachments = submission.get("assignmentSubmission", {}).get("attachments", [])
        if not attachments:
            return "Sem anexos"

        file_id = attachments[0].get("driveFile", {}).get("id")
        if not file_id:
            return "Arquivo sem ID"

        # Conectando na API Drive
        drive_service = build('drive', 'v3', credentials=creds)

        # Obtendo metadados do arquivo
        file_metadata = drive_service.files().get(fileId=file_id, fields="owners, name").execute()
        owner_name = file_metadata.get("owners", [{}])[0].get("displayName", "Desconhecido")
        
        print(f"📂 Arquivo enviado por: {owner_name} | Nome do arquivo: {file_metadata.get('name')}")
        return owner_name

    except Exception as e:
        print(f"❌ Erro ao obter nome do aluno via Drive API: {e}")
        return "Erro ao obter nome"



def listar_alunos(course_id: str) -> list[Student]:
    """
    Lista os alunos inscritos em um curso específico, estruturando os dados no modelo Pydantic.

    Args:
        course_id (str): Identificador do curso no Google Classroom.

    Retorna:
        list[Student]: Lista contendo os alunos matriculados no curso.
    """
    service = get_classroom_service()
    results = service.courses().students().list(courseId=course_id).execute()
    
    alunos = results.get("students", [])

    return [
        Student(
            id=aluno["userId"],
            name=aluno["profile"]["name"].get("fullName", "Nome Indisponível"),  # 🔹 Garante um nome válido
            email=aluno["profile"].get("emailAddress"),
            photoUrl=aluno["profile"].get("photoUrl")
        )
        for aluno in alunos
    ]


def obter_detalhes_curso(course_id: str):
    """Obtém detalhes de um curso específico no Google Classroom."""
    service = get_classroom_service()

    try:
        course = service.courses().get(id=course_id).execute()
        return {
            "id": course.get("id"),
            "name": course.get("name"),
            "section": course.get("section"),
            "description": course.get("description"),
            "teacherName": course.get("teacherName"),
            "room": course.get("room"),
            "courseState": course.get("courseState"),
        }
    except Exception as e:
        print(f"❌ Erro ao obter detalhes do curso {course_id}: {e}")
        return None
    
def listar_submissoes(course_id: str, coursework_id: str):
    """Lista as submissões de um trabalho específico."""
    service = get_classroom_service()
    results = service.courses().courseWork().studentSubmissions().list(
        courseId=course_id, courseWorkId=coursework_id
    ).execute()
    return results.get("studentSubmissions", [])


def obter_detalhes_submissao(course_id: str, coursework_id: str, submission_id: str):
    """
    Obtém os detalhes de uma submissão específica de um aluno no Google Classroom.

    Args:
        course_id (str): ID do curso no Google Classroom.
        coursework_id (str): ID do trabalho/atividade no Google Classroom.
        submission_id (str): ID da submissão do aluno.

    Returns:
        dict: Dados da submissão, incluindo anexos (se existirem).
    """
    try:
        service = get_classroom_service()
        submission = (
            service.courses()
            .courseWork()
            .studentSubmissions()
            .get(
                courseId=course_id,
                courseWorkId=coursework_id,
                id=submission_id
            )
            .execute()
        )

        if not submission:
            print(f"❌ Nenhuma submissão encontrada para ID {submission_id}")
            return None

        print(f"✅ Submissão encontrada: {submission}")

        return submission

    except Exception as e:
        print(f"❌ Erro ao obter detalhes da submissão: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter detalhes da submissão.")