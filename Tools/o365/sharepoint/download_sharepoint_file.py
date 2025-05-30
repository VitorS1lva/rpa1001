import os
import base64
import requests

def download_sharepoint_files(logger, access_token, sharepoint_folder_url, download_dir):
    """
    Faz o download de todos os arquivos de uma pasta do SharePoint usando apenas a URL da pasta.

    Args:
        logger: Objeto logger para registrar logs.
        access_token (str): Token de autenticação Microsoft Graph.
        sharepoint_folder_url (str): URL da pasta no SharePoint.
        download_dir (str): Caminho local onde os arquivos serão salvos.

    Returns:
        List[str]: Lista de caminhos locais dos arquivos baixados.
    """
    try:
        logger.info(f"SharePoint Folder Download - Baixando todos os arquivos da pasta: {sharepoint_folder_url}")

        # Codifica a URL para o formato de shareId
        encoded_url = base64.b64encode(sharepoint_folder_url.encode('utf-8')).decode('utf-8')
        share_id = f'u!{encoded_url.replace("/", "_").replace("+", "-").rstrip("=")}'

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Resolve a URL da pasta para um driveItem
        folder_metadata_url = f"https://graph.microsoft.com/v1.0/shares/{share_id}/driveItem"
        folder_response = requests.get(folder_metadata_url, headers=headers)
        folder_response.raise_for_status()
        folder_item = folder_response.json()

        drive_id = folder_item["parentReference"]["driveId"]
        item_id = folder_item["id"]

        # Lista os arquivos dentro da pasta
        children_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/children"
        children_response = requests.get(children_url, headers=headers)
        children_response.raise_for_status()
        children = children_response.json().get("value", [])

        # Garante o diretório local
        os.makedirs(download_dir, exist_ok=True)
        downloaded_files = []

        for item in children:
            if item.get("file"):  # Só baixa arquivos, ignora subpastas
                file_name = item["name"]
                download_url = item["@microsoft.graph.downloadUrl"]
                local_path = os.path.join(download_dir, file_name)

                file_response = requests.get(download_url)
                file_response.raise_for_status()

                with open(local_path, 'wb') as f:
                    f.write(file_response.content)

                logger.info(f"Arquivo '{file_name}' baixado para: {local_path}")
                downloaded_files.append(local_path)

        return downloaded_files

    except Exception as e:
        logger.error(f"Erro ao baixar arquivos da pasta do SharePoint: {e}")
        raise
