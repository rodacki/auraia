# provaia/src/provaia/services/file_service.py

"""
===============================================================================
SERVIÇOS DE ARQUIVOS – Google Drive
===============================================================================

Este módulo fornece funcionalidades para interação com a API do Google Drive, 
permitindo o download de arquivos armazenados no Google Drive utilizando 
autenticação via OAuth2.

===============================================================================
FUNCIONALIDADES
===============================================================================

- **Cliente do Google Drive**:
  - Obtenção de cliente autenticado para interagir com o Google Drive.

- **Download de arquivos**:
  - Função para baixar arquivos diretamente do Google Drive usando seu `file_id`.

===============================================================================
EXEMPLOS DE USO
===============================================================================

- Baixar um arquivo do Google Drive usando o ID do arquivo:
  ```python
  conteudo = baixar_arquivo_drive("1A2B3C4D5E6")
  print(conteudo)
  ```

===============================================================================
DEPENDÊNCIAS
===============================================================================

- Bibliotecas Python:
  - `google-api-python-client`
  - `google-auth`
  - `google-auth-oauthlib`
  - `io` (biblioteca padrão)

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
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from src.provaia.services.auth_service import get_google_credentials
from typing import List
from src.provaia.schemas.geral import Attachment

# ----------------------------------------
# CLIENTE DO GOOGLE DRIVE
# ----------------------------------------
def get_drive_service():
    """
    Retorna um cliente autenticado para interagir com a API do Google Drive.

    Retorna:
        Resource: Cliente autenticado para a API do Google Drive.
    """
    creds = get_google_credentials()
    return build("drive", "v3", credentials=creds)


# ----------------------------------------
# DOWNLOAD DE ARQUIVOS DO GOOGLE DRIVE
# ----------------------------------------
def baixar_arquivo_drive(file_id: str) -> str:
    """
    Realiza o download de um arquivo do Google Drive dado seu identificador único.

    Args:
        file_id (str): O identificador único do arquivo no Google Drive.

    Retorna:
        str: Conteúdo do arquivo baixado, convertido para texto (UTF-8).

    Exemplo:
        ```python
        conteudo = baixar_arquivo_drive("1ab23cd4EfG5h6Ij")
        print(conteudo)
        ```

    Efeitos colaterais:
        - Exibe progresso do download no console.

    Tratamento de erros:
        - Caso ocorra algum erro durante o download, exibe uma mensagem e retorna `None`.
    """
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    print("\nBaixando arquivo do Google Drive...")

    try:
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"Download: {int(status.progress() * 100)}% concluído.")

        file_content = fh.getvalue().decode("utf-8")  # Convertendo para string UTF-8
        print(f"file_service.py - Conteudo do arquivo:\n{file_content}")
        return file_content


    except Exception as e:
        print(f"Erro ao baixar arquivo do Drive: {e}")
        return None

# ----------------------------------------
# OBTENÇÃO DE METADADOS DO DRIVE (Novo)
# ----------------------------------------
def obter_nome_aluno_por_arquivo(file_id: str) -> str:
    """
    Obtém o nome do aluno com base no proprietário do arquivo no Google Drive.

    Args:
        file_id (str): ID do arquivo no Google Drive.

    Retorna:
        str: Nome do dono do arquivo (aluno), ou 'Nome não encontrado' se não puder ser obtido.
    """
    try:
        service = get_drive_service()
        file_metadata = service.files().get(fileId=file_id, fields="owners, name").execute()
        owner_name = file_metadata.get("owners", [{}])[0].get("displayName", "Desconhecido")
        
        print(f"📂 Arquivo enviado por: {owner_name} | Nome do arquivo: {file_metadata.get('name')}")
        return owner_name

    except Exception as e:
        print(f"❌ Erro ao obter nome do aluno via Drive API: {e}")
        return "Erro ao obter nome"
    
# def obter_arquivos_submissao(attachments: List[dict]) -> List[Attachment]:
#     """
#     Processa a lista de anexos de uma submissão e retorna os metadados dos arquivos.

#     Args:
#         attachments (List[dict]): Lista de anexos da submissão, obtida da API do Google Classroom.

#     Retorna:
#         List[Attachment]: Lista de objetos Attachment com ID, nome, URL de download e tipo MIME.
#     """
#     arquivos = []

#     for attachment in attachments:
#         if "driveFile" in attachment:
#             drive_file = attachment["driveFile"]
#             file_id = drive_file["id"]
#             file_name = drive_file.get("title", "Arquivo sem nome")
#             mime_type = drive_file.get("mimeType", None)

#             # Gerar URL de download
#             file_url = f"https://drive.google.com/uc?export=download&id={file_id}"

#             arquivos.append(Attachment(id=file_id, name=file_name, file_url=file_url, mime_type=mime_type))

#     return arquivos

def obter_arquivos_submissao(attachments: List[dict]) -> List[Attachment]:
    """
    Processa a lista de anexos de uma submissão e retorna os metadados dos arquivos.

    Args:
        attachments (List[dict]): Lista de anexos da submissão, obtida da API do Google Classroom.

    Retorna:
        List[Attachment]: Lista de objetos Attachment com ID, nome, URL de download e tipo MIME.
    """
    arquivos = []

    for attachment in attachments:
        if "driveFile" in attachment:
            drive_file = attachment["driveFile"]
            file_id = drive_file["id"]
            file_name = drive_file.get("title", "Arquivo sem nome")
            file_link = drive_file.get("alternateLink")  # 🔹 Corrigindo acesso ao link
            mime_type = drive_file.get("mimeType", None)

            # 🔹 Gerar URL direta de download do arquivo no Google Drive
            download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"

            arquivos.append(
                Attachment(id=file_id, name=file_name, file_url=download_url, mime_type=mime_type)
            )

    if not arquivos:
        print("❌ Nenhum arquivo extraído corretamente dos anexos.")
    
    return arquivos