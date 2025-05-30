from .Utils.system_manipulation.take_screenshot import take_screenshot
from .Utils.exceptions.exceptions import *
import pandas as pd
import traceback

# Imports para manipulação no SAP
from datetime import date, timedelta
import win32com.client 
import subprocess
import time
import datetime


def process(apps, env_vars, queue_items, logger, assets):
    """
    Executa o processo principal da automação, percorrendo itens da fila.

    Parâmetros:
        apps (dict): Dicionário com as aplicações utilizadas, instanciadas previamente.
        logger (Logger): Logger para registro dos logs da execução.
        queue_items (pandas.DataFrame): DataFrame representando os itens da fila.
    """

    logger.info("Process - Iniciando execução do processo com múltiplos queue items...")

    # Define as colunas para os DataFrames de sucesso e erro
    success_columns = ["process_idx", "status"]
    error_columns = ["status", "details", "data", "screenshot_path"]

    # Inicializa os DataFrames vazios
    ls_success = pd.DataFrame(columns=success_columns)
    ls_errors = pd.DataFrame(columns=error_columns)

    # Itera linha a linha do DataFrame
    for idx, (_, row) in enumerate(queue_items.iterrows(), start=1):
        queue_item = row.tolist()

        logger.info(f"Process - Processando item {queue_items["name"]}")  # Melhorar qualidade do log

        try:
            # Lógica do proces

            # Inicializando variáveis locais
            logger.info("Process - Inicializando variáveis locais")
            ## Tabela de consolidação de dados
            dt_input = pd.DataFrame(columns=[
                "nota_fiscal",
                "data_fiscal",
                "cod_cfop",
                "valor_nota_fiscal",
                "status",
                "consultado",
                "xml"
             ])
            
            # Inserindo parâmetros da query na transação
            logger.info("Process - Inserindo parâmetros da query na transação")
            apps[0].findById("wnd[0]/usr/ctxtSO_BUKRS-LOW").text = env_vars.get("matriz_code")
            apps[0].findById("wnd[0]/usr/btn%_SO_BRANC_%_APP_%-VALU_PUSH").press()
            apps[0].findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,0]").text = env_vars.get("filial_code")
            apps[0].findById("wnd[0]").sendVKey(8)
            apps[0].findById("wnd[0]/usr/ctxtSO_PSTDT-LOW").text = (date.today().replace(day=1) - timedelta(days=1)).replace(day=1).strftime("%d.%m.%Y")
            apps[0].findById("wnd[0]/usr/ctxtSO_PSTDT-HIGH").text = "09.04.2025" #(date.today().replace(day=1) - timedelta(days=1)).strftime("%d.%m.%Y")
            apps[0].findById("wnd[0]/usr/ctxtSO_NFTYP-LOW").text = env_vars.get("nf_code")
            apps[0].findById("wnd[0]/usr/btn%_SO_CFOP_%_APP_%-VALU_PUSH").press()
            apps[0].findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,0]").text = env_vars.get("cfop_first_code")
            apps[0].findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").text = env_vars.get("cfop_second_code")
            apps[0].findById("wnd[0]").sendVKey(8)
            apps[0].findById("wnd[0]/usr/ctxtP_VARI").text = env_vars.get("template_code")
            apps[0].findById("wnd[0]").sendVKey(8)

            # Interação com a tabela de dados
            logger.info("Process - Interação com a tabela de dados")
            ## Captura do numero total de linhas
            tabela_bruta = apps[0].findById("wnd[0]/usr/cntlGRID1/shellcont/shell")
            numero_linhas = tabela_bruta.RowCount
            numero_colunas = tabela_bruta.ColumnCount

            # Entrando no modo de visão
            logger.info("Process - Entrando no modo de visão")
            apps[0].findById("wnd[0]/mbar/menu[0]/menu[0]").select()

            # Iniciando loop de coleta de informações da tabela
            logger.info("Process - Iniciando loop de coleta de informações da tabela")
            ## Iniciando variáveis
            row_idx = 8
            column_idx = 2
            old_value = ""
            ls_deduplicado = []

            while row_idx <= (numero_linhas + 5): # O nº 5 existe para compensar o cabeçalho
                valor = apps[0].findById(f"wnd[0]/usr/lbl[{column_idx},{row_idx}]").text
                valor = valor.strip()

                if old_value != valor:
                    ls_deduplicado.append(valor)

                old_value = valor
                row_idx = row_idx + 1 
            
            apps[0].findById("wnd[0]").sendVKey(3)

            # Loop para captura de informações
            logger.info("Process - Entrando no loop para captura de informações")

            # Counter para quantidade de notas
            counter_nf = 1

            for nota_fiscal in ls_deduplicado:
                # Fazendo a busca na tabela
                logger.info(f"Process - Buscando NF de Nº {counter_nf} - {nota_fiscal}")

                apps[0].findById("/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[71]").press()
                apps[0].findById("wnd[1]/usr/txtGS_SEARCH-VALUE").text = nota_fiscal
                apps[0].findById("wnd[0]").sendVKey(0)
                apps[0].findById("wnd[0]").sendVKey(12)
                apps[0].findById("wnd[0]").sendVKey(2)
                time.sleep(3)

                # Capturando informações dentro da nota
                logger.info(f"Process - Capturando informações dentro da nota")
                apps[0].findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB2").select()
                time.sleep(3)
                valor_nota = apps[0].findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB2/ssubHEADER_TAB:SAPLJ1BB2:2200/txtJ_1BDYDOC-NFTOT").text
                apps[0].findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB8").select()
                time.sleep(3)
                chave_acesso = apps[0].findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB8/ssubHEADER_TAB:SAPLJ1BB2:2800/txtJ_1B_NFE_SCREEN_FIELDS-ACCKEY").text
                data_documento = apps[0].findById("wnd[0]/usr/ctxtJ_1BDYDOC-DOCDAT").text

                # Alimentando tabela de report
                logger.info(f"Process - Alimentando tabela de repor")
                novo_registro = pd.DataFrame([{
                    "nota_fiscal": nota_fiscal,
                    "data_fiscal": data_documento,
                    "cod_cfop": "6110/AA",
                    "valor_nota_fiscal": valor_nota,
                    "status": "",
                    "consultado": "",
                    "xml": chave_acesso
                }])

                dt_input = pd.concat([dt_input, novo_registro], ignore_index=True)

                # Retornando para a tela da tabela
                logger.info(f"Process - Retornando para a tela da tabela")
                apps[0].findById("wnd[0]").sendVKey(3)
                time.sleep(2)
                apps[0].findById("wnd[0]").sendVKey(3)

                # Acrescendo counter_nf
                counter_nf = counter_nf + 1 

                pass

            # Registra sucesso do processo em DataFrame
            success_row = pd.DataFrame([{
                "process_idx": str(queue_items["name"]),
                "status": "Success"
            }])
            ls_success = pd.concat([ls_success, success_row], ignore_index=True)

            logger.info(f"Process - Item {queue_items["name"]} processado com sucesso.")

        except Exception as e:
            logger.error(f"Process - Erro ao processar item {queue_items["name"]}: {e}")
            logger.debug(traceback.format_exc())
            screenshot_path = take_screenshot(logger)
            logger.debug(f"Process- Screenshot salvo em: {screenshot_path}")
            error_type = type(e).__name__

            # Dicionario de possiveis erros
            status_text = {
                "BusinessRuleException": "Business Rule Exception",
                "SystemException": "System Exception"
            }.get(error_type, "Erro não previsto")

            # Adiciona o erro a tabela de coleta de erros
            error_row = pd.DataFrame([{
                "status": status_text,
                "details": str(e),
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "screenshot_path": screenshot_path,
            }])
            ls_errors = pd.concat([ls_errors, error_row], ignore_index=True)

            if error_type == "BusinessRuleException":
                logger.warning(f"Process - Erro de regra de negócio no item {queue_items["name"]}5.")
            elif error_type == "SystemException":
                logger.critical(f"Process - Erro de sistema no item {queue_items["name"]}.")
            else:
                logger.warning(f"Process - Erro não previsto no item {queue_items["name"]}.")

        continue

    logger.info("Process - Fim da execução dos queue items.")

    return ls_errors, ls_success, dt_input
