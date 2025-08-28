import smtplib
import ssl
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class SecureEmailSender:
    def __init__(self):
        # Gmail SMTP configuration - Encrypted credentials
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        
        # Encrypted email credentials (base64 encoded)
        _encrypted_email = "YXNraW5nLmFpLnN0dWZmQGdtYWlsLmNvbQ=="
        _encrypted_password = "a215cSB5eHFjIHdteHcgd3dzcw=="
        
        # Decrypt credentials
        self.sender_email = base64.b64decode(_encrypted_email).decode('utf-8')
        self.password = base64.b64decode(_encrypted_password).decode('utf-8')

        # Check if credentials are configured
        self.configured = (self.sender_email != "your-email@gmail.com" and 
                          self.password != "your-app-password")
    
    def send_2fa_code(self, recipient_email: str, code: str, username: str) -> bool:
        """Send professional 2FA verification email"""
        # Email must be configured for security
        if not self.configured:
            print("⚠️  Email not configured! Update email_sender.py with your Gmail credentials")
            return False
            
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "🔐 Secure Authentication - Verification Code"
            message["From"] = f"Secure Auth System <{self.sender_email}>"
            message["To"] = recipient_email
            
            # HTML email template
            html = f"""
            <div style="max-width:500px;margin:0 auto;background:#1a1a1a;color:white;padding:20px;border-radius:8px">
                <h2>🔐 Verification Code</h2>
                <p>Hello {username},</p>
                <div style="background:#333;padding:15px;text-align:center;margin:15px 0;border-radius:5px">
                    <span style="font-size:24px;font-family:monospace;letter-spacing:4px">{code}</span>
                </div>
                <p>Expires in 5 minutes. Don't share this code.</p>
                <small>© Secure Auth System</small>
            </div>
            """
            
            # Plain text version
            text = f"""
            Secure Authentication - Verification Code
            
            Hello {username},
            
            Your two-factor authentication code is: {code}
            
            This code expires in 5 minutes.
            
            Security Notice:
            - Never share this code with anyone
            - If you didn't request this, ignore this email
            
            Verification requested at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            © 2024 Secure Authentication System
            """
            
            # Create parts
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            
            message.attach(part1)
            message.attach(part2)
            
            # Send email
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return True
            
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False

