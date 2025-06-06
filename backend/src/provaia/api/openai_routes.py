# # provaia/src/provaia/api/openai_routes.py



"""
===============================================================================
ROTAS PARA INTEGRAÇÃO COM OPENAI
===============================================================================
Este módulo contém as rotas (endpoints) relacionadas à interação com a API da OpenAI
para geração automática de questões com base no conteúdo submetido pelos alunos.

As rotas permitem ao frontend enviar código fonte submetido pelos alunos e obter
questões de avaliação geradas automaticamente pela IA generativa (OpenAI).

===============================================================================
FUNCIONALIDADES
===============================================================================
- **Geração de Questões**:
    - Cria questões automaticamente a partir do conteúdo fornecido.
    - Suporta geração de questões de múltipla escolha, verdadeiro/falso e discursivas.

===============================================================================
ENDPOINTS
===============================================================================
- `POST /gerar_questao`
    - Recebe código submetido pelo aluno e retorna questões geradas pela IA.

===============================================================================
DEPENDÊNCIAS
===============================================================================
- FastAPI
- Serviços internos:
  - `openai_service`

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
from fastapi import APIRouter, HTTPException
from src.provaia.services.openai_service import generate_questions
from src.provaia.schemas.questoes import ConjuntoQuestoes

# ----------------------------------------
# CONFIGURAÇÕES DE ROTAS
# ----------------------------------------
router = APIRouter(prefix="/openai", tags=["OpenAI"])


# ----------------------------------------
# ENDPOINTS
# ----------------------------------------
# @router.post("/gerar_questao")
# async def gerar_questao(conteudo: dict):
#     """
#     Gera uma questão de múltipla escolha com base no conteúdo enviado pelo usuário.

#     **Exemplo de requisição:**
#     ```json
#     {
#         "conteudo_resposta": "print('Hello, world!')"
#     }

#     Parâmetros:
#         conteudo (dict): Um dicionário contendo o código ou texto submetido pelo aluno,
#                          estruturado como no exemplo acima.

#     Retorna:
#         dict: Uma questão de múltipla escolha gerada pela IA, incluindo alternativas e resposta correta.

#     Exceções:
#         HTTPException: Retorna erro HTTP caso falhe a geração da questão.
#     """
#     if "conteudo_resposta" not in conteudo:
#         raise HTTPException(status_code=400, detail="Campo 'conteudo_resposta' é obrigatório.")

#     questao = generate_questions(conteudo["conteudo_resposta"])
#     return {"questao": questao.model_dump()}

@router.post("/gerar_questao", response_model=ConjuntoQuestoes)
async def gerar_questao(conteudo: dict):
    """
    Gera um conjunto de questões (objetiva, VF e discursiva) a partir do código enviado.

    **Exemplo de requisição:**
    ```json
    {
        "conteudo_resposta": "print('Hello, world!')"
    }
    ```

    **Parâmetros:**
    - `conteudo (dict)`: Código ou texto submetido pelo aluno.

    **Retorno:**
    - `ConjuntoQuestoes`: Um objeto contendo três questões (objetiva, VF e discursiva).

    **Erros:**
    - Retorna 400 se o campo 'conteudo_resposta' estiver ausente.
    - Retorna 500 se a geração das questões falhar.
    """
    if "conteudo_resposta" not in conteudo:
        raise HTTPException(status_code=400, detail="Campo 'conteudo_resposta' é obrigatório.")

    try:
        questoes = await generate_questions(conteudo["conteudo_resposta"])
         # ✅ Garantimos que a resposta seja um objeto do tipo ConjuntoQuestoes
        if not isinstance(questoes, ConjuntoQuestoes):
            print("🔍 Converting to ConjuntoQuestoes:", questoes)
            questoes = ConjuntoQuestoes(**questoes.model_dump())  # Conversão 
        return questoes  # Retorna um objeto Pydantic
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar questões: {str(e)}")