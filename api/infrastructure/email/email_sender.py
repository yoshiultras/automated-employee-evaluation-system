import smtplib
from email.mime.text import MIMEText
from smtplib import SMTPRecipientsRefused

from api.config.settings import Settings
from api.core.dto import AccountLoginMessage
from api.core.protocols import EmailSender


class EmailSenderImpl(EmailSender):
    def __init__(self, settings: Settings):
        email_sender_settings = settings.email_sender_settings
        self.email_password = email_sender_settings.email_password
        self.email_from = email_sender_settings.email_from
        self.server = email_sender_settings.server
        self.server_port = email_sender_settings.server_port
        self.jinja_templates = settings.jinja_templates_email

    async def account_login_message(self, data: AccountLoginMessage):
        template = self.jinja_templates.get_template(
            "account_login_message.html"
        )
        rendered_message = template.render(datetime=data.datetime)
        email_message = MIMEText(rendered_message)
        email_message["Subject"] = "Кто-то вошел в ваш аккаунт."

        email_message["From"] = self.email_from
        email_message["To"] = data.email_recipient

        try:
            server = smtplib.SMTP_SSL(self.server, self.server_port)
            server.ehlo()
            server.login(self.email_from, self.email_password)
            server.send_message(email_message)
            server.quit()
        except SMTPRecipientsRefused:
            pass
        except Exception:
            pass
