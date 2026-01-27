# 🎯 Taller de Phishing - Aprende a Detectar Ataques

Bienvenido al taller donde aprenderás a identificar intentos de phishing. En 2 horas vas a ver cómo funcionan estos ataques y, más importante, cómo protegerte de ellos.

> **Nota importante:** Esto es solo educativo. Todo lo que ves aquí son simulaciones controladas.

---

## ¿Qué vamos a hacer?

Durante el taller vas a:

- Ver demos en vivo de ataques de phishing (Instagram, WiFi falsos, emails fraudulentos)
- Jugar a "Spot the Phish" - un juego interactivo con 12 escenarios reales
- Aprender las señales de alarma que debes detectar
- Llevarte un kit completo de recursos para consultar después

Al final del taller sabrás identificar la mayoría de intentos de phishing que te encuentres.

---

## 🚨 Señales de Alarma Básicas

Aprende a detectar estas red flags:

**En emails:**
- Te amenazan con urgencia ("su cuenta se bloqueará en 24h")
- El dominio del remitente no cuadra (bbva-notificaciones.com en vez de bbva.es)
- Errores gramaticales raros
- Te piden contraseñas o datos personales

**En URLs:**
- Dominios muy parecidos pero con pequeños cambios (paypa1.com, arnazon.com)
- URL que no coincide con el remitente
- Sin HTTPS (el candado)

**En mensajes:**
- Premios que nunca pediste
- Paquetes que no esperabas
- Urgencia extrema

---

## 🎮 Actividades del Taller

### 1. Demo en Vivo (20 min)
Verás cómo funcionan diferentes ataques desde dentro. Es impactante ver lo fácil que es crear una página falsa convincente.

### 2. Juego "Spot the Phish" (25 min)
12 escenarios para poner a prueba tu ojo. Cada respuesta incluye explicación de por qué es phishing o legítimo.

**URL del juego:** (el instructor te la dará)

### 3. Quiz Final (15 min)
Kahoot para cerrar y consolidar lo aprendido.

---

## 🛡️ Cómo Protegerte

### Lo básico:

1. **Verifica siempre antes de hacer clic**
   - Lee el dominio letra por letra
   - Pasa el ratón sobre los enlaces (sin hacer clic) para ver la URL real
   - Cuando tengas dudas, accede escribiendo la URL oficial tú mismo

2. **Usa un gestor de contraseñas**
   
   Esto es clave: servicios como Bitwarden (gratis) o 1Password generan contraseñas únicas para cada sitio. Y aquí viene lo mejor: **no autocompletan en sitios falsos** porque detectan que el dominio no es el correcto. Es como tener un anti-phishing automático.

3. **Activa 2FA (autenticación en dos pasos)**
   
   Incluso si roban tu contraseña, no podrán entrar sin el segundo código.

4. **Ante la duda, NO hagas clic**
   
   En serio. Mejor perder 2 minutos llamando al banco para verificar, que perder tu cuenta.

### Si ya caíste en phishing:

Actúa rápido:
1. Cambia la contraseña YA (en el sitio real, no en el enlace del phishing)
2. Activa 2FA si no lo tenías
3. Revisa actividad reciente
4. Si diste datos bancarios, llama a tu banco inmediatamente

---

## 💡 Herramientas Útiles

**Gestores de contraseñas:**
- Bitwarden (gratis, open source)
- 1Password (de pago pero muy completo)
- LastPass (tiene versión gratis)

**Para verificar URLs sospechosas:**
- VirusTotal (https://www.virustotal.com/)
- URLScan.io
- Have I Been Pwned (para ver si tu email fue filtrado)

**Apps para 2FA:**
- Google Authenticator
- Microsoft Authenticator
- Authy

---

## 📚 Recursos del Taller

Al final del taller tendrás acceso a:

- **Checklist de verificación** - Guía paso a paso para analizar emails y mensajes
- **Guía rápida** - Las 5 señales de alarma más importantes
- **Lista de herramientas** - Software recomendado con enlaces
- **Certificado** - Para que tengas constancia de tu participación

**URL del kit de recursos:** (el instructor te la dará durante el taller)

---

## ❓ Preguntas Frecuentes

**P: ¿Por qué caí en el phishing del taller?**  
R: Es normal. Los ataques están diseñados para engañar. Lo importante es que ahora sabes identificarlos.

**P: ¿Están seguros mis datos después del taller?**  
R: Sí, todo fue simulado. Los datos se borran al finalizar y nadie tiene acceso.

**P: ¿Debo cambiar mis contraseñas reales?**  
R: Solo si usaste contraseñas reales en el taller (cosa que NO deberías hacer). Si usaste contraseñas de prueba, estás bien.

**P: ¿Cómo sé si un email de mi banco es real?**  
R: Tres cosas - verifica el dominio del remitente, los bancos NUNCA piden contraseñas por email, y si dudas llama al número que está en tu tarjeta.

---

## 📞 Contactos Importantes

**España:**
- INCIBE (Instituto Nacional de Ciberseguridad): 017
- Reportar phishing: incidencias@incibe-cert.es
- Alternativamente, se puede utilizar el formulario https://www.incibe.es/incibe-cert/incidentes/notificaciones

**Tu banco:** Número en tu tarjeta (NO el del email sospechoso)

---

## 🎓 Certificado

Si completas el taller y superas el quiz final, puedes generar tu certificado digital.

---

## � Comentario Final

La ciberseguridad no es solo cosa de expertos. Con conocer unas pocas señales de alarma ya reduces muchísimo el riesgo. Comparte lo que aprendas con familia y amigos - muchos ataques funcionan porque la gente simplemente no sabe qué buscar.

Recuerda: **ante la duda, NO hagas clic**.

---

## 🔧 Para el Instructor - Setup del Taller

<details>
<summary>Click para ver instrucciones de instalación</summary>

### Requisitos previos:
- Docker instalado en tu máquina
- Tener este repositorio clonado

### Paso 1: Construir la imagen Docker

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
docker build -t taller-phishing .
```

Esto tardará 2-3 minutos la primera vez (descarga dependencias).

### Paso 2: Iniciar el contenedor

```bash
docker run -d -p 5000:5000 --name taller-phishing-test taller-phishing
```

El servidor estará corriendo en `http://localhost:5000`

### Paso 3: Verificar que funciona

Abre tu navegador y prueba:
- Instagram: http://localhost:5000/
- WiFi Portal: http://localhost:5000/wifi
- Juego: http://localhost:5000/juego
- Kit recursos: http://localhost:5000/kit
- Dashboard: http://localhost:5000/admin

### Comandos útiles:

**Ver logs del contenedor:**
```bash
docker logs taller-phishing-test
```

**Detener el contenedor:**
```bash
docker stop taller-phishing-test
```

**Eliminar el contenedor:**
```bash
docker rm taller-phishing-test
```

**Reconstruir después de cambios:**
```bash
docker stop taller-phishing-test
docker rm taller-phishing-test
docker build -t taller-phishing .
docker run -d -p 5000:5000 --name taller-phishing-test taller-phishing
```

### Para compartir en red local:

1. Obtén tu IP local:
   - Windows: `ipconfig` (busca IPv4)
   - Mac/Linux: `ifconfig` o `ip addr`

2. Comparte con los participantes:
   ```
   http://TU_IP:5000/juego
   http://TU_IP:5000/kit
   ```

3. Asegúrate de que el firewall permite conexiones al puerto 5000

### Estructura de URLs para el taller:

- `/` - Instagram phishing demo
- `/wifi` - WiFi portal falso
- `/juego` - Spot the Phish (actividad principal)
- `/kit` - Kit de supervivencia con recursos
- `/recursos/checklist` - Checklist detallado
- `/recursos/guia-rapida` - Guía rápida
- `/recursos/herramientas` - Lista de herramientas
- `/certificado` - Generador de certificados
- `/admin` - Dashboard de estadísticas
- `/educativo` - Página educativa (redirect automático)

### Notas:

- La base de datos SQLite se crea automáticamente en `phishing_data.db`
- Los datos se resetean cada vez que eliminas el contenedor
- El servidor corre en modo `debug=False` para producción

</details>

---

<div align="center">

**Mantente alerta, mantente seguro** 🛡️

</div>

