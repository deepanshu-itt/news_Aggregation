import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re


class EmailContentFormatter:

    @staticmethod
    def convert_urls_to_links(text):
        return re.sub(r'(https?://\S+)', r'<a href="\1">\1</a>', text)

    def format_plain_text(self, body):
        return body

    def format_html(self, body, message=""):
        html_body_content = self.convert_urls_to_links(body).replace('\n', '<br>')
        return f"""\
        <html>
            <body>
                <p>Hi Geek,</p>
                <p>{message}</p>
                <p>{html_body_content}</p>
            </body>
        </html>
        """


class EmailSender:

    def __init__(self, app_config, formatter=None):
        self.app_config = app_config
        self.formatter = formatter or EmailContentFormatter()

    def send_email(self, to_email, subject, body):
        sender_email = self.app_config['EMAIL_HOST_USER']
        sender_password = self.app_config['EMAIL_HOST_PASSWORD']
        smtp_server = self.app_config['EMAIL_HOST']
        smtp_port = self.app_config['EMAIL_PORT']
        use_tls = self.app_config['EMAIL_USE_TLS']

        msg = MIMEMultipart("alternative")
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email

        plain_text = self.formatter.format_plain_text(body)
        html_text = self.formatter.format_html(body)

        msg.attach(MIMEText(plain_text, 'plain'))
        msg.attach(MIMEText(html_text, 'html'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if use_tls:
                    server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            print(f"Email sent successfully to {to_email} with subject: {subject}")
            return True
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")
            return False
