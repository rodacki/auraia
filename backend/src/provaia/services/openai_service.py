# provaia/src/provaia/services/openai_service.py
"""
===============================================================================
SERVIÇO DE INTEGRAÇÃO COM A OPENAI
===============================================================================
Este módulo fornece integração com a API da OpenAI para geração automática de
questões personalizadas com base no conteúdo fornecido pelos alunos.

Utiliza o modelo GPT-4o para gerar três tipos diferentes de questões:
- Questão de múltipla escolha
- Questão de verdadeiro ou falso
- Questão discursiva

===============================================================================
FUNCIONALIDADES
===============================================================================
- Envia código ou texto do aluno para a API da OpenAI.
- Recebe e processa respostas no formato JSON.
- Converte respostas da OpenAI em modelos Pydantic para validação e padronização.

===============================================================================
DEPENDÊNCIAS
===============================================================================
- openai
- src.provaia.config (para configuração das chaves de API)
- src.provaia.schemas.questoes (para modelos Pydantic das questões)

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
from openai import OpenAI
from pydantic import ValidationError
from fastapi import HTTPException
from src.provaia.config import settings
from src.provaia.schemas.questoes import (
    QuestaoObjetiva, 
    QuestaoVerdadeiroFalso, 
    QuestaoSubjetiva, 
    ConjuntoQuestoes
)
from typing import List
import json

# ----------------------------------------
# CONFIGURAÇÃO
# ----------------------------------------
openai = OpenAI(api_key=settings.OPENAI_API_KEY)

# ----------------------------------------
# FUNÇÕES
# ----------------------------------------

async def generate_questions(source_code: str) -> ConjuntoQuestoes:
    """Gera questões a partir do código-fonte utilizando a API OpenAI e Structured Outputs."""

    try:
        completion = openai.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Gere três questões com base no código-fonte do aluno:\n"
                                              "1) Uma questão objetiva (múltipla escolha).\n"
                                              "2) Uma questão de verdadeiro ou falso.\n"
                                              "3) Uma questão subjetiva (discursiva)."},
                {"role": "user", "content": f"Aqui está o código-fonte do aluno:\n{source_code}"},
            ],
            response_format=ConjuntoQuestoes,  # ✅ OpenAI já retorna o objeto estruturado
        )


        # 📌 O retorno de `parse()` contém um objeto OpenAI. Extraímos apenas o `choices[0].message.parsed`
        if not completion.choices:
            raise ValueError("A resposta da OpenAI não contém 'choices'.")

        questoes: ConjuntoQuestoes = completion.choices[0].message.parsed  # ✅ Pegamos apenas a estrutura de questões

        # 🔍 Debug: Exibir a resposta final
        print("✅ Questões geradas corretamente:", questoes)


        return questoes  # ✅ Retorna diretamente um objeto ConjuntoQuestoes

    except Exception as e:
        print(f"❌ Erro ao chamar OpenAI: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar questões: {str(e)}")






