from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime, date
from .questoes import ConjuntoQuestoes
from .classroom import Student

# 🔹 Definição do modelo de entrada (requisição)
class SourceCodeRequest(BaseModel):
    sourceCode: str

class Attachment(BaseModel):
    """Representa um arquivo submetido pelo aluno, que pode ser acessado no Google Drive do professor."""

    id: str  # Identificador único do anexo (arquivo).
    name: str  # Nome do arquivo submetido.
    file_url: HttpUrl  # URL para recuperar o arquivo no Google Drive.
    mime_type: Optional[str] = None  # Tipo MIME do arquivo (exemplo: "text/x-python", "application/pdf").


class StudentSubmission(BaseModel):
    """Representa a submissão de um aluno em uma atividade prática (Coursework)."""

    id: str  # Identificador único da submissão.
    student_id: str  # Identificador único do aluno que fez a submissão.
    coursework_id: str  # Identificador da atividade à qual essa submissão pertence.
    submission_time: datetime  # Data e hora em que a submissão foi realizada.
    attachments: List[Attachment]  # Lista de arquivos submetidos pelo aluno.
    status: str  # Status da submissão (exemplos: "TURNED_IN" - entregue, "RETURNED" - corrigida, "DRAFT" - rascunho).


class Coursework(BaseModel):
    """Representa uma atividade prática dentro de um curso."""

    id: str  # Identificador único da atividade.
    title: str  # Título da atividade.
    description: Optional[str] = None  # Descrição da atividade (pode ser opcional).
    topic_id: Optional[str] = None  # Identificador do tópico ao qual essa atividade pertence (se aplicável).
    due_date: Optional[datetime] = None  # Data e hora de entrega da atividade (se houver prazo definido).
    submissions: List[StudentSubmission] = []  # Lista de submissões feitas pelos alunos nessa atividade.


class Topic(BaseModel):
    """Representa um tópico dentro de um curso (exemplo: "Programação em Python", "Banco de Dados")."""

    id: str  # Identificador único do tópico.
    name: str  # Nome do tópico.
    course_id: str  # Identificador do curso ao qual este tópico pertence.


class Course(BaseModel):
    """Representa um curso dentro do Google Classroom."""

    id: str  # Identificador único do curso.
    name: str  # Nome do curso (exemplo: "Introdução à Programação").
    section: Optional[str] = None  # Seção do curso (exemplo: "Turma A - 2024").
    description: Optional[str] = None  # Descrição do curso (pode conter detalhes adicionais).
    topics: List[Topic] = []  # Lista de tópicos associados ao curso.
    coursework: List[Coursework] = []  # Lista de atividades (Coursework) dentro do curso.


class StudentExamQuestion(BaseModel):
    """Representa uma questão da prova individual de um estudante."""

    student_submission_id: str  # ID da submissão do aluno usada para gerar as questões.
    source_code: str  # Código-fonte selecionado aleatoriamente de um dos anexos da submissão.
    subQuestions: ConjuntoQuestoes  # Objeto contendo as subquestões geradas a partir do código-fonte.


class StudentExam(BaseModel):
    """Representa a prova completa de um estudante, contendo várias questões."""

    studentId: str  # ID do estudante que realizará a prova.
    questions: List[StudentExamQuestion]  # Lista de questões da prova (o tamanho corresponde a `num_questions` de Evaluation).


class Evaluation(BaseModel):
    """Representa uma avaliação criada pelo usuário no sistema."""

    id: str  # Identificador único da avaliação (gerado pelo frontend).
    course: Course  # Curso ao qual essa avaliação pertence.
    title: str  # Título da avaliação (exemplo: "Prova Final de Algoritmos").
    date: date  # Data da avaliação (formato YYYY-MM-DD).
    num_questions: int  # Número total de questões na avaliação.
    selected_courseworks: List[str]  # Lista de IDs de atividades selecionadas para gerar questões.
    selected_students: List[Student]  # Lista de IDs dos alunos selecionados para realizar a avaliação.
    student_exams: List[StudentExam] = []  # Mapeia cada estudante para sua prova individual.