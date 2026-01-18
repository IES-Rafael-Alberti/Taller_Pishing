# 🎣 Taller_Phishing

Bienvenidos al taller de Phishing en donde podras sustraer cuentas de manera educativa. 😈

Este proyecto utiliza **Docker** para ejecutar la herramienta **Zphisher** en un entorno seguro y aislado.



* **Objetivo:** Demostrar la facilidad con la que se pueden clonar webs para aprender a identificar estos fraudes.
* **Prohibido:** Utilizar esta herramienta contra objetivos reales o personas sin su consentimiento.
* **Responsabilidad:** El usuario es el único responsable de sus acciones.

---

## 🚀 Guía Paso a Paso

Abre tu terminal dentro de esta carpeta (`Taller_Phishing`) y sigue las instrucciones.

### 1: Levantar el contenedor 

Lo primero es "fabricar" nuestro contenedor. Este comando leerá el archivo `Dockerfile`, descargará Zphisher de internet y preparará todo el sistema automáticamente.

Ejecuta este comando (no olvides el punto al final):

```bash
docker build -t taller-phishing .
```

En caso de que te salga error de permisos en Linux escribe sudo delante 

### 2: El arranque

## 🐧 Opción A: LINUX

```bash
docker run -it --rm --net=host taller-phishing```
```

## 🪟 Opción B: WINDOWS

```bash
docker run -it --rm -p 8080:8080 taller-phishing
```


### 3: Generar y Acceder (La Víctima)

Una vez dentro de la herramienta, sigue estos pasos para generar el enlace trampa y probarlo.

### 1. Dentro de la Terminal (El Atacante)

1. Elige una red social (ej: Opción `1` Facebook).
2. Elige el tipo de ataque (ej: Opción `1` Login Page).
3. **Selección del Túnel (IMPORTANTE):**
   * Elige **Cloudflared** (Suele ser la opción 2 o 3). Esto creará un enlace público de internet.
   * *Espera unos segundos a que genere las URLs.*

### 2. En tu Navegador (La Víctima)

La terminal te mostrará algo como: `URL 1: https://cuidadi-to-con-esto.trycloudflare.com`

* **Copia esa URL** que aparece en la terminal.
* Abre tu navegador web (Chrome, Firefox, Edge).
* **Pega la URL** en la barra de direcciones y pulsa Enter.
* ¡Verás la página clonada!

#### ⚠️ Nota Especial para Localhost (Windows)

Si en lugar de *Cloudflared* eliges la opción **Localhost**:
* Zphisher te dirá que la web está en `127.0.0.1:8080`.
* En Windows, abre tu navegador y escribe manualmente: `http://localhost:8080`

---

## 🛑 Cómo salir

Cuando termines la práctica:
1. Pulsa `CTRL + C` (dos veces si es necesario).
2. El contenedor se borrará automáticamente gracias a la opción `--rm`, dejando tu ordenador limpio.