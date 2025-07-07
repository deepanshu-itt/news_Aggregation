import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
from typing import List


class EmailContentFormatter:

    @staticmethod
    def convert_urls_to_links(text):
        return re.sub(r'(https?://\S+)', r'<a href="\1">\1</a>', text)
    

    @staticmethod
    def build_email_content_from_articles(articles, body_lines):
    
        for index, article in enumerate(articles):
            body_lines += (
                f"- {index + 1}.) Article Id: {article.id}\n"
                f"  Title: {article.title}\n"
                f"  URL: {article.url}\n\n"
            )

        return "\n" + body_lines


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
        email_sent = False
        message = MIMEMultipart("alternative")
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = to_email

        plain_text = self.formatter.format_plain_text(body)
        html_text = self.formatter.format_html(body)

        message.attach(MIMEText(plain_text, 'plain'))
        message.attach(MIMEText(html_text, 'html'))

        try:
            self.run_smtp_server(message)
            email_sent = True

        except Exception as error:
            print(f"Failed to send email to {to_email}: {error}")
        
        return email_sent

    
    def run_smtp_server(self,message):
        sender_email = self.app_config['EMAIL_HOST_USER']
        sender_password = self.app_config['EMAIL_HOST_PASSWORD']
        smtp_server = self.app_config['EMAIL_HOST']
        smtp_port = self.app_config['EMAIL_PORT']
        use_tls = self.app_config['EMAIL_USE_TLS']
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            if use_tls:
                server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        print(f"Email sent successfully to {message['To']} with subject: {message['Subject']}")
