import os
import base64
import requests

def upload_files_to_sharepoint(logger, access_token, sharepoint_folder_url, local_file_paths):
    """
    Faz upload de arquivos ou diretórios inteiros para uma pasta no SharePoint.
    Substitui arquivos com o mesmo nome automaticamente.

    Args:
        logger: Objeto logger para registrar logs.
        access_token (str): Token de autenticação Microsoft Graph.
        sharepoint_folder_url (str): URL da pasta no SharePoint.
        local_file_paths (List[str]): Lista de caminhos de arquivos ou diretórios.

    Returns:
        List[str]: Lista de URLs dos arquivos enviados com sucesso.
    """
    try:
        logger.info("SharePoint Upload - Iniciando upload de múltiplos arquivos...")

        # Codifica a URL da pasta para shareId
        encoded_url = base64.b64encode(sharepoint_folder_url.encode('utf-8')).decode('utf-8')
        share_id = f'u!{encoded_url.replace("/", "_").replace("+", "-").rstrip("=")}'

        # Resolve a URL da pasta para pegar o driveId e itemId
        folder_metadata_url = f"https://graph.microsoft.com/v1.0/shares/{share_id}/driveItem"
        metadata_response = requests.get(folder_metadata_url, headers={"Authorization": f"Bearer {access_token}"})
        metadata_response.raise_for_status()
        folder_item = metadata_response.json()

        drive_id = folder_item["parentReference"]["driveId"]
        folder_item_id = folder_item["id"]

        uploaded_urls = []

        for path in local_file_paths:
            if os.path.isdir(path):
                # Percorre arquivos dentro do diretório
                for root, _, files in os.walk(path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        url = upload_single_file(full_path, file, drive_id, folder_item_id, access_token, logger)
                        if url:
                            uploaded_urls.append(url)
            elif os.path.isfile(path):
                file_name = os.path.basename(path)
                url = upload_single_file(path, file_name, drive_id, folder_item_id, access_token, logger)
                if url:
                    uploaded_urls.append(url)
            else:
                logger.warning(f"Caminho inválido ignorado: {path}")

        logger.info(f"Upload concluído. {len(uploaded_urls)} arquivos enviados com sucesso.")
        return uploaded_urls

    except Exception as e:
        logger.error(f"Erro ao enviar arquivos para o SharePoint: {e}")
        raise


def upload_single_file_to_sharepoint(logger, access_token, sharepoint_folder_url, file_path):
    """
    Faz o upload de um único arquivo para uma pasta no SharePoint.
    Substitui automaticamente arquivos com o mesmo nome.

    Args:
        logger: Objeto logger para registrar logs.
        access_token (str): Token de autenticação Microsoft Graph.
        sharepoint_folder_url (str): URL da pasta no SharePoint.
        file_path (str): Caminho completo do arquivo local a ser enviado.

    Returns:
        str: URL do arquivo enviado no SharePoint.
    """
    try:
        if not os.path.isfile(file_path):
            logger.error(f"SharePoint Upload Sigle File - O caminho fornecido não é um arquivo válido: {file_path}")
            return None

        logger.info(f"SharePoint Upload Single File - Enviando arquivo: {file_path}")

        # Codifica a URL da pasta SharePoint em shareId
        encoded_url = base64.b64encode(sharepoint_folder_url.encode('utf-8')).decode('utf-8')
        share_id = f'u!{encoded_url.replace("/", "_").replace("+", "-").rstrip("=")}'

        headers = {"Authorization": f"Bearer {access_token}"}

        # Resolve metadados da pasta
        folder_metadata_url = f"https://graph.microsoft.com/v1.0/shares/{share_id}/driveItem"
        metadata_response = requests.get(folder_metadata_url, headers=headers)
        metadata_response.raise_for_status()
        folder_item = metadata_response.json()

        drive_id = folder_item["parentReference"]["driveId"]
        folder_item_id = folder_item["id"]

        # Extrai o nome do arquivo
        file_name = os.path.basename(file_path)

        # Monta a URL de upload (sobrescreve se já existir)
        upload_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_item_id}:/{file_name}:/content"

        # Realiza o upload
        with open(file_path, "rb") as f:
            response = requests.put(upload_url, headers={**headers, "Content-Type": "application/octet-stream"}, data=f)
        response.raise_for_status()

        uploaded_item = response.json()
        web_url = uploaded_item.get("webUrl")
        logger.info(f"SharePoint Upload Single File - Arquivo '{file_name}' enviado com sucesso para: {web_url}")

        return web_url

    except Exception as e:
        logger.error(f"SharePoint Upload Single File - Erro ao enviar arquivo para o SharePoint: {e}")
        raise