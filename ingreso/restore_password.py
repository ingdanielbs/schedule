import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string

def generar_contraseña():
    caracteres = string.ascii_letters + string.digits
    longitud = 10
    return ''.join(random.choice(caracteres) for i in range(longitud))

def enviar_correo(destinatario, contraseña):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    puerto = 587
    remitente = 'info.sara.tel@gmail.com'
    contraseña_smtp = 'bzjk hkez tfmo tltm'

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = 'Recuperación de contraseña - SARA'

    cuerpo = f'Tu nueva contraseña es: {contraseña}'
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Iniciar sesión en el servidor SMTP
    servidor = smtplib.SMTP(smtp_server, puerto)
    servidor.starttls()
    servidor.login(remitente, contraseña_smtp)

    # Enviar el correo electrónico
    servidor.send_message(mensaje)

    # Cerrar la conexión
    servidor.quit()

# Función principal
def recuperar_contraseña(email):
    correo_destino = email
    nueva_contraseña = generar_contraseña()
    enviar_correo(correo_destino, nueva_contraseña)

if __name__ == "__main__":
    recuperar_contraseña()
