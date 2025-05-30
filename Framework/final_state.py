from .Utils.system_manipulation import take_screenshot
from Tools.o365.o365_auth_scope import authenticate_office365
from Tools.o365.outlook.send_mail import send_email
from Tools.o365.sharepoint.upload_file_to_sharepoint import upload_single_file_to_sharepoint
import pandas as pd
import os

def final_state(logger, input_table, error_table, success_table, env_vars, apps, assets):
    """
    Finaliza a execução do processo automatizado.

    Parâmetros:
        logger (Logger): Logger para registrar eventos e erros.
        error_table (list): Lista de erros ocorridos durante o processo.
        success_table (list): Lista de registros bem-sucedidos.
        apps (list): Lista de instâncias de aplicações abertas para serem finalizadas.
    """

    # Consolidação das tabelas em Excel
    try:
        logger.info("Final State - Consolidando tabelas de erro e sucesso em Excel...")

        # Define o nome do arquivo e o diretório de destino
        temp_folder = env_vars.get("output_folder")
        filename = "input.xlsx"
        file_path = os.path.abspath(os.path.join(temp_folder, filename))

        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            input_table.to_excel(writer, sheet_name="input", index=False)
            success_table.to_excel(writer, sheet_name="Sucessos", index=False)
            error_table.to_excel(writer, sheet_name="Erros", index=False)

    except Exception as e:
        logger.error(f"Final State - Erro ao consolidar tabelas em Excel: {e}")
        screenshot_path = take_screenshot(logger)
        logger.debug(f"Process - Screenshot salvo em: {screenshot_path}")
        raise


    # Envio de e-mail com os resultados da execução
    try:
        logger.info("Final State - Enviando e-mail com resultados da execução...")
        o365Conection = authenticate_office365(logger=logger, tenant_id=assets["tenant_id"], client_id=env_vars["client_id"], client_secret=assets["client_secret"])
        send_email(logger=logger, access_token=o365Conection, sender=env_vars.get("mail_sender"), to_recipients=env_vars.get("mail_to",[]), subject="RPA1003 - Relatório de Execução", body="", attachment_paths=[file_path])
        # Lógica para envio ao sharepoint
        upload_single_file_to_sharepoint(logger=logger, access_token=o365Conection, sharepoint_folder_url=env_vars.get("sharepoint_url"), file_path=file_path)
    except Exception as e:
        logger.error(f"Final State - Erro ao enviar e-mail: {e}")
        screenshot_path = take_screenshot(logger)
        logger.debug(f"Process- Screenshot salvo em: {screenshot_path}")
        raise

    # Fechamento das aplicações abertas
    try:
        logger.info("Final State - Fechando aplicações abertas...")
        for app in apps:
            try:
                app.close()
                logger.info(f"Final State - Aplicação {app} fechada com sucesso.")
            except Exception as e:
                logger.warning(f"Final State - Erro ao tentar fechar a aplicação {app}: {e}")
    except Exception as e:
        logger.error(f"Final State - Erro no loop de fechamento de aplicações: {e}")
        take_screenshot(logger)
        raise

    logger.info("Final State - Processo finalizado com sucesso.")