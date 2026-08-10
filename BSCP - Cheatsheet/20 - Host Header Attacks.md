## IMPORTANTE: 

**Cuando encuentre en un lab o en el BSCP una APP que no devuelve /admin, no tiene scripts curiosos que podamos explotar, no tiene una funcionalidad que podamos analizar para explotar, el brute force attack del LOGIN por el rate limit tampoco funciona, tampoco podemos ingresar como wiener y tras de eso el FFUF no encuentra enpoints ocultos, el ataque va directamente en modificiar algo de la request principal de la app, su host header, un nuevo param body, un web cache (si devuelve reglas de caché, etc)**

## Qué es la cabecera HTTP Host?

La cabecera HTTP Host es una cabecera de solicitud obligatoria a partir de HTTP/1.1. Especifica el nombre de dominio a la que el cliente quiere acceder. Por ejemplo, cuando un usuario visita `https://portswigger.net/web-security`, su navegador compondrá una solicitud que contiene una cabecera de Host de la siguiente manera:

```
GET /web-security HTTP/1.1
Host: portswigger.net
```

## Qué es un ataque de cabecera HTTP Host?

Los ataques de encabezados HTTP Host explotan sitios web vulnerables que manejan el valor de la cabecera de Host de una manera insegura. Si el servidor confía implícitamente en la cabecera de Host, y no lo valida o escapa adecuadamente, un atacante puede ser capaz de utilizar este intromisivo para inyectar cargas útiles dañinas que manipulan el comportamiento del lado del servidor. Los ataques que implican inyectar una carga útil directamente en la cabecera de Host a menudo se conocen como ataques de "inyección de cabecera de hosta".

Cualquiera de estos headers a añadir. 
- `X-Host`
- `X-Forwarded-Server`
- `X-HTTP-Host-Override`
- `Forwarded`

---

1. Change Host Header to your exploit server to exfiltrate password reset token

2. Bypass authorization by setting Host: localhost

3. Add a Second 'Host' Header reflected in response -> Cache Poisoning
![[Pasted image 20260731165731.png]]

4. SSRF to access admin panel somewhere in 192.168.1.0/24:
	* Uncheck 'Update Host Header to match target' on Intruder:
	* Host: 192.168.0.§1§
	* Bruteforce 1 to 255 and access admin panel

5. You can add full URL as GET https://lab/ and then set arbitrary 'Host' header:
![[Pasted image 20260731171654.png]]

6. Duplicate request with GET /admin and Host 192.168.0.1 and send in **SEQUENCE** (in the exam it would be probably localhost:6566):
![[Pasted image 20260731172533.png|299]]
* First Request:
![[Pasted image 20260731172548.png]]
* Second Request:
![[Pasted image 20260731172716.png]]

