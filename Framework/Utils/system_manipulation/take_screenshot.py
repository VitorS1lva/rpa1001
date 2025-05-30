import pyautogui
from datetime import datetime
import os

def take_screenshot(logger):
    """
    Tira um screenshot da tela atual e salva na pasta 'Screenshots'.
    Retorna o caminho completo do arquivo salvo.

    Parâmetros:
        logger (Logger): Logger para registrar mensagens de log.

    Retorna:
        str | None: Caminho completo do screenshot salvo, ou None se houver erro.
    """
    try:
        # Define a pasta onde o screenshot será salvo
        screenshot_folder = os.path.join(os.getcwd(), 'Screenshots')
        
        # Cria a pasta se ela não existir
        os.makedirs(screenshot_folder, exist_ok=True)
        
        # Gera nome do arquivo com base na data e hora
        screenshot_file_name = f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
        
        # Caminho completo do arquivo
        complete_path = os.path.join(screenshot_folder, screenshot_file_name)
        
        # Tira o screenshot e salva
        screenshot = pyautogui.screenshot()
        screenshot.save(complete_path)
        
        logger.info(f"Take Screenshot - Screenshot salvo em: {complete_path}")
        return complete_path

    except Exception as e:
        logger.error(f"Take Screenshot - Erro ao tirar screenshot: {e}")
        return None