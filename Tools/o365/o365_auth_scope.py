import requests

def authenticate_office365(logger, tenant_id, client_id, client_secret, scope="https://graph.microsoft.com/.default"):
    """
    Autentica na API do Office 365 (Microsoft Graph) usando o fluxo client_credentials.

    Args:
        logger: objeto logger para registrar logs.
        tenant_id (str): ID do tenant (locatário do Azure).
        client_id (str): ID da aplicação registrada no Azure.
        client_secret (str): Segredo da aplicação.
        scope (str): Escopo de permissão. Por padrão, usa Microsoft Graph.

    Returns:
        str: Token de acesso (Bearer token) para ser usado em chamadas subsequentes.
    """
    logger.info("O365 Authentication Scope - Autenticando na API do Office 365...")

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status()

        o365Conection = response.json().get("access_token")
        if not o365Conection:
            raise ValueError("Token de acesso não encontrado na resposta.")

        logger.info("O365 Authentication Scope - Autenticação bem-sucedida.")
        return o365Conection

    except requests.exceptions.RequestException as e:
        logger.error(f"O365 Authentication Scope - Erro na requisição de autenticação: {e}")
        raise
    except Exception as ex:
        logger.error(f"O365 Authentication Scope - Erro inesperado ao autenticar no Office 365: {ex}")
        raise
