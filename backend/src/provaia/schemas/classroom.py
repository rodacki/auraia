

"""
===============================================================================
SCHEMAS PARA INTEGRAÇÃO COM GOOGLE CLASSROOM
===============================================================================
Este módulo contém as definições dos modelos de dados (schemas) utilizados 
para representar entidades provenientes do Google Classroom no 
sistema **ProvaIA**.

Estes schemas são utilizados para:
  - Validar e estruturar os dados recebidos da API do Google Classroom.
  - Garantir consistência dos dados ao longo das operações internas do backend.

===============================================================================
MODELOS DISPONÍVEIS
===============================================================================
1. **Course**:
    Representa informações básicas sobre cursos obtidos do Google Classroom.

2. **CourseWork**:
   Representa um trabalho (atividade, exercício ou tarefa) atribuído pelo 
   professor em um curso específico.

3. **StudentSubmission**:
   - Representa as submissões feitas pelos alunos para uma atividade específica.

===============================================================================
AUTORES
===============================================================================
- Paulo César Rodacki Gomes
- Email: rodacki@gmail.com
- Data: 10/03/2025

===============================================================================
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
from pydantic import BaseModel, EmailStr
from typing import Optional

# ----------------------------------------
# Modelos para Google Classroom
# ----------------------------------------

class Course(BaseModel):
    """
    Representa um curso obtido através da integração com a API do Google Classroom.

    Attributes:
        id (str): Identificador único do curso no Google Classroom.
        name (str): Nome do curso.
        section (Optional[str]): Seção ou turma específica (opcional).
        description (Optional[str]): Descrição detalhada do curso (opcional).
        owner_id (Optional[str]): Identificador do proprietário (professor responsável)
             do curso (opcional).
    """
    id: str
    name: str
    section: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[str] = None


class CourseWork(BaseModel):
    """
    Representa uma atividade (coursework) em um curso do Google Classroom.

    Attributes:
        id (str): Identificador único da atividade.
        course_id (str): Identificador do curso ao qual a atividade pertence.
        title (str): Título da atividade.
        description (Optional[str]): Descrição detalhada da atividade (opcional).
        due_date (Optional[str]): Data de entrega da atividade, em formato de string (opcional).
        max_points (Optional[float]): Pontuação máxima que pode ser atribuída à atividade (opcional).
    """
    id: str
    course_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    max_points: Optional[float] = None
    


class StudentSubmission(BaseModel):
    """
    Representa uma submissão realizada por um aluno em uma atividade específica no Google Classroom.

    Attributes:
        id (str): Identificador único da submissão no Google Classroom.
        course_id (str): Identificador do curso ao qual pertence a submissão.
        coursework_id (str): Identificador da atividade a qual esta submissão está associada.
        user_id (str): Identificador do usuário (aluno) que realizou a submissão.
        state (str): Estado atual da submissão (e.g., "CREATED", "TURNED_IN", "RETURNED").
        assigned_grade (Optional[float]): Nota atribuída pelo professor (opcional).
    """
    id: str
    course_id: str
    coursework_id: str
    user_id: str
    state: str
    assigned_grade: Optional[float] = None


class Student(BaseModel):
    id: str  # ID único do aluno no Google Classroom
    name: str  # Nome completo do aluno
    email: Optional[EmailStr] = None  # E-mail do aluno (opcional)
    photoUrl: Optional[str] = None  # URL da foto do aluno (opcional)

# ----------------------------------------
# FIM DO MÓDULO
# ----------------------------------------
