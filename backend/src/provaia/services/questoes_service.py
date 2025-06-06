# provaia/src/provaia/services/questoes_service.py


"""
===============================================================================
SERVIÇO DE GERAÇÃO DE QUESTÕES PERSONALIZADAS (QUESTOES_SERVICE)
===============================================================================

Este módulo implementa a lógica principal para a geração automatizada de questões
personalizadas com base nas submissões dos alunos obtidas através do Google Classroom.
Utiliza integrações com serviços do Google Classroom, OpenAI e geração de PDFs.

===============================================================================
FUNCIONALIDADES
===============================================================================
1. **Obtenção do Conteúdo das Submissões**:
   - Obtém código-fonte submetido pelos alunos diretamente do Google Classroom.

2. **Geração de Questões via OpenAI**:
   - Utiliza a API da OpenAI para gerar questões objetivas, verdadeiro/falso e discursivas,
     personalizadas com base no código fonte submetido pelo aluno.

3. **Geração de PDFs Personalizados**:
   - Cria documentos PDF individuais contendo as questões geradas, organizadas
     por aluno.

===============================================================================
CLASSES E MÉTODOS PRINCIPAIS
===============================================================================
- **Função: processar_submissao**
    - Obtém conteúdo da submissão do aluno.
    - Gera questões personalizadas usando a API da OpenAI.
    - Retorna um dicionário contendo nome do aluno e questões geradas.

===============================================================================
COMO UTILIZAR
===============================================================================

- Exemplo de uso básico:

```python
resultado = processar_submissao(course_id="12345", 
                                coursework_id="67890", 
                                submission_id="ABCDEF")
print(resultado)
```

===============================================================================
DEPENDÊNCIAS
===============================================================================
- Integrações internas:
  - `classroom_service`: Obtém dados do Google Classroom.
  - `openai_service`: Geração automática de questões.
  - `pdf_service`: Criação de PDFs personalizados.

- Bibliotecas externas:
  - FastAPI
  - Pydantic

===============================================================================
AUTOR
===============================================================================
- Autor: Paulo César Rodacki Gomes
- Email: rodacki@gmail.com
- Data: 10/03/2025
===============================================================================
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
from typing import Dict, List, Union
from fastapi import HTTPException
from pydantic import ValidationError
import json
from src.provaia.services.classroom_service import obter_conteudo_submissao
from src.provaia.services.file_service import obter_nome_aluno_por_arquivo
from src.provaia.services.openai_service import generate_questions
from src.provaia.services.pdf_service import create_pdf
from src.provaia.schemas.questoes import (
    QuestaoObjetiva, 
    QuestaoVerdadeiroFalso, 
    QuestaoSubjetiva, 
    ConjuntoQuestoes
)

# ----------------------------------------------------------------------------
# FUNÇÕES
# ----------------------------------------------------------------------------
async def processar_submissao(course_id: str, coursework_id: str, submission_id: str) -> Dict[str, Union[str, Dict]]:
    """
    Processa uma submissão específica do aluno, gerando questões personalizadas a partir do conteúdo enviado.
    """

    # Obtém o conteúdo submetido pelo aluno
    conteudo_submissao, file_id = obter_conteudo_submissao(course_id, coursework_id, submission_id)
    if not conteudo_submissao or not file_id:
        return {"error": "Não foi possível obter o conteúdo da submissão"}

    # Obtém o nome do aluno que realizou a submissão
    nome_aluno = obter_nome_aluno_por_arquivo(file_id)

    # 🚀 Garante que a chamada assíncrona seja awaitada corretamente
    questoes_response = await generate_questions(conteudo_submissao)


    # CODIGO DE DEBUG
    try: 
        # Certifique-se de que há escolhas válidas
        if not questoes_response.choices:
            raise ValueError("Resposta do OpenAI não contém 'choices'.")

        # Acessa diretamente o objeto estruturado gerado pelo structured_outputs
        questoes = questoes_response.choices[0].message.parsed  # Já é um objeto Pydantic do tipo ConjuntoQuestoes

        # 🔍 Debug: Exibir o objeto Pydantic extraído
        print("✅ Objeto Pydantic extraído da resposta:", questoes)

        # Converte o objeto Pydantic para dicionário antes de retorná-lo na API
        questoes_dict = questoes.model_dump() 
        # 🔍 Debug: Exibir o objeto Pydantic extraído
        print("✅ questoes_dict:", questoes_dict)

         # Retorna resultado corrigido com código-fonte incluído
        response_data = {
            "aluno": nome_aluno,
            "codigo_fonte": conteudo_submissao,  # ✅ Inclui o código-fonte na resposta
            "questoes": questoes_dict,  # ✅ Corrige conversão do objeto Pydantic
            "pdf": None  # Alterar se necessário
        }

        try:
            json.dumps(response_data)  # Testa se é JSON válido
            print("✅ Resposta JSON válida para retorno.")
        except TypeError as e:
            print("❌ ERRO: Resposta contém tipos não serializáveis para JSON!", str(e))
            raise HTTPException(status_code=500, detail="Erro ao processar resposta - tipo não serializável.")

        return response_data
    
    except ValidationError as e:
        print("❌ Erro de validação Pydantic:", str(e))
        raise HTTPException(status_code=400, detail="Erro ao validar resposta gerada pelo OpenAI.")


    except AttributeError as e:
        print("❌ Erro ao acessar atributos do objeto retornado:", str(e))
        raise HTTPException(status_code=400, detail="Erro ao processar resposta do OpenAI: formato inesperado")

    except Exception as e:
        print("❌ Erro inesperado:", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao processar questões")




async def gerar_questoes_para_aluno(course_id: str, coursework_id: str, submission_id: str):
    """
    Gera questões de prova para um aluno a partir do conteúdo de uma submissão.

    Esta função realiza os seguintes passos:
      1. Obtém o conteúdo da submissão usando o identificador do curso, exercício e submissão.
      2. Recupera o nome do aluno associado à submissão.
      3. Gera uma questão de prova utilizando a API OpenAI com base no conteúdo obtido.
      4. Cria um arquivo PDF contendo a questão gerada e o nome do aluno.
    
    Parâmetros:
        - course_id (str): Identificador do curso no Google Classroom.
        - coursework_id (str): Identificador do exercício associado à submissão.
        - submission_id (str): Identificador da submissão do aluno.

    Retorna:
        Dict[str, Any]:
            - "aluno": Nome completo do aluno.
            - "questoes": Lista contendo a(s) questão(ões) gerada(s), no formato de dicionário.
            - "pdf": Caminho do arquivo PDF gerado.
            - Em caso de falha, retorna um dicionário com a chave "erro" e uma mensagem descritiva.

    Exemplo:
        resultado = gerar_questoes_para_aluno("curso123", "cw456", "sub789")
        if "erro" in resultado:
            print("Erro:", resultado["erro"])
        else:
            print("PDF gerado:", resultado["pdf"])
    """
    conteudo_resposta, file_id = obter_conteudo_submissao(course_id, coursework_id, submission_id)
    if not conteudo_resposta or not file_id:
        return {"erro": "Não foi possível obter o conteúdo da submissão"}

    aluno = obter_nome_aluno_por_arquivo(submission_id)
    questao = await generate_questions(conteudo_resposta)

    # Criar PDF
    #pdf_path = create_pdf(aluno, [questao])

    return {"aluno": aluno, "questoes": [questao.model_dump()], "pdf": None}

