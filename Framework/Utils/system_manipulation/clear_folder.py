import os
import shutil

def clear_create_temp_folder(paths, logger):
    """
    Recebe uma lista de caminhos e para cada caminho:
    - Se o diretório não existir, cria
    - Se existir, apaga todo conteúdo (arquivos e subpastas) dentro dele
    """

    if not isinstance(paths, list):
        logger.error("clear_folder - O argumento 'paths' deve ser uma lista de strings representando caminhos de pastas.")
        raise TypeError("O argumento 'paths' deve ser uma lista de strings representando caminhos de pastas.")

    for path in paths:
        try:
            if not os.path.exists(path):
                os.makedirs(path)  # cria diretório e todos os pais se precisar
                logger.info(f"clear_folder - Diretório '{path}' criado com sucesso!")
            else:
                # Apaga todo conteúdo da pasta, arquivos e subpastas
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.remove(item_path)  # remove arquivo ou link simbólico
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # remove diretório e conteúdo recursivamente
                logger.info(f"clear_folder - Conteúdo do diretório '{path}' removido com sucesso.")
        except PermissionError as e:
            logger.error(f"clear_folder - Permissão insuficiente para manipular o diretório '{path}': {e}")
        except Exception as e:
            logger.error(f"clear_folder - Erro ao limpar/criar o diretório '{path}': {e}")