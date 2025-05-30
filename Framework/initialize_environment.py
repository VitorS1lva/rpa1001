import os
import json
from .Utils.system_manipulation.clear_folder import clear_create_temp_folder
from .Utils.system_manipulation.take_screenshot import take_screenshot
from Tools.o365.o365_auth_scope import authenticate_office365
from Tools.o365.sharepoint.download_sharepoint_file import download_sharepoint_files
from Tools.excel.read_excel_file import read_excel
import pandas as pd

def initialize_environment(logger, assets):
    """
    Inicializa o ambiente de automação:

    - Lê configurações do arquivo config.json
    - Define variáveis globais com base nessas configurações
    - Limpa pastas de arquivos temporários definidas no config.json

    Args:
        logger (logging.Logger): Objeto de logger utilizado para registrar logs durante a inicialização do ambiente.
    """

    # Leitura do arquivo config.json
    try:
        config_path = os.path.join(os.path.dirname(__file__), os.pardir, 'Data', 'config.json')
        config_path = os.path.abspath(config_path)  # Garante o caminho absoluto, se necessário
        logger.info("Initialize Environment - Lendo arquivo config.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    except Exception as e:
        logger.error(f"Erro ao abrir config.json: {e}")
        screenshot_path = take_screenshot(logger)
        logger.debug(f"Screenshot salvo em: {screenshot_path}")
        raise

    # Inicializa o dicionário de ambiente com os dados do config
    environment_vars = {}

    try:
        logger.info("Initialize Environment - Carregando variáveis do config para dicionário local")
        for key, value in config_data.items():
            environment_vars[key] = value
    except Exception as e:
        logger.error(f"Initialize Environment - Erro ao carregar variáveis do config.json: {e}")
        screenshot_path = take_screenshot(logger)
        logger.debug(f"Screenshot salvo em: {screenshot_path}")
        raise

    # Limpeza de pastas temporárias
    try:
        if not environment_vars.get('temp_folders', []):
            logger.warning("Initialize Environment - Nenhuma pasta temporária definida em 'temp_folders' no config.json")
        clear_create_temp_folder(paths=environment_vars.get('temp_folders', []), logger=logger)
        logger.info("Initialize Environment - Pastas temporárias limpas/criadas com sucesso")
    except Exception as e:
        logger.error(f"Initialize Environment - Erro ao limpar/criar pastas temporárias: {e}")
        screenshot_path = take_screenshot(logger)
        logger.debug(f"Screenshot salvo em: {screenshot_path}")
        raise

    # --- Lógica de criação de queue items ---
    # O item tem que ser um data frame criado pela biblioteca do Pandas
    queue_items = pd.DataFrame([{'name': 'teste'}])
    # --- Fim da lógica de criação de queue items ---

    logger.info("Initialize Environment - Ambiente inicializado com sucesso")

    return environment_vars, queue_items