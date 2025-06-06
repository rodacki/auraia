"""
===============================================================================
SCHEMAS PARA QUESTÕES DE AVALIAÇÕES (schemas/questoes.py)
===============================================================================
Este módulo define os schemas (modelos) para representar questões utilizadas
nas avaliações geradas pelo sistema ProvaIA. São definidos modelos específicos
para questões objetivas (múltipla escolha), questões de verdadeiro ou falso, 
e questões subjetivas (discursivas).

Estes schemas são utilizados para validação, formatação e manipulação de dados
das questões geradas automaticamente pela integração com IA (OpenAI).

===============================================================================
ESTRUTURAS DE DADOS DEFINIDAS
===============================================================================
- Questão Objetiva (QuestaoObjetiva):
  - Representa questões de múltipla escolha com alternativas A-E e indicação
    da resposta correta.

- Questão Verdadeiro ou Falso (QuestaoVerdadeiroFalso):
  - Representa questões que admitem respostas apenas como "Verdadeiro" ou "Falso".

- Questão Subjetiva (QuestaoSubjetiva):
  - Representa questões discursivas abertas, podendo conter ou não uma sugestão
    de resposta correta.

- Conjunto de Questões (ConjuntoQuestoes):
  - Agrupa os três tipos de questões (objetiva, verdadeiro/falso e subjetiva)
    para composição das provas geradas.

===============================================================================
COMO USAR
===============================================================================
Esses modelos são utilizados principalmente nas interações com a API e na geração
das provas em PDF:

Exemplo:

```python
questao_objetiva = QuestaoObjetiva(
    enunciado="Qual é o resultado de 2+2?",
    alternativa_a="3",
    alternativa_b="4",
    alternativa_c="5",
    alternativa_d="6",
    alternativa_e="7",
    resposta_correta="b"
)

questao_vf = QuestaoVerdadeiroFalso(
    enunciado="Python é uma linguagem tipada dinamicamente.",
    resposta_correta="V"
)

questao_subjetiva = QuestaoSubjetiva(
    enunciado="Explique o conceito de recursão.",
    resposta_correta=None
)

conjunto = ConjuntoQuestoes(
    objetiva=questao_objetiva,
    vf=questao_vf,
    subjetiva=questao_subjetiva
)
```

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
from typing import Literal, Optional
from pydantic import BaseModel

# ----------------------------------------
# DEFINIÇÕES DE MODELOS
# ----------------------------------------

class QuestaoObjetiva(BaseModel):
    """Modelo para questão objetiva (múltipla escolha)."""
    enunciado: str
    alternativa_a: str
    alternativa_b: str
    alternativa_c: str
    alternativa_d: str
    alternativa_e: str
    resposta_correta: Literal['a', 'b', 'c', 'd', 'e']


class QuestaoVerdadeiroFalso(BaseModel):
    """Modelo para questão de verdadeiro ou falso."""
    enunciado: str
    resposta_correta: Literal['V', 'F']


class QuestaoSubjetiva(BaseModel):
    """Modelo para questão subjetiva (discursiva)."""
    enunciado: str
    resposta_correta: Optional[str] = None


class ConjuntoQuestoes(BaseModel):
    """Modelo que agrupa diferentes tipos de questões em um único conjunto."""
    objetiva: QuestaoObjetiva
    vf: QuestaoVerdadeiroFalso
    subjetiva: QuestaoSubjetiva

# ----------------------------------------
# FIM DO MÓDULO
# ----------------------------------------
