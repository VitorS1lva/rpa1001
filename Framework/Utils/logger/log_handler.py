import logging
import os
from datetime import datetime

def setup_logger(name, level=logging.INFO, log_dir: str = "logs") -> logging.Logger:
    """
    Configura e retorna um logger com saída em console e arquivo.

    Parâmetros:
        name (str): Nome identificador do logger.
        level (int): Nível de log desejado (ex: logging.INFO, logging.DEBUG).
        log_dir (str): Diretório onde os arquivos de log serão salvos. Default: 'logs'.

    Retorna:
        logging.Logger: Objeto logger configurado.

    Exemplos:
        logger = setup_logger("Execucao")
        logger.info("Iniciando execução do processo.")
        logger.warning("Aviso de possível inconsistência.")
        logger.error("Erro simulado para fins de teste.")
    """

    # Garante que o diretório de logs exista
    os.makedirs(log_dir, exist_ok=True)

    # Gera timestamp para nome do arquivo de log (formato: dia-mês-ano_hora-minuto-segundo)
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    # Cria o caminho completo do arquivo de log
    log_file = os.path.join(log_dir, f"{name}_{timestamp}.log")

    # Obtém o logger pelo nome
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evita adicionar múltiplos handlers ao mesmo logger em execuções repetidas
    if not logger.handlers:

        # Define o formato padrão das mensagens de log
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Handler para exibir logs no console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler para registrar logs em arquivo
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger