import mysql.connector as mysqlpy
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

password = os.environ.get('EMAIL_PASSWORD')
email_from = os.environ.get('EMAIL')
email_to = os.environ.get('EMAIL')

smtp = os.environ.get('SMTP')
smtp_port = os.environ.get('SMTP_PORT')

def get_db_connection():
    user = 'root'
    password = 'example'
    host = 'localhost'
    port = '3307'
    database = 'PCO'
    bdd = mysqlpy.connect(user=user, password=password, host=host, port=port, database=database)
    return bdd

def garder_cinq_premieres_occurrences(groupe):
    return groupe.head(5)  


def send_mail(subject: str, mail: str) -> smtplib:
    '''
    envoie de mail
    -entrée: le sujet et le corps du mail
    '''
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    
    # Add text content
    text_part = MIMEText(str(mail), 'plain')
    msg.attach(text_part)

    # Connect to the SMTP server
    with smtplib.SMTP(smtp, smtp_port) as server:
        # Start TLS (Transport Layer Security) for secure communication
        server.starttls()
        
        # Login to your email account
        server.login(email_from, password)
        
        # Send the message
        server.send_message(msg)