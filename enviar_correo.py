"""
INSTRUCCIONES DE USO (TALLER):

1. PRIMERO: Inicia el Servidor SMTP Simulado (Terminal 1)
   Este comando crea un "buzón falso" que imprimirá los correos en pantalla en lugar de enviarlos a internet.
   >>> python -m smtpd -n -c DebuggingServer localhost:1025

2. SEGUNDO: Inicia el Servidor Web del Phishing (Terminal 2 - Opcional para este script, pero necesario para el ataque)
   >>> python app.py

3. TERCERO: Ejecuta este script de envío (Terminal 3)
   >>> python enviar_correo.py

   - Te pedirá un correo destinatario (ej: victima@test.com).
   - Revisa la Terminal 1 para ver cómo "llega" el correo.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def enviar_correo_phishing(destinatario):
    # --- CONFIGURACIÓN (Rellenar con datos de prueba o reales) ---
    remitente = "security-alert@instagram-support.com" # Esto se puede spoofear en algunos servidores, o aparecerá "a nombre de"
    asunto = "ALERTA DE SEGURIDAD: Nuevo inicio de sesión en Windows"
    
    # Para pruebas reales, necesitas un servidor SMTP. 
    # Ejemplo con Servidor Local de Pruebas (Simulación)
    # Ejecuta en otra terminal: python -m smtpd -n -c DebuggingServer localhost:1025
    smtp_server = "localhost"
    smtp_port = 1025
    usuario_smtp = "cualquiercosa" # No se usa en modo local
    password_smtp = "cualquiercosa" # No se usa en modo local

    # --- CARGAR EL HTML DEL CORREO ---
    ruta_html = os.path.join("PruebasHTML", "email_phishing.html")
    try:
        with open(ruta_html, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_html}")
        return

    # --- CREAR EL MENSAJE ---
    msg = MIMEMultipart("alternative")
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto

    # Parte de texto plano por si el HTML falla
    text = """
    Instagram Security Alert
    
    Detectamos un inicio de sesión inusual en tu cuenta desde Rusia.
    Si no fuiste tú, por favor asegura tu cuenta inmediatamente en:
    http://localhost:5000
    """

    # Adjuntar ambas versiones (Texto y HTML)
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html_content, "html")
    msg.attach(part1)
    msg.attach(part2)

    # --- ENVIAR ---
    try:
        # En modo simulación (debugging server), no usamos starttls ni login
        server = smtplib.SMTP(smtp_server, smtp_port)
        # server.starttls() # Comentado para simulación local
        # server.login(usuario_smtp, password_smtp) # Comentado para simulación local
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()
        print(f"[+] Correo enviado exitosamente a {destinatario}")
        print("[i] Revisa la terminal donde corre el servidor SMTP simulado para ver el contenido.")
        
    except Exception as e:
        print(f"[-] Error al enviar el correo: {e}")
        print("\nNOTA: Para que funcione, necesitas configurar las variables smtp_server, usuario_smtp y password_smtp en el script.")

if __name__ == "__main__":
    target = input("Introduce el correo de la víctima: ")
    enviar_correo_phishing(target)
