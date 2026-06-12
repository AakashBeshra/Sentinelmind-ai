import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
import aiohttp
import asyncio
from app.core.config import settings
from app.core.logging import logger

class NotificationService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST if hasattr(settings, 'SMTP_HOST') else "smtp.gmail.com"
        self.smtp_port = settings.SMTP_PORT if hasattr(settings, 'SMTP_PORT') else 587
        self.smtp_user = settings.SMTP_USER if hasattr(settings, 'SMTP_USER') else ""
        self.smtp_password = settings.SMTP_PASSWORD if hasattr(settings, 'SMTP_PASSWORD') else ""
    
    async def send_email(self, to_email: str, subject: str, body: str, html: Optional[str] = None):
        """Send email notification"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_user
            msg['To'] = to_email
            
            # Attach plain text
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach HTML if provided
            if html:
                msg.attach(MIMEText(html, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    async def send_welcome_email(self, email: str, username: str):
        """Send welcome email to new user"""
        subject = "Welcome to SentinelMind AI!"
        body = f"""
        Hi {username},
        
        Welcome to SentinelMind AI! We're excited to have you on board.
        
        Get started by:
        1. Analyzing your first text
        2. Exploring the dashboard
        3. Checking out premium features
        
        Best regards,
        SentinelMind AI Team
        """
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: auto; padding: 20px;">
                <h1 style="color: #3b82f6;">Welcome to SentinelMind AI!</h1>
                <p>Hi <strong>{username}</strong>,</p>
                <p>Welcome to SentinelMind AI! We're excited to have you on board.</p>
                <h3>Get started by:</h3>
                <ul>
                    <li>Analyzing your first text</li>
                    <li>Exploring the dashboard</li>
                    <li>Checking out premium features</li>
                </ul>
                <hr>
                <p style="color: #666;">Best regards,<br>SentinelMind AI Team</p>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(email, subject, body, html)
    
    async def send_analysis_complete_notification(self, email: str, results: Dict):
        """Send notification when batch analysis completes"""
        subject = "Your batch analysis is complete"
        body = f"""
        Your sentiment analysis batch has been processed.
        
        Summary:
        - Total analyses: {results.get('total', 0)}
        - Positive: {results.get('positive', 0)}
        - Negative: {results.get('negative', 0)}
        - Neutral: {results.get('neutral', 0)}
        
        Log in to view detailed results.
        """
        
        return await self.send_email(email, subject, body)
    
    async def send_webhook(self, webhook_url: str, payload: Dict, headers: Optional[Dict] = None):
        """Send webhook notification"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload, headers=headers or {}) as response:
                    if response.status == 200:
                        logger.info(f"Webhook sent to {webhook_url}")
                        return True
                    else:
                        logger.error(f"Webhook failed with status {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return False