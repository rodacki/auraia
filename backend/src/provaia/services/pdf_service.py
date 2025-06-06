

"""
===============================================================================
PDF SERVICE
===============================================================================
Este módulo contém a função responsável pela geração de arquivos PDF com questões
personalizadas de avaliações geradas pelo sistema **ProvaIA**.

O objetivo deste módulo é gerar arquivos PDF individuais, contendo as questões 
de prova personalizadas geradas com base nas respostas dos alunos via Google Classroom.

===============================================================================
FUNCIONALIDADES
===============================================================================

- **Geração de PDFs**:
  - Criação de arquivos PDF com as questões geradas.
  - Formatação clara e legível para facilitar o uso pelo aluno.

===============================================================================
USO
===============================================================================

Exemplo de uso:

```python
from src.provaia.schemas.questoes import QuestaoObjetiva

questoes = [
    QuestaoObjetiva(
        enunciado="Qual a saída do código?",
        alternativa_a="10",
        alternativa_b="20",
        alternativa_c="30",
        alternativa_d="40",
        alternativa_e="50",
        resposta_correta="b"
    )
]

create_pdf("Nome Aluno", questoes)
```

===============================================================================
DEPENDÊNCIAS
===============================================================================

- **FPDF**: Utilizada para gerar arquivos PDF.
- **schemas.questoes**: Modelos Pydantic para questões.

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
from typing import List
from fpdf import FPDF
from src.provaia.schemas.questoes import ConjuntoQuestoes


# ----------------------------------------
# Função para geração do PDF
# ----------------------------------------
async def create_pdf(aluno: str, questions: ConjuntoQuestoes) -> str:
    """
    Gera um PDF contendo as questões geradas pela OpenAI no formato adequado.

    Args:
        aluno (str): Nome do aluno.
        questions (ConjuntoQuestoes): Objeto contendo as questões objetiva, VF e subjetiva.

    Returns:
        str: Caminho do arquivo PDF gerado.
    """

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)

    # Cabeçalho
    pdf.cell(200, 10, f"Avaliação - {aluno}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    # Questão Objetiva
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 8, "Questão Objetiva:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 6, questions.objetiva.enunciado)
    pdf.ln(5)
    pdf.cell(0, 6, f"A) {questions.objetiva.alternativa_a}", ln=True)
    pdf.cell(0, 6, f"B) {questions.objetiva.alternativa_b}", ln=True)
    pdf.cell(0, 6, f"C) {questions.objetiva.alternativa_c}", ln=True)
    pdf.cell(0, 6, f"D) {questions.objetiva.alternativa_d}", ln=True)
    pdf.cell(0, 6, f"E) {questions.objetiva.alternativa_e}", ln=True)
    pdf.ln(10)

    # Questão Verdadeiro ou Falso
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 8, "Questão de Verdadeiro ou Falso:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 6, questions.vf.enunciado)
    pdf.ln(5)

    # Questão Subjetiva
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 8, "Questão Discursiva:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 6, questions.subjetiva.enunciado)
    pdf.ln(10)

    # Caminho do arquivo PDF
    pdf_filename = f"avaliacao_{aluno.replace(' ', '_')}.pdf"
    pdf.output(pdf_filename)

    return pdf_filename
