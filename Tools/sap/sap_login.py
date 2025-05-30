import subprocess
import time
import win32com.client

def login_sap(
    sap_exe_path: str,
    sap_connection_name: str,
    sap_session_code: str,
    sap_login: str,
    sap_password: str,
    sap_transaction_code: str,
    logger
):
    """
    Realiza o login automático no SAP GUI via SAP Scripting e acessa uma transação específica.

    Esta função executa os seguintes passos:
    1. Inicia o processo do SAP GUI (saplogon.exe).
    2. Obtém o objeto SAP GUI Automation.
    3. Abre a conexão com o ambiente especificado (ex: QAS, PRD).
    4. Realiza o login com usuário e senha fornecidos.
    5. Acessa a transação SAP especificada (ex: YSD008).

    Parâmetros:
    - sap_exe_path (str): Caminho completo do executável SAP GUI (saplogon.exe).
    - sap_connection_name (str): Nome da conexão SAP configurada no SAP Logon.
    - sap_session_code (str): Código do mandante (ex: "400").
    - sap_login (str): Usuário SAP.
    - sap_password (str): Senha do usuário SAP.
    - sap_transaction_code (str): Código da transação a ser acessada após o login.
    - env_vars (dict): Dicionário com variáveis de ambiente (não utilizado diretamente, reservado para uso futuro).
    - logger (Logger): Instância de logger para registrar informações e erros durante o processo.

    Retorno:
    - session (win32com.client.CDispatch): Sessão SAP ativa, já logada e com a transação acessada.
    - None: Em caso de erro durante qualquer etapa do processo.
    """

    try:
        logger.info("SAP Login - Inicializando processo do SAP.")
        subprocess.Popen(sap_exe_path)
        time.sleep(5)

        # Inicializa o objeto SAP GUI
        SapGuiAuto = win32com.client.GetObject("SAPGUI")

        if not isinstance(SapGuiAuto, win32com.client.CDispatch):
            logger.error("SAP Login - Falha ao obter SAPGUI object.")
            return None

        # Obtém o engine de scripting do SAP
        application = SapGuiAuto.GetScriptingEngine
        connection = application.OpenConnection(sap_connection_name, True)
        time.sleep(3)

        # Inicia a sessão SAP
        session = connection.Children(0)
        session.findById("wnd[0]").maximize()

        # Realiza o login
        logger.info("SAP Login - Realizando login.")
        session.findById("wnd[0]/usr/txtRSYST-MANDT").text = sap_session_code
        session.findById("wnd[0]/usr/txtRSYST-BNAME").text = sap_login
        session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = sap_password
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(2)

        # Acessa a transação desejada
        logger.info(f"SAP Login - Chamando transação {sap_transaction_code}")
        session.findById("wnd[0]/tbar[0]/okcd").text = sap_transaction_code
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(2)

        logger.info("SAP Login - Login e transação executados com sucesso.")

        return session

    except Exception as e:
        logger.exception(f"SAP Login - Erro ao realizar login no SAP: {str(e)}")
        return None
