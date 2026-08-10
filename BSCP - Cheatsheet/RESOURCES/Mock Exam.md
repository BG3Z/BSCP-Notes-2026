# 🛡️ BSCP Examen: Reporte de Vulnerabilidades

> [!INFO] Resumen
> Apuntes sobre los vectores de ataque y vulnerabilidades encontradas durante los dos intentos del examen **Burp Suite Certified Practitioner (BSCP)**, junto con consejos para afrontar la certificación.

---

## ❌ Primer Intento

### 🌐 Web 1

*   **Fase 1 (Host Header Attack):** Existía un ataque de cabecera de host a través de `X-Host`. No había caché. No logré explotar la vulnerabilidad (apuntaba a ser un tipo de *HTTP Request Smuggling*, pero no llegué a sacar cuál era exactamente).
*   **Fase 2:** *- Sin resolver -*
*   **Fase 3:** *- Sin resolver -*

### 🌐 Web 2

*   **Fase 1 (WAF Bypass & XSS):** En el buscador existía un **WAF** que bloqueaba ciertas etiquetas y atributos. 
	*   **Solución:** A través del *Intruder* descubrí que estaba permitida la etiqueta `<body>` con el atributo `onload`. Se le enviaba a la víctima un payload XSS para exfiltrar sus cookies y se realizaba el login con la cookie robada.
*   **Fase 2 (Broken Access Control):** Una vez logueado, la funcionalidad en el apartado *"Forgot Password"* cambiaba. 
	*   **Solución:** Al poner un nombre de usuario y enviar la solicitud con tu propia cookie de sesión válida, el servidor te devolvía en la respuesta la cookie de sesión válida del usuario proporcionado. Solo había que solicitar el usuario `administrator` para conseguir su sesión.
*   **Fase 3 (OS Command Injection):** En el apartado de administración había unas imágenes que se obtenían a través de un `GET`:
	```http
	/images/?path=15.jpg&size="100x200!"
	```
	*   **Solución:** Lo primero que puedes pensar es en un *Path Traversal*, pero tras probar un buen rato, resultó ser un **OS Command Injection** contra el parámetro `size`. Podías enviar la siguiente solicitud para forzar un `POST` contra una URL de Burp Collaborator y exfiltrar el contenido del fichero:
	```http
	/images/?path=15.jpg&size="100x200!;COMANDO;"
	```

---

## ✅ Segundo Intento (COMPLETADO)

### 🌐 Web 1

*   **Fase 1 (Username Enumeration & Brute Force):** Existía una vulnerabilidad de enumeración de usuarios en el apartado de *"Forgot Password"*. Al introducir un nombre, el servidor respondía con un mensaje distinto dependiendo de si el usuario existía o no.
	*   **Solución:** Se descubrieron 3 usuarios: `administrator`, `carlos` y `ak`. Como los dos primeros son usuarios "default", se procedió a realizar un ataque de fuerza bruta de contraseñas contra el usuario `ak`, logrando acceder.
*   **Fase 2 (Information Disclosure & CSRF/XSS):** En el apartado de *My Account* había un script que mostraba una URL de la cual se obtenía la *API Key*. La ruta era similar a esta:
	```http
	/userinfo/?unixtime=171726362
	```
	*   **Solución:** Esa ruta no solo devolvía la *API Key*, sino también las cookies de sesión activas. Se montó un script para exfiltrar esta información del administrador forzando la petición:
	```javascript
	"/userinfo/?unixtime=" + Date.now()
	```
	Al robar la información, obtenías la cookie y podías loguearte como `administrator`.
*   **Fase 3 (SSTI):** Un *Server-Side Template Injection* muy claro. 
	*   **Solución:** Se identificó que el motor era Python (el payload `3*'7'` devolvía `3333333`) y se descartó Django. Tras unos 40 minutos de pruebas, se encontró el payload correcto (probablemente Jinja2) para obtener la ejecución de comandos y la solución final.

### 🌐 Web 2

*   **Fase 1 (Web Cache Poisoning):** Cambiando la cabecera `X-Host` podías alterar un recurso que se estaba cacheando.
	*   **Solución:** Se inyectó la URL del *Exploit Server* en la cabecera para envenenar la caché y forzar a la víctima a enviar sus cookies.
*   **Fase 2 (Broken Access Control):** Igual que en el primer intento. Con el *"Forgot Password"* podías obtener una cookie de sesión válida para el usuario que escribieras en el parámetro.
*   **Fase 3 (OS Command Injection):** Exactamente igual a la del primer intento. Inyección de comandos en el sistema a través del parámetro `size` de la imagen.

---

## 💡 Recomendaciones Post-Certificación

> [!TIP] Consejos de preparación
> Por lo que he estado leyendo, no suelen aparecer vulnerabilidades en el examen que estén por debajo del nivel *"Essential Skills"*, aunque siempre se recomienda verlas todas.

1. **Hacer toda la PortSwigger Academy:** Completar todos los laboratorios de la academia al menos hasta el apartado de *Essential Skills*.
2. **No infravalorar los Mystery Labs:** Al principio parecen alejados de la situación real del examen porque no te dan el objetivo a lograr (error de mi primer intento). Tras hacer unos **50 Mystery Labs**, confirmo que **sí sirven, y mucho**.
	* *¿Por qué?* Aprendes a mapear todas las funcionalidades de la web, a identificar cuáles pueden ser vulnerables a ciegas y a deducir el impacto. Esto es crucial para aprender a descartar vías muertas rápido en el examen real.
3. **Exámenes de prueba (Practice Exams):**
	* Están bien para entender cómo es el entorno real.
	* *Desventaja:* A día de hoy, los 2 exámenes de prueba disponibles son prácticamente idénticos en sus 3 fases.
	* *Recomendación:* Hazlos solo cuando te sientas **realmente preparado**, ya que al ser solo dos, quemarás esas balas rápidamente.