import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import functions_framework
import os

@functions_framework.http
def cors_enabled_function(request):
    
    if request.method == "OPTIONS":
      
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

   
    headers = {"Access-Control-Allow-Origin": "*"}

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return "Dados JSON ausentes", 400

        result = send_email(data)
        return (result, 200, headers)
    else:
        return ("Método não permitido", 405, headers)

def send_email(data):
    subject = data.get("subject")
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not subject or not name or not email or not message:
        return "Campos obrigatórios ausentes"

    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT'))
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    recipient_email = os.environ.get('RECIPIENT_EMAIL')

    if not smtp_server or not smtp_port or not smtp_username or not smtp_password or not recipient_email:
        return "Configuração de e-mail ausente ou incorreta"

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient_email
    msg['Subject'] = subject

    body = f"Nome: {name}\nEmail: {email}\nAssunto: {subject}\nMensagem: {message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, recipient_email, msg.as_string())
        server.quit()
        return "E-mail enviado com sucesso!"
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {str(e)}")
        return f"Erro ao enviar o e-mail: {str(e)}"
