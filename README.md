# 🎣 Taller_Phishing

Bienvenidos al taller de Phishing en donde podrás sustraer cuentas de manera educativa. 😈

Este proyecto utiliza Docker para ejecutar una herramienta de simulación de phishing en un entorno seguro y aislado.

**Objetivo:** Demostrar la facilidad con la que se pueden clonar webs para aprender a identificar estos fraudes.

**Prohibido:** Utilizar esta herramienta contra objetivos reales o personas sin su consentimiento.

**Responsabilidad:** El usuario es el único responsable de sus acciones.

---

## 📊 ¿Qué incluye este taller?

- 🔵 **Instagram Clone**: Página de login idéntica a Instagram
- 📶 **WiFi Portal**: Portal cautivo falso (Evil Twin)
- 📈 **Dashboard en Tiempo Real**: Ve las capturas mientras ocurren
- 🎓 **Página Educativa**: Enseña a identificar señales de phishing
- 💾 **Base de Datos**: Guarda todos los datos capturados
- 📊 **Exportación CSV**: Descarga los resultados para análisis

---

## 🚀 Guía Paso a Paso

Abre tu terminal dentro de esta carpeta (`Taller_Pishing`) y sigue las instrucciones.

### 1️⃣ Construir el contenedor

Lo primero es "fabricar" nuestro contenedor. Este comando leerá el archivo Dockerfile, descargará las dependencias de internet y preparará todo el sistema automáticamente.

Ejecuta este comando (¡no olvides el punto al final!):

```bash
docker build -t taller-phishing .
```

💡 *En caso de que te salga error de permisos en Linux escribe `sudo` delante*

⏱️ *Primera vez: ~2-3 minutos*

---

### 2️⃣ El arranque

```bash
docker run -it --rm -p 5000:5000 taller-phishing
```

🎉 **¡Listo!** El servidor está corriendo.

---

### 3️⃣ Acceder a las páginas (La Víctima)

Ahora que el servidor está corriendo, abre tu navegador web y visita:

#### 📱 Opción A: Probar en tu ordenador (Localhost)

- **Instagram Clone**: http://localhost:5000
- **WiFi Portal**: http://localhost:5000/wifi
- **Dashboard Admin**: http://localhost:5000/admin
- **Demo Correo Phishing**: http://localhost:5000/email-demo 📧

#### 🌐 Opción B: Compartir en clase (Red Local)

Si quieres que tus compañeros accedan desde sus dispositivos:

**Windows:**
```powershell
# 1. Obtén tu IP
ipconfig
# Busca "Dirección IPv4" (ej: 192.168.1.100)

# 2. Abre el firewall (ejecutar como administrador)
New-NetFirewallRule -DisplayName "Taller Phishing" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# 3. Comparte esta URL con tus compañeros
http://TU_IP:5000  # Ej: http://192.168.1.100:5000
```

**Linux/Mac:**
```bash
# Obtén tu IP
ip addr show
# o
ifconfig

# Comparte esta URL
http://TU_IP:5000
```

⚠️ **Nota:** Todos deben estar en la misma red WiFi.

#### 🚀 Opción C: Túnel Público (Cloudflared) - ¡URL Realista!

Para obtener una URL pública accesible desde **cualquier lugar** con HTTPS (perfecto para presentaciones):

```powershell
# Ejecutar script automatizado
.\scripts\iniciar_tunel_publico.ps1
```

Este script generará una URL como:
```
https://palabras-aleatorias-aqui.trycloudflare.com
```

✅ **Ventajas:**
- Accesible desde cualquier dispositivo con internet
- HTTPS automático (más realista)
- No necesitas estar en la misma red WiFi

⚠️ **Importante:** La URL es temporal y cambia cada vez.

---

### 4️⃣ Monitorear las capturas (El Atacante)

#### En la Terminal
Todos los datos capturados aparecerán en tiempo real en la terminal donde ejecutaste el contenedor.

#### En el Dashboard Web 📊

Abre el dashboard administrativo para ver estadísticas profesionales:

```
http://localhost:5000/admin
```

**¿Qué verás?**
- 📈 Estadísticas: Visitantes, víctimas, tasa de conversión
- 📉 Gráfico timeline: Capturas por hora (últimas 24h)
- 🌍 Top IPs: Ranking de dispositivos más activos
- 📋 Tabla completa: Todas las credenciales capturadas
- 💾 Exportar CSV: Descarga los datos
- � Ver ejemplo de correo phishing: Muestra cómo se vería un email real
- 🔄 Auto-refresh: Se actualiza solo cada 10 segundos

💡 **Tip:** Abre el dashboard en una segunda pantalla durante tu presentación.

#### 📧 Demo de Correo Phishing

Para mostrar a tus compañeros cómo se ve un correo de phishing real:

1. **Desde el dashboard**, haz clic en "📧 Ver Ejemplo de Correo Phishing"
2. O accede directamente a: `http://localhost:5000/email-demo`

**Características de la demo:**
- ✅ Muestra un correo de Instagram falso completo
- ✅ Resalta las señales de alerta que se deben notar
- ✅ Explica las técnicas de ingeniería social usadas
- ✅ El botón muestra la URL real al pasar el mouse
- ✅ Perfecto para proyectar en clase y analizar en grupo

🎓 **Uso en clase:** Proyecta esta página y pide a tus compañeros que identifiquen las señales de phishing antes de revelar las respuestas.

---

### 5️⃣ La Experiencia Educativa 🎓

Cuando alguien ingrese sus credenciales en cualquier página falsa, será redirigido automáticamente a una **página educativa** que explica:

- 🚨 Las 5 señales de phishing que debió notar
- 📊 Estadísticas reales de phishing
- 💡 Consejos de protección
- 🔐 Mejores prácticas de seguridad

¡Así aprenden en el acto!

---

## 🛑 Cómo salir

Cuando termines la práctica:

1. Pulsa `CTRL + C` en la terminal (dos veces si es necesario)
2. El contenedor se borrará automáticamente gracias a la opción `--rm`, dejando tu ordenador limpio

---

## 📁 Estructura del Proyecto

```
Taller_Pishing/
├── app.py                    # Servidor Flask principal
├── Dockerfile               # Configuración Docker
├── requirements.txt         # Dependencias Python
├── PruebasHTML/             # Páginas HTML de phishing
│   ├── indexinsta.html      # Instagram clone
│   ├── wifi_portal.html     # WiFi portal
│   ├── educativo.html       # Página educativa
│   └── dashboard.html       # Dashboard admin
├── scripts/                 # Scripts de utilidad
│   ├── compartir_red_local.ps1
│   └── iniciar_tunel_publico.ps1
└── docs/                    # Documentación completa
    ├── README.md
    ├── IDEAS.md
    └── URL_PUBLICA.md
```

---

## 🔐 ¿Qué datos se capturan?

El servidor guarda automáticamente:

- ✅ Timestamp (fecha y hora)
- ✅ Direcciones IP de visitantes
- ✅ User-Agent (navegador/dispositivo)
- ✅ Credenciales ingresadas (usuario y contraseña)
- ✅ Escenario utilizado (Instagram, WiFi, etc.)

### Acceder a la base de datos

```bash
sqlite3 phishing_data.db

# Consultas útiles
SELECT * FROM captures;
SELECT COUNT(*) FROM visits;
SELECT scenario, COUNT(*) FROM captures GROUP BY scenario;
```

### API REST para desarrolladores

| Endpoint | Descripción |
|----------|-------------|
| `/api/stats` | Estadísticas generales |
| `/api/captures` | Últimas 100 capturas |
| `/api/timeline` | Timeline 24h |
| `/api/export/csv` | Exportar CSV |

```bash
# Ejemplo
curl http://localhost:5000/api/stats
curl http://localhost:5000/api/export/csv -o capturas.csv
```

---

## 📚 Recursos Adicionales

- 📖 [Documentación Completa](docs/README.md) - Información detallada sobre phishing
- 💡 [Ideas y Roadmap](docs/IDEAS.md) - Mejoras futuras
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - Cómo contribuir
- 📄 [LICENSE](LICENSE) - Licencia MIT

**Aprende más sobre ciberseguridad:**
- [INCIBE - Ciberseguridad](https://www.incibe.es/)
- [PhishTank - Base de datos](https://phishtank.org/)

---

## ⚠️ Responsabilidad Legal

**ESTE PROYECTO ES EXCLUSIVAMENTE EDUCATIVO**

✅ **Permitido:**
- Educación en ciberseguridad
- Demostraciones en clase
- Entrenamiento de concienciación
- Investigación en entornos controlados

❌ **PROHIBIDO:**
- Uso contra personas sin consentimiento
- Ataques a sistemas reales
- Cualquier actividad ilegal
- Distribución de datos capturados

**El usuario es 100% responsable de sus acciones. El uso indebido puede resultar en consecuencias legales graves.**

---

<div align="center">

**Hecho con ❤️ para la educación en ciberseguridad**

[⬆ Volver arriba](#-taller_phishing)

</div>
