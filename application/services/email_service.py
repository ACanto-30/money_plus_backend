from typing import List, Dict, Any
from domain.ports.secondary.email_sender import IEmailSender
from application.dto.email_dto import EmailMessageDTO, EmailResultDTO, BulkEmailRequestDTO, BulkEmailResponseDTO
from infrastructure.configuration.container import Container

class EmailService:
    """Servicio de aplicación para el envío de emails"""
    
    def __init__(self):
        self._email_sender = Container.resolve(IEmailSender)
    
    def send_welcome_email(self, to_email: str, username: str) -> EmailResultDTO:
        """Envía un email de bienvenida"""
        subject = "¡Bienvenido a GoScanAPI!"
        body = f"""
        Hola {username},
        
        ¡Bienvenido a GoScanAPI! Tu cuenta ha sido creada exitosamente.
        
        Gracias por registrarte en nuestra plataforma.
        
        Saludos,
        El equipo de GoScanAPI
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>¡Bienvenido a GoScanAPI!</h2>
            <p>Hola <strong>{username}</strong>,</p>
            <p>¡Bienvenido a GoScanAPI! Tu cuenta ha sido creada exitosamente.</p>
            <p>Gracias por registrarte en nuestra plataforma.</p>
            <br>
            <p>Saludos,<br>El equipo de GoScanAPI</p>
        </body>
        </html>
        """
        
        payload = {
            'to': to_email,
            'subject': subject,
            'body': body,
            'html_body': html_body
        }
        
        result = self._email_sender.send_email(payload)
        
        return EmailResultDTO(**result)
    
    def send_password_reset_email(self, to_email: str, code: int) -> EmailResultDTO:
        """Envía un email de restablecimiento de contraseña"""
        subject = "Restablecimiento de contraseña - GoScanAPI"
        body = f"""
        Hola,
        
        Has solicitado restablecer tu contraseña en GoScanAPI.
        
        Para continuar con el proceso, coloca el siguiente código en la aplicación:
        {code}
        
        Este código expirará en 1 hora.
        
        Si no solicitaste este cambio, puedes ignorar este email.

        Saludos,
        El equipo de GoScanAPI
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>Restablecimiento de contraseña</h2>
            <p>Hola,</p>
            <p>Has solicitado restablecer tu contraseña en GoScanAPI.</p>
            <p>Para continuar con el proceso, coloca el siguiente código en la aplicación:</p>
            <p><strong>{code}</strong></p>
            <p>Este código expirará en 1 hora.</p>
            <p>Si no solicitaste este cambio, puedes ignorar este email.</p>
            <br>
            <p>Saludos,<br>El equipo de GoScanAPI</p>
        </body>
        </html>
        """
        
        payload = {
            'to': to_email,
            'subject': subject,
            'body': body,
            'html_body': html_body
        }
        
        result = self._email_sender.send_email(payload)
        
        return EmailResultDTO(**result)
    
    def send_notification_email(self, to_email: str, subject: str, message: str, html_message: str = None) -> EmailResultDTO:
        """Envía un email de notificación personalizado"""
        payload = {
            'to': to_email,
            'subject': subject,
            'body': message
        }
        
        if html_message:
            payload['html_body'] = html_message
        
        result = self._email_sender.send_email(payload)
        
        return EmailResultDTO(**result)
    
    def send_bulk_notification(self, email_list: List[str], subject: str, message: str, html_message: str = None) -> BulkEmailResponseDTO:
        """Envía notificaciones masivas"""
        # Preparar datos para envío masivo
        emails_data = []
        for email in email_list:
            email_data = {
                'to': email,
                'subject': subject,
                'body': message
            }
            if html_message:
                email_data['html_body'] = html_message
            emails_data.append(email_data)
        
        # Enviar emails
        results = self._email_sender.send_bulk_email(emails_data)
        
        # Convertir resultados a DTOs
        email_results = [EmailResultDTO(**result) for result in results]
        
        # Calcular estadísticas
        total_sent = sum(1 for result in email_results if result.success)
        total_failed = len(email_results) - total_sent
        
        return BulkEmailResponseDTO(
            results=email_results,
            total_sent=total_sent,
            total_failed=total_failed
        )
    
    def send_email_from_dto(self, email_dto: EmailMessageDTO) -> EmailResultDTO:
        """Envía un email usando un DTO"""
        payload = {
            'to': email_dto.to,
            'subject': email_dto.subject,
            'body': email_dto.body
        }
        
        if email_dto.cc:
            payload['cc'] = email_dto.cc
        if email_dto.bcc:
            payload['bcc'] = email_dto.bcc
        if email_dto.html_body:
            payload['html_body'] = email_dto.html_body
        
        result = self._email_sender.send_email(payload)
        
        return EmailResultDTO(**result)
    
    def send_bulk_from_dto(self, bulk_request: BulkEmailRequestDTO) -> BulkEmailResponseDTO:
        """Envía emails masivos usando un DTO"""
        # Convertir DTOs a diccionarios
        emails_data = []
        for email_dto in bulk_request.emails:
            email_data = {
                'to': email_dto.to,
                'subject': email_dto.subject,
                'body': email_dto.body
            }
            if email_dto.cc:
                email_data['cc'] = email_dto.cc
            if email_dto.bcc:
                email_data['bcc'] = email_dto.bcc
            if email_dto.html_body:
                email_data['html_body'] = email_dto.html_body
            emails_data.append(email_data)
        
        # Enviar emails
        results = self._email_sender.send_bulk_email(emails_data)
        
        # Convertir resultados a DTOs
        email_results = [EmailResultDTO(**result) for result in results]
        
        # Calcular estadísticas
        total_sent = sum(1 for result in email_results if result.success)
        total_failed = len(email_results) - total_sent
        
        return BulkEmailResponseDTO(
            results=email_results,
            total_sent=total_sent,
            total_failed=total_failed
        )
    
    def test_email_connection(self) -> bool:
        """Prueba la conexión del servicio de email"""
        return self._email_sender.test_connection() 