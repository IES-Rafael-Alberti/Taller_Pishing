"""
🎣 SCRIPT DE ENVÍO DE CORREOS PHISHING (EDUCATIVO)

INSTRUCCIONES DE USO (TALLER):

1. PRIMERO: Inicia el Servidor SMTP Simulado (Terminal 1)
   Este comando crea un "buzón falso" que imprimirá los correos en pantalla:
   
   >>> python -m smtpd -n -c DebuggingServer localhost:1025

2. SEGUNDO: Inicia el Servidor Web del Phishing (Terminal 2)
   >>> docker run -it --rm -p 5000:5000 taller-phishing
   O sin Docker:
   >>> python app.py

3. TERCERO: Ejecuta este script de envío (Terminal 3)
   >>> python scripts/enviar_correo.py

   - Te pedirá un correo destinatario (ej: victima@test.com)
   - Revisa la Terminal 1 para ver cómo "llega" el correo

⚠️ NOTA: Este script usa un servidor SMTP LOCAL DE PRUEBAS.
   Los correos NO se envían a internet, solo se muestran en la terminal.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo_phishing(destinatario, url_phishing="http://localhost:5000"):
    # --- CONFIGURACIÓN ---
    remitente = "security@instagram.com"  # Remitente falso (spoofing)
    asunto = "🔒 Alerta de Seguridad - Nuevo inicio de sesión detectado"
    
    # Servidor SMTP local de pruebas
    smtp_server = "localhost"
    smtp_port = 1025

    # --- HTML DEL CORREO (Incluido directamente) ---
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Security Alert</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #fafafa; margin: 0; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: white; border: 1px solid #dbdbdb; border-radius: 8px; overflow: hidden;">
            <!-- Header -->
            <div style="background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 32px; font-weight: bold;">Instagram</h1>
            </div>
            
            <!-- Body -->
            <div style="padding: 30px;">
                <h2 style="color: #262626; font-size: 24px; margin-bottom: 20px;">🔒 Alerta de Seguridad</h2>
                
                <p style="color: #262626; font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
                    Hola,
                </p>
                
                <p style="color: #262626; font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
                    Detectamos un <strong>inicio de sesión inusual</strong> en tu cuenta de Instagram desde una ubicación desconocida:
                </p>
                
                <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <p style="margin: 0; color: #856404; font-size: 14px;">
                        <strong>📍 Ubicación:</strong> Moscú, Rusia<br>
                        <strong>🕒 Fecha:</strong> 18 de Enero, 2026 - 03:42 AM<br>
                        <strong>💻 Dispositivo:</strong> Windows 10 - Chrome
                    </p>
                </div>
                
                <p style="color: #262626; font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
                    Si <strong>NO fuiste tú</strong>, te recomendamos asegurar tu cuenta inmediatamente.
                </p>
                
                <!-- Button -->
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{url_phishing}" style="background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%); color: white; text-decoration: none; padding: 14px 40px; border-radius: 8px; font-size: 16px; font-weight: bold; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        ✓ Verificar Actividad
                    </a>
                </div>
                
                <p style="color: #8e8e8e; font-size: 14px; line-height: 1.6; margin-top: 20px;">
                    Si fuiste tú quien inició sesión, puedes ignorar este mensaje.
                </p>
                
                <hr style="border: none; border-top: 1px solid #dbdbdb; margin: 30px 0;">
                
                <p style="color: #8e8e8e; font-size: 12px; line-height: 1.6;">
                    Este es un correo automático del sistema de seguridad de Instagram.<br>
                    Por favor no respondas a este mensaje.
                </p>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #fafafa; padding: 20px; text-align: center; border-top: 1px solid #dbdbdb;">
                <p style="color: #8e8e8e; font-size: 12px; margin: 5px 0;">
                    © 2026 Instagram from Meta
                </p>
                <p style="color: #8e8e8e; font-size: 12px; margin: 5px 0;">
                    <a href="#" style="color: #0095f6; text-decoration: none;">Centro de Ayuda</a> • 
                    <a href="#" style="color: #0095f6; text-decoration: none;">Términos</a> • 
                    <a href="#" style="color: #0095f6; text-decoration: none;">Privacidad</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    # --- CREAR EL MENSAJE ---
    msg = MIMEMultipart("alternative")
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto

    # Parte de texto plano por si el HTML falla
    text = f"""
    Instagram Security Alert
    
    Detectamos un inicio de sesión inusual en tu cuenta desde Moscú, Rusia.
    
    Ubicación: Moscú, Rusia
    Fecha: 18 de Enero, 2026 - 03:42 AM
    Dispositivo: Windows 10 - Chrome
    
    Si no fuiste tú, por favor asegura tu cuenta inmediatamente en:
    {url_phishing}
    
    Si fuiste tú, puedes ignorar este mensaje.
    
    ---
    Instagram Security Team
    © 2026 Instagram from Meta
    """

    # --- CREAR EL MENSAJE ---
    msg = MIMEMultipart("alternative")
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto

    # Adjuntar ambas versiones (Texto y HTML)
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html_content, "html")
    msg.attach(part1)
    msg.attach(part2)

    # --- ENVIAR ---
    try:
        print(f"[*] Conectando al servidor SMTP en {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        
        print(f"[*] Enviando correo a {destinatario}...")
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()
        
        print(f"\n✅ [+] Correo enviado exitosamente a {destinatario}")
        print(f"📧 De: {remitente}")
        print(f"📌 Asunto: {asunto}")
        print(f"🔗 URL Phishing: {url_phishing}")
        print("\n[i] Revisa la terminal donde corre el servidor SMTP simulado (Terminal 1) para ver el contenido completo del correo.")
        
    except ConnectionRefusedError:
        print("\n❌ [-] Error: No se pudo conectar al servidor SMTP.")
        print("\n💡 SOLUCIÓN: Asegúrate de tener el servidor SMTP simulado corriendo en otra terminal:")
        print("   >>> python -m smtpd -n -c DebuggingServer localhost:1025\n")
        
    except Exception as e:
        print(f"\n❌ [-] Error al enviar el correo: {e}")

def main():
    print("=" * 60)
    print("🎣 SIMULADOR DE CORREOS PHISHING (EDUCATIVO)")
    print("=" * 60)
    print("\n⚠️  IMPORTANTE: Este script es solo para fines educativos.")
    print("   Los correos NO se envían a internet, solo se muestran en terminal.\n")
    
    # Solicitar datos
    target = input("📧 Introduce el correo de la víctima simulada: ").strip()
    
    if not target:
        print("\n❌ Error: Debes introducir un correo.")
        return
    
    # Preguntar si quiere personalizar la URL
    print(f"\n🔗 URL actual del phishing: http://localhost:5000")
    cambiar = input("¿Quieres usar otra URL? (s/N): ").strip().lower()
    
    if cambiar == 's':
        url_custom = input("Introduce la URL completa: ").strip()
        if url_custom:
            enviar_correo_phishing(target, url_custom)
        else:
            enviar_correo_phishing(target)
    else:
        enviar_correo_phishing(target)

if __name__ == "__main__":
    main()
