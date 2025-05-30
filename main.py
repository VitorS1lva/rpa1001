from Framework.Utils.logger import log_handler
from Framework.initialize_environment import initialize_environment
from Framework.initialize_applications import initialize_applications
from Framework.process import process
from Framework.final_state import final_state

class Main:
    def __init__(self, assets):
        """
        Inicializa a classe Main:
        - Configura o logger para registrar eventos
        - Prepara as variáveis para os módulos do framework
        - Carrega as credenciais fornecidas
        Parâmetros:
            credentials (dict): Dicionário contendo as credenciais necessárias para o processo.
        """
        # Configura o logger para registrar eventos
        self.logger = log_handler.setup_logger("#")
        self.logger.info("Main - Iniciando Main.py")

        # Verifica se as credenciais foram fornecidas, caso contrário, usa um dicionário vazio
        if assets is None:
            assets = {}
            self.logger.warning("Main - Nenhuma credencial fornecida, usando dicionário vazio.")
        else:
            self.logger.info("Main - Carregando credenciais")
            self.assets = assets
        print(assets)
        # Inicializa o ambiente e aplicações como None (serão configurados no main)
        self.environment_data = None
        self.applications = None

    def main(self):
        """
        Método principal para executar o fluxo do programa:
        - Inicializa o ambiente
        - Inicializa as aplicações
        - Executa o processo principal
        - Finaliza o estado/processo
        """
        self.logger.info("Main - Iniciando ambiente")
        # Inicializa o ambiente e captura os dados retornados
        self.env_vars, self.queue_items = initialize_environment(logger=self.logger, assets=self.assets)

        self.logger.info("Main - Inicializando aplicações")
        # Inicializa as aplicações e armazena a lista retornada
        self.applications = initialize_applications(logger=self.logger, env_vars=self.env_vars, assets=self.assets)

        self.logger.info("Main - Executando process")
        # Executa o processo principal passando as aplicações inicializadas
        self.ls_errors, self.ls_success, self.input_table = process(apps=self.applications, env_vars=self.env_vars, queue_items=self.queue_items, logger=self.logger, assets=self.assets)

        self.logger.info("Main - Finalizando processo")
        # Finaliza o estado/processo conforme implementação do framework
        final_state(logger=self.logger, input_table=self.input_table, error_table=self.ls_errors, success_table=self.ls_success, env_vars=self.env_vars, apps=self.applications, assets=self.assets)

if __name__ == "__main__":
    # Ponto de entrada do script
    main_instance = Main(assets="")
    main_instance.main()
