import pandas as pd

def read_excel(file_path, sheet_name=0, logger=None):
    """
    Lê um arquivo Excel (.xls, .xlsx) e retorna um DataFrame com os dados da planilha.

    Args:
        file_path (str): Caminho completo do arquivo Excel.
        sheet_name (str|int, opcional): NOME ou índice da planilha a ser lida. Padrão é a primeira planilha.
        logger (logging.Logger, opcional): Objeto logger para registrar logs.

    Returns:
        df (pandas.DataFrame): Dados da planilha em formato de tabela.
    """
    try:
        if logger:
            logger.info(f"Read Excel File - Lendo arquivo Excel: {file_path}, planilha: {sheet_name}")
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        if logger:
            logger.info(f"Read Excel File - Arquivo Excel lido com sucesso: {file_path}")
            logger.info(f"Read Excel File - Prewview dos dados: {df.head()}")
        return df
    except Exception as e:
        if logger:
            logger.error(f"Read Excel File - Erro ao ler o arquivo Excel {file_path}: {e}")
        else:
            print(f"Erro ao ler o arquivo Excel: {e}")
        raise
