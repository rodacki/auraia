"""
quickstart.py - Protótipo do sistema para interagir com o Google Classroom e a API da OpenAI

Este script realiza as seguintes operações:
  - Autentica o usuário com o Google e obtém credenciais para acessar o Google Classroom e o Drive.
  - Lista os cursos disponíveis no Google Classroom e permite a escolha de um curso.
  - Exibe detalhes do curso e lista seus tópicos.
  - Lista os "courseworks" (trabalhos) de um curso e permite a seleção de um deles.
  - Lista as submissões de um coursework, permitindo escolher uma submissão e visualizar seus anexos.
  - Processa o anexo selecionado, seja baixando um arquivo do Google Drive ou obtendo o conteúdo via URL.
  - Envia o código-fonte submetido pelo aluno para a API da OpenAI, solicitando a geração de questões de prova.
  - Gera um PDF com as questões elaboradas e o nome do aluno.
  
Observação: As variáveis de ambiente são carregadas do arquivo .env.
"""

from __future__ import print_function

import os
import os.path
import json
import io
import requests
import rich
from typing import Optional, List, Union
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from openai import OpenAI
from dotenv import load_dotenv
from fpdf import FPDF
from schemas.questoes import QuestaoObjetiva, QuestaoSubjetiva, QuestaoVerdadeiroFalso

# Definição dos escopos necessários para acesso às APIs do Google
SCOPES = [
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

# Caminhos para os arquivos de token e credenciais do Google
TOKEN_PATH = 'backend/src/provaia/data/token.json'
CREDENTIALS_PATH = 'backend/src/provaia/data/credentials-provaia-ifc3.json'

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
# Obtém a API Key da OpenAI do ambiente
api_key = os.getenv("OPENAI_API_KEY")
print(f"API key: {api_key}")

# Instancia o cliente OpenAI com a API key
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------------------------------------------------
# 2) Função para obter credenciais do Google
# ------------------------------------------------------------
def get_google_credentials():
    """
    Obtém as credenciais do Google para acesso às APIs do Classroom e Drive.
    
    Se já houver um token salvo em TOKEN_PATH, ele é carregado. Caso contrário,
    inicia o fluxo OAuth para autenticar e obter novas credenciais, salvando o token
    para futuras execuções.
    
    Retorna:
        creds: Objeto de credenciais do Google.
    """
    print("Obtendo credenciais do Google...")
    creds = None

    # Verifica se já existe um token salvo
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # Se as credenciais não forem válidas, realiza o fluxo OAuth
    if not creds or not creds.valid:
        print("Recuperando credenciais")
        if creds and creds.expired and creds.refresh_token:
            # Atualiza o token se ele estiver expirado
            creds.refresh(Request())
        else:
            # Inicia o fluxo de autenticação com o arquivo de credenciais
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH,  # Caminho para o arquivo de credenciais
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Salva as credenciais obtidas para uso futuro
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())

    print("Escopos concedidos:", creds.scopes)

     # 🚨 Verificação dos escopos concedidos
    granted_scopes = set(creds.scopes)
    required_scopes = set(SCOPES)
    missing_scopes = required_scopes - granted_scopes

    print("\n🔎 **Verificação de escopos:**")
    print(f"✅ Escopos concedidos: {granted_scopes}")

    if missing_scopes:
        print(f"⚠️ **Atenção:** Os seguintes escopos estão ausentes e podem impedir o funcionamento correto:")
        for scope in missing_scopes:
            print(f"   - {scope}")
        print("❗ Você pode precisar revogar o acesso e reautenticar o app.")
    return creds

# ------------------------------------------------------------
# Função para listar os cursos do Google Classroom
# ------------------------------------------------------------
def list_courses(service):
    """
    Lista os cursos disponíveis no Google Classroom.

    Parâmetros:
        service: Objeto de serviço da API Classroom autenticado.
    
    Retorna:
        courses (list): Lista de cursos obtidos da API.
    """
    print("Listando cursos do Google Classroom...")
    results = service.courses().list().execute()
    courses = results.get('courses', [])
    if not courses:
        print("Nenhum curso encontrado ou você não tem permissão de acesso.")
    else:
        for idx, course in enumerate(courses, start=1):
            print(f"{idx}. {course.get('name')} (ID: {course.get('id')})")
    return courses

# ------------------------------------------------------------
# Função para permitir a escolha de um curso pelo usuário
# ------------------------------------------------------------
def choose_course(courses):
    """
    Permite que o usuário escolha um curso a partir de uma lista de cursos.

    Parâmetros:
        courses (list): Lista de cursos obtidos da API.
    
    Retorna:
        curso_escolhido (dict): O curso selecionado pelo usuário.
    """
    curso_idx = int(input("\nEscolha o número do curso: "))
    curso_escolhido = courses[curso_idx - 1]
    print(f"\n>> Curso selecionado: {curso_escolhido.get('name')}")
    print(f"ID do curso: {curso_escolhido.get('id')}")
    return curso_escolhido

# ------------------------------------------------------------
# Função para exibir os detalhes de um curso selecionado
# ------------------------------------------------------------
def show_course_details(service, course):
    """
    Exibe os detalhes do curso selecionado.

    Parâmetros:
        service: Objeto de serviço da API Classroom autenticado.
        course (dict): Curso selecionado.
    """
    course_id = course.get('id')
    dados_curso = service.courses().get(id=course_id).execute()
    print("\nDados do curso:")
    print(json.dumps(dados_curso, indent=4, ensure_ascii=False))

# ------------------------------------------------------------
# Função para listar os trabalhos (courseworks) de um curso
# ------------------------------------------------------------
def list_courseworks(service, course_id):
    """
    Lista os courseworks (trabalhos) de um curso.

    Parâmetros:
        service: Objeto de serviço da API Classroom autenticado.
        course_id (str): ID do curso.
    
    Retorna:
        course_work_list (list): Lista de courseworks do curso.
    """
    try:
        cw_response = service.courses().courseWork().list(courseId=course_id).execute()
        course_work_list = cw_response.get('courseWork', [])
        if not course_work_list:
            print(f"\nNenhum coursework encontrado para o curso: {course_id}")
        else:
            print(f"\nCourseworks do curso {course_id}:")
            for idx, cw in enumerate(course_work_list, start=1):
                print(f"{idx}. ID: {cw.get('id')}, Título: {cw.get('title')}")
        return course_work_list
    except Exception as e:
        print("Erro ao obter os courseworks:", e)
        return []

# ------------------------------------------------------------
# Função para permitir a escolha de um coursework
# ------------------------------------------------------------
def choose_coursework(course_work_list):
    """
    Permite que o usuário escolha um coursework da lista.

    Parâmetros:
        course_work_list (list): Lista de courseworks.
    
    Retorna:
        cw_escolhido (dict): O coursework selecionado.
    """
    cw_idx = int(input("\nEscolha o número do coursework para ver as respostas: "))
    cw_escolhido = course_work_list[cw_idx - 1]
    print(f"\n>> Coursework selecionado: {cw_escolhido.get('title')} (ID: {cw_escolhido.get('id')})")
    return cw_escolhido

# ------------------------------------------------------------
# Função para listar as submissões de um coursework
# ------------------------------------------------------------
def list_submissions(service, course_id, cw_id, creds):
    """
    Lista as submissões de um coursework.

    Parâmetros:
        service: Objeto de serviço da API Classroom autenticado.
        course_id (str): ID do curso.
        cw_id (str): ID do coursework.
    
    Retorna:
        submissions (list): Lista de submissões encontradas.
    """
    try:
        submissions_response = service.courses().courseWork().studentSubmissions().list(
            courseId=course_id, courseWorkId=cw_id
        ).execute()
        submissions = submissions_response.get('studentSubmissions', [])
        if not submissions:
            print("Nenhuma submissão encontrada para este coursework.")
        else:
            print("\nSubmissões:")
            for idx, submission in enumerate(submissions, start=1):
                user_id = submission.get('userId')
                print(f"{idx}. ID da submissão: {submission.get('id')}")
                print(f"   ID do aluno: {submission.get('userId')}")
                try:
                    profile = service.userProfiles().get(userId=user_id).execute()
                    #print(f"User profile: {profile}")
                    student_name = profile.get('name', {}).get('fullName')
                    student_email = get_email_from_people_api(creds, user_id)  # 🔥 Chama API People
                except Exception as e:
                    student_name = "Erro ao obter nome"
                    student_email = "Erro ao obter e-mail"
                    print(f"   ⚠️ Erro ao obter perfil do aluno: {e}")
                print(f"   Nome do aluno: {student_name}")
                print(f"   E-mail do aluno: {student_email}")
                print(f"   Estado da submissão: {submission.get('state')}")
                print("-" * 40)
                if idx == 5: break
            return submissions
    except Exception as e:
        print("Erro ao obter as submissões:", e)
        return []



def get_email_from_people_api(creds, user_id):
    """
    Obtém o e-mail do aluno usando a API People.
    """
    try:
        people_service = build('people', 'v1', credentials=creds)  # 🔥 Usa credenciais diretamente
        person = people_service.people().get(
            resourceName=f'people/{user_id}', 
            personFields='emailAddresses'
        ).execute()
        
        emails = person.get('emailAddresses', [])
        if emails:
            return emails[0].get('value')  # Retorna o primeiro e-mail disponível
        return "E-mail não disponível"
    
    except Exception as e:
        print(f"Erro ao buscar e-mail pela API People: {e}")
        return "E-mail não disponível"


# ------------------------------------------------------------
# Função para permitir a escolha de uma submissão
# ------------------------------------------------------------
def choose_submission(submissions):
    """
    Permite que o usuário escolha uma submissão a partir de uma lista.

    Parâmetros:
        submissions (list): Lista de submissões.
    
    Retorna:
        selected_submission (dict): A submissão escolhida.
    """
    sub_idx = int(input("\nEscolha o número da submissão para visualizar o anexo: "))
    selected_submission = submissions[sub_idx - 1]
    return selected_submission

# ------------------------------------------------------------
# Função para extrair anexos de uma submissão
# ------------------------------------------------------------
def get_submission_attachments(submission):
    """
    Extrai e retorna a lista de anexos de uma submissão.

    Parâmetros:
        submission (dict): Dados da submissão.
    
    Retorna:
        attachments (list): Lista de anexos encontrados, ou lista vazia se nenhum anexo existir.
    """
    assignment_submission = submission.get('assignmentSubmission')
    if assignment_submission is None:
        print("Esta submissão não contém anexos.")
        return []
    attachments = assignment_submission.get('attachments', [])
    if not attachments:
        print("Nenhum anexo encontrado nesta submissão.")
    else:
        print("\nAnexos disponíveis:")
        for idx, attachment in enumerate(attachments, start=1):
            attachment_type = list(attachment.keys())[0]
            print(f"{idx}. Tipo: {attachment_type}")
            if attachment_type == 'driveFile':
                drive_file = attachment.get('driveFile')
                print("   Título:", drive_file.get('title'))
                print("   ID:", drive_file.get('id'))
            elif attachment_type == 'link':
                link = attachment.get('link')
                print("   URL:", link.get('url'))
    return attachments

# ------------------------------------------------------------
# Função para permitir a escolha de um anexo
# ------------------------------------------------------------
def choose_attachment(attachments):
    """
    Permite que o usuário escolha um anexo da lista de anexos.

    Parâmetros:
        attachments (list): Lista de anexos.
    
    Retorna:
        O anexo selecionado.
    """
    att_idx = int(input("\nSelecione o número do anexo para obter o conteúdo: "))
    return attachments[att_idx - 1]

# ------------------------------------------------------------
# Função para processar um anexo (download ou requisição)
# ------------------------------------------------------------
def process_attachment(selected_attachment, creds) -> Optional[str]:
    """
    Processa o anexo selecionado:
      - Se for um 'driveFile', baixa o arquivo via API do Google Drive.
      - Se for um 'link', obtém o conteúdo através de uma requisição HTTP.
    
    Parâmetros:
        selected_attachment (dict): Anexo selecionado.
        creds: Credenciais do Google para acesso ao Drive.
    
    Retorna:
        Conteúdo do anexo como uma string, ou None em caso de falha.
    """
    if 'driveFile' in selected_attachment:
        drive_file = selected_attachment.get('driveFile')
        file_id = drive_file.get('id')
        drive_service = build('drive', 'v3', credentials=creds)
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        print("\nBaixando arquivo do Drive...")
        try:
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    print(f"Download {int(status.progress() * 100)}%.")
            file_content = fh.getvalue().decode('utf-8')
            print(f"Conteúdo do arquivo: \n{file_content}")
            return file_content
        except Exception as e:
            print("Erro ao baixar arquivo do Drive:", e)
            return None
    elif 'link' in selected_attachment:
        link = selected_attachment.get('link')
        url = link.get('url')
        print(f"\nObtendo conteúdo do link: {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print("Falha ao obter o conteúdo do link. Código de status:", response.status_code)
                return None
        except Exception as e:
            print("Erro ao obter o conteúdo do link:", e)
            return None
    else:
        print("Tipo de anexo não suportado para extração de conteúdo.")
        return None

# ------------------------------------------------------------
# Função para listar os tópicos de um curso
# ------------------------------------------------------------
def list_topics(service, course_id):
    """
    Lista os tópicos do curso especificado.

    Parâmetros:
        service: Objeto de serviço da API Classroom autenticado.
        course_id (str): ID do curso.
    """
    response = service.courses().topics().list(courseId=course_id).execute()
    topics = response.get('topic', [])
    if topics:
        print("\nTópicos do curso:")
        for topic in topics:
            print(f"ID: {topic.get('topicId')} - Nome: {topic.get('name')}")
    else:
        print("\nNenhum tópico encontrado para este curso.")

# ------------------------------------------------------------
# Função para enviar o código fonte do aluno para a OpenAI e gerar questões
# ------------------------------------------------------------
def generate_questions(student_answer):
    """
    Envia o conteúdo da resposta do aluno para a API da OpenAI e solicita a elaboração de três questões:
      1. Questão de múltipla escolha.
      2. Questão de verdadeiro/falso.
      3. Questão discursiva.
    
    Parâmetros:
        student_answer (str): Código fonte ou resposta submetida pelo aluno.
    
    Retorna:
        generated_text: Texto contendo as questões geradas, esperado do tipo QuestaoObjetiva.
    """
    system_prompt = (
        "Você é um professor de programação no Bacharelado em Ciência da Computação "
        "e precisa criar questões de prova baseadas no código Python elaborado pelo aluno."
    )
    user_prompt = f"Crie uma questão de múltipla escolha em nível de dificuldade intermediário. Seja claro e objetivo. O código do aluno é: \n\n{student_answer}"
   
    try:
        print("Consultando OpenAI")
        completion = openai_client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=QuestaoObjetiva,
        )
        print("OpenAI respondeu")
        generated_text = completion.choices[0].message.parsed

        # Verifica se o retorno é do tipo esperado
        if isinstance(generated_text, QuestaoObjetiva):
            print("Questão gerada com sucesso!")
            print(generated_text.model_dump_json(indent=2))  # Exibe a questão formatada
        else:
            print("Erro: O retorno da API não é do tipo esperado.")

        return generated_text
    
    except Exception as e:
        print("Erro ao gerar questões com OpenAI:", e)
        return None

# ------------------------------------------------------------
# Função para gerar um PDF com as questões
# ------------------------------------------------------------
def create_pdf(student_name: str, questoes: List[Union[QuestaoObjetiva, QuestaoVerdadeiroFalso, QuestaoSubjetiva]]):
    """
    Gera um arquivo PDF contendo as questões de prova para o aluno.

    Parâmetros:
        student_name (str): Nome do aluno.
        questoes (list): Lista de questões geradas (objetos do tipo QuestaoObjetiva, QuestaoVerdadeiroFalso ou QuestaoSubjetiva).
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Prova - {student_name}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)

    for idx, questao in enumerate(questoes, start=1):
        formatted_text = format_questao(questao)
        pdf.multi_cell(0, 10, f"Questão {idx}:")
        pdf.ln(2)
        pdf.multi_cell(0, 10, formatted_text)
        pdf.ln(5)

    # Gera um nome seguro para o arquivo PDF com base no nome do aluno
    safe_name = "".join(c for c in student_name if c.isalnum() or c in (' ', '_')).rstrip().replace(" ", "_")
    filename = f"{safe_name}_questoes.pdf"
    pdf.output(filename)
    print(f"PDF gerado: {filename}")

# ------------------------------------------------------------
# Função para obter o nome do aluno a partir da submissão
# ------------------------------------------------------------
def get_student_name(submission, service) -> str:
    """
    Retorna o nome completo do aluno baseado na submissão.

    Parâmetros:
        submission (dict): Dados da submissão, contendo o 'userId'.
        service: Objeto de serviço da API Classroom autenticado.
    
    Retorna:
        Nome completo do aluno, ou "Nome não encontrado" em caso de erro.
    """
    user_id = submission.get('userId')
    if not user_id:
        return "Nome não encontrado"
    
    try:
        profile = service.userProfiles().get(userId=user_id).execute()
        return profile.get('name', {}).get('fullName', "Nome não encontrado")
    except Exception as e:
        print("Erro ao obter o perfil do aluno:", e)
        return "Nome não encontrado"

# ------------------------------------------------------------
# Função para formatar uma questão para exibição no PDF
# ------------------------------------------------------------
def format_questao(questao: Union[QuestaoObjetiva, QuestaoVerdadeiroFalso, QuestaoSubjetiva]) -> str:
    """
    Formata uma questão para exibição no PDF, de acordo com seu tipo.
    
    Parâmetros:
        questao: Objeto da questão (QuestaoObjetiva, QuestaoVerdadeiroFalso ou QuestaoSubjetiva).
    
    Retorna:
        Uma string formatada representando a questão.
    """
    if isinstance(questao, QuestaoObjetiva):
        return (
            f"{questao.enunciado}\n"
            f"A) {questao.alternativa_a}\n"
            f"B) {questao.alternativa_b}\n"
            f"C) {questao.alternativa_c}\n"
            f"D) {questao.alternativa_d}\n"
            f"E) {questao.alternativa_e}\n"
            f"Resposta correta: {questao.resposta_correta.upper()}\n"
        )
    
    elif isinstance(questao, QuestaoVerdadeiroFalso):
        return (
            f"{questao.enunciado}\n"
            f"Resposta correta: {'Verdadeiro' if questao.resposta_correta == 'V' else 'Falso'}\n"
        )
    
    elif isinstance(questao, QuestaoSubjetiva):
        return (
            f"{questao.enunciado}\n"
            f"Resposta correta: {questao.resposta_correta if questao.resposta_correta else 'Não fornecida'}\n"
        )
    
    return "Questão inválida"

# ------------------------------------------------------------
# Função para garantir que as questões estão em formato Pydantic
# ------------------------------------------------------------
def prepare_questions_for_pdf(questions):
    """
    Converte dicionários retornados da API para instâncias dos modelos Pydantic, se necessário,
    e filtra questões inválidas.
    
    Parâmetros:
        questions (list): Lista de questões (podem ser dicionários ou instâncias de QuestaoObjetiva).
    
    Retorna:
        Lista de questões formatadas corretamente.
    """
    formatted_questions = []
    for question in questions:
        if isinstance(question, dict):  # Converte dicionário para modelo Pydantic
            formatted_questions.append(QuestaoObjetiva.model_validate(question))
        elif isinstance(question, QuestaoObjetiva):
            formatted_questions.append(question)
        else:
            print(f"Questão inválida detectada: {question}")
    
    return formatted_questions

# ------------------------------------------------------------
# Função principal que orquestra o fluxo do protótipo
# ------------------------------------------------------------
def main():
    """
    Função principal que executa o fluxo completo:
      - Autenticação e criação do cliente da API Classroom.
      - Listagem e seleção de curso e coursework.
      - Listagem de submissões e escolha de um anexo.
      - Processamento do anexo para extrair o conteúdo.
      - Geração de questões a partir do conteúdo com a API da OpenAI.
      - Preparação e exibição das questões.
      - Geração de um PDF com as questões personalizadas.
    """
    # Autentica e cria o cliente da API Classroom
    creds = get_google_credentials()
    classroom_service = build('classroom', 'v1', credentials=creds)

    # Listar e escolher curso
    courses = list_courses(classroom_service)
    if not courses:
        print("Nenhum curso disponível.")
        return
    
    selected_course = choose_course(courses)
    course_id = selected_course.get('id')

    # Exibir detalhes e tópicos do curso
    show_course_details(classroom_service, selected_course)
    list_topics(classroom_service, course_id)

    # Listar e escolher coursework
    courseworks = list_courseworks(classroom_service, course_id)
    if not courseworks:
        print("Nenhum trabalho disponível.")
        return
    
    selected_coursework = choose_coursework(courseworks)
    cw_id = selected_coursework.get('id')

    # Listar e escolher submissão
    submissions = list_submissions(classroom_service, course_id, cw_id, creds)
    if not submissions:
        print("Nenhuma submissão encontrada.")
        return
    
    selected_submission = choose_submission(submissions)
    student_name = get_student_name(selected_submission, classroom_service)

    # Obter e escolher anexo
    attachments = get_submission_attachments(selected_submission)
    if not attachments:
        print("Nenhum anexo encontrado na submissão.")
        return
    
    selected_attachment = choose_attachment(attachments)

    # Processar o anexo escolhido (baixar ou fazer requisição)
    resposta_aluno = process_attachment(selected_attachment, creds)
    if not resposta_aluno:
        print("Erro ao processar anexo. Resposta do aluno não encontrada.")
        return

    # Gerar questão a partir da resposta do aluno
    generated_question = generate_questions(resposta_aluno)
    if not generated_question:
        print("Erro ao gerar questão com OpenAI.")
        return

    # Preparar as questões para geração do PDF
    questions = prepare_questions_for_pdf([generated_question])
    if not questions:
        print("Não foi possível processar as questões.")
        return

    # Exibir as questões geradas antes de gerar o PDF
    print("\nQuestões geradas:")
    for idx, questao in enumerate(questions, start=1):
        print(f"\nQuestão {idx}:")
        print(questao.model_dump_json(indent=2))

    # Gerar PDF com as questões
    print("\nGerando PDF com as questões...")
    create_pdf(student_name, questions)
    

if __name__ == '__main__':
    main()