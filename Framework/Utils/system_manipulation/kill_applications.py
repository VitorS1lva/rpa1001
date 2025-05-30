import psutil
import logging

def kill_applications(app_names: list, logger: logging.Logger):
    """
    Encerra aplicações com base na lista de nomes fornecidos.

    Parâmetros:
        app_names (list): Lista com os nomes das aplicações a serem encerradas (ex: ['excel.exe']).
        logger (Logger): Logger para registrar as ações e erros.
    """
    
    logger.info("Close Applications - Iniciando encerramento das aplicações...")

    for app in app_names:
        logger.info(f"Close Applications - Buscando processos para: {app}")
        try:
            found = False
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() == app.lower():
                    logger.info(f"Close Applications - Encerrando {app} (PID {proc.pid})")
                    proc.terminate()
                    found = True
            if not found:
                logger.warning(f"Close Applications - Nenhuma instância de '{app}' encontrada.")
        except Exception as e:
            logger.error(f"Close Applications - Erro ao tentar encerrar '{app}': {e}")

    logger.info("Close Applications - Finalizado.")
