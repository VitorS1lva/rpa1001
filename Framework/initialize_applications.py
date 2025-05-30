from .Utils.system_manipulation.kill_applications import kill_applications
from .Utils.system_manipulation.take_screenshot import take_screenshot
from .Utils.exceptions.exceptions import  SystemException
from Tools.sap.sap_login import login_sap

# Imports para login no SAP
import win32com.client 
import subprocess
import time

def initialize_applications(logger, env_vars, assets):
    """
    Inicializa as aplicações necessárias para o processo.

    Args:
        logger: objeto logger para registrar logs de execução.

    Returns:
        list: Lista de aplicações inicializadas (pode ser vazia se nada for inicializado).
    """

    # Inicializa a lista de aplicações que será retornada ao fim do initialize_applications
    applications = []

    # Chamando função de limpeza de aplicações
    kill_applications(env_vars.get("apps_to_kill", []), logger)

    # Lógica de inicialização de aplicações
    try:
       # Lógica de login no SAP
        session = login_sap(env_vars.get("sap_path"), env_vars.get("sap_connection_name"), env_vars.get("sap_code"), assets["sap_login"], assets["sap_password"], env_vars.get("sap_transaction_code"), logger)

        # Adiciona o app incializado a lista de aplicações
        applications.append(session)
        logger.info(f"Initialize Applications - Aplicações inicializadas com sucesso: {len(applications)} apps.")

    except Exception as e:
        logger.error(f"Initialize Applications - Erro ao inicializar aplicações: {e}")
        logger.error(f"Initialize Applications - Erro ao inicializar aplicações: {e.with_traceback}")
        screenshot_path = take_screenshot(logger)
        logger.debug(f"Screenshot salvo em: {screenshot_path}")
        raise

    return applications