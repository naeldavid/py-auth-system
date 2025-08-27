import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class SecureEmailSender:
    def __init__(self):
        # Gmail SMTP configuration
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.sender_email = "your-email@gmail.com"  # Replace with your Gmail
        self.password = "your-app-password"         # Replace with Gmail app password
    
    def send_2fa_code(self, recipient_email: str, code: str, username: str) -> bool:
        """Send professional 2FA verification email"""
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
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return True
            
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False

# Test function
def test_email():
    sender = SecureEmailSender()
    success = sender.send_2fa_code("nael@famille-david.com", "123456", "nael")
    print(f"Email sent: {success}")

if __name__ == "__main__":
    test_email()