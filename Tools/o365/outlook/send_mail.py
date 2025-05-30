import os
import requests
from base64 import b64encode

def send_email(logger, access_token, sender, to_recipients, subject, body, attachment_paths=None):
    """
    Envia um e-mail via Microsoft Graph API (Outlook), com suporte a anexos.

    Args:
        access_token (str): Token de acesso OAuth2.
        sender (str): E-mail do remetente.
        to_recipients (list): Lista de e-mails dos destinatários.
        subject (str): Assunto do e-mail.
        body (str): Corpo do e-mail em HTML.
        logger (Logger): Logger configurado no escopo externo.
        attachment_paths (list, opcional): Lista de caminhos de arquivos a serem anexados.
    """
    logger.info("EmailSender - Iniciando preparo do e-mail...")

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    recipients = [{"emailAddress": {"address": addr}} for addr in to_recipients]

    email = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": body
            },
            "toRecipients": recipients,
        },
        "saveToSentItems": "true"
    }

    if attachment_paths:
        attachments = []
        for path in attachment_paths:
            try:
                filename = os.path.basename(path)
                with open(path, "rb") as f:
                    content_bytes = b64encode(f.read()).decode('utf-8')
                attachments.append({
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": filename,
                    "contentBytes": content_bytes
                })
                logger.info(f"EmailSender - Anexo adicionado: {filename}")
            except Exception as e:
                logger.error(f"EmailSender - Erro ao processar anexo {path}: {e}")
        email["message"]["attachments"] = attachments

    try:
        response = requests.post(
            f"https://graph.microsoft.com/v1.0/users/{sender}/sendMail",
            headers=headers,
            json=email
        )
        if response.status_code == 202:
            logger.info("EmailSender - E-mail enviado com sucesso.")
        else:
            logger.error(f"EmailSender - Falha ao enviar e-mail: {response.status_code} - {response.text}")
    except Exception as e:
        logger.exception(f"EmailSender - Exceção ao tentar enviar e-mail: {e}")