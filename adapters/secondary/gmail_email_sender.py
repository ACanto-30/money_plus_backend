import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional
from decouple import config
from domain.ports.secondary.email_sender import IEmailSender
from domain.commands.email_command import EmailCommand

class GmailEmailSender(IEmailSender):
    """Implementación del EmailSender usando Gmail SMTP"""
    
    def __init__(self):
        # Configuración de Gmail
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = str(config('GMAIL_SENDER_EMAIL', default=''))
        self.app_password = str(config('GMAIL_APP_PASSWORD', default=''))
        self.sender_name = str(config('GMAIL_SENDER_NAME', default='GoScanAPI'))
        
        # Validar configuración
        if not self.sender_email or not self.app_password:
            raise ValueError("GMAIL_SENDER_EMAIL y GMAIL_APP_PASSWORD deben estar configurados en el archivo .env")
    
    def send_email(self, email_command: EmailCommand) ->  bool:
        """Envía un email usando Gmail SMTP"""
        try:
            # Extraer datos del payload
            to = email_command.to
            subject = email_command.subject
            body = email_command.body
            cc = email_command.cc
            bcc = email_command.bcc
            html_body = email_command.html_body
            
            # Validar datos requeridos
            if not to or not subject or not body:
                return False
            
            # Crear el mensaje
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = to
            msg['Subject'] = subject
            
            # Agregar destinatarios CC si existen
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            # Agregar destinatarios BCC si existen
            if bcc:
                msg['Bcc'] = ', '.join(bcc)
            
            # Agregar el cuerpo del mensaje
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # Agregar versión HTML si existe
            if html_body:
                html_part = MIMEText(html_body, 'html', 'utf-8')
                msg.attach(html_part)
            
            # Preparar lista de destinatarios
            recipients = [to]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            # Enviar el email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(self.sender_email, self.app_password)
                server.send_message(msg, from_addr=self.sender_email, to_addrs=recipients)
            
            return True
            
        except smtplib.SMTPAuthenticationError:
            return False
        except smtplib.SMTPRecipientsRefused as e:
            return False
        except smtplib.SMTPServerDisconnected:
            return False
        except Exception as e:
            return False
    
    def send_bulk_email(self, emails_data: List[EmailCommand]) -> bool:
        """Envía múltiples emails usando Gmail SMTP"""
        
        try:
            # Establecer conexión una sola vez para todos los emails
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(self.sender_email, self.app_password)
                
                for email_command in emails_data:
                    try:
                        # Extraer datos del email
                        to = email_command.to
                        subject = email_command.subject
                        body = email_command.body
                        cc = email_command.cc
                        bcc = email_command.bcc
                        html_body = email_command.html_body
                        
                        # Validar datos requeridos
                        if not to or not subject or not body:
                            return False
                        
                        # Crear el mensaje
                        msg = MIMEMultipart('alternative')
                        msg['From'] = f"{self.sender_name} <{self.sender_email}>"
                        msg['To'] = to
                        msg['Subject'] = subject
                        
                        # Agregar destinatarios CC si existen
                        if cc:
                            msg['Cc'] = ', '.join(cc)
                        
                        # Agregar destinatarios BCC si existen
                        if bcc:
                            msg['Bcc'] = ', '.join(bcc)
                        
                        # Agregar el cuerpo del mensaje
                        text_part = MIMEText(body, 'plain', 'utf-8')
                        msg.attach(text_part)
                        
                        # Agregar versión HTML si existe
                        if html_body:
                            html_part = MIMEText(html_body, 'html', 'utf-8')
                            msg.attach(html_part)
                        
                        # Preparar lista de destinatarios
                        recipients = [to]
                        if cc:
                            recipients.extend(cc)
                        if bcc:
                            recipients.extend(bcc)
                        
                        # Enviar el email
                        server.send_message(msg, from_addr=self.sender_email, to_addrs=recipients)
                        
                        return True
                        
                    except Exception as e:
                        return False
                        
        except Exception as e:
            # Si hay error de conexión, marcar todos como fallidos
            for email_command in emails_data:
                return False
        
        return True
    
    def test_connection(self) -> bool:
        """Prueba la conexión con el servidor de Gmail"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(self.sender_email, self.app_password)
                return True
        except Exception:
            return False
    
    def send_password_reset_email(self, to_email: str, code: int) -> bool:
        """Envía un email de reseteo de contraseña"""
        try:
            subject = "Código de Reseteo de Contraseña - GoScanAPI"
            body = f"""
            Hola,
            
            Has solicitado un reseteo de contraseña para tu cuenta en GoScanAPI.
            
            Tu código de reseteo es: {code}
            
            Este código expira en 10 minutos.
            
            Si no solicitaste este reseteo, puedes ignorar este email.
            
            Saludos,
            Equipo de GoScanAPI
            """
            
            html_body = f"""
            <html>
            <body>
                <h2>Código de Reseteo de Contraseña</h2>
                <p>Hola,</p>
                <p>Has solicitado un reseteo de contraseña para tu cuenta en GoScanAPI.</p>
                <p><strong>Tu código de reseteo es: {code}</strong></p>
                <p>Este código expira en 10 minutos.</p>
                <p>Si no solicitaste este reseteo, puedes ignorar este email.</p>
                <br>
                <p>Saludos,<br>Equipo de GoScanAPI</p>
            </body>
            </html>
            """
            
            # Crear el comando de email
            email_command = EmailCommand(
                to=to_email,
                subject=subject,
                body=body,
                html_body=html_body,
                cc=[],
                bcc=[]
            )
            
            # Enviar el email usando el método existente
            return self.send_email(email_command)
            
        except Exception:
            return False 