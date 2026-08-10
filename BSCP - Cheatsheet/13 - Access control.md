Checks:
```
robots.txt

/admin route in javascript source code ctr+shift+C

cookie modification to become admin

4 - roleid can be modified in some request to become admin role (ex: {"email":"wiener@admin-user.net","roleid":2})

5 - userid can be controlled by a request parameter (ex: /my-account?id=carlos)
(Cambiando el id del usuario en la url)

6 - Hovering para descubrir el # unpredictable id de carlos mediante un post suyo

7 - Contraseña en placeholder con tipo 'password'

8 - Descargar el transcript de un live chat, lo mandamos en repeater, follow redirect y vemos que descarga el archivo X.txt, empezando en 2 (asi que descargamos el 1.txt que será el de carlos)

9 - Use X-Original-URL to bypass /admin acces denied:
GET / HTTP 1.1
X-Original-URL: /admin

10 - Take admin req, wiener cookie and change request method to POST or GET with parameters to upgrade users with wiener session

11 - Lo mismo pero con una confirmacion entre medias (la confirmacion te dejaba hacerlo con la cookie de wiener)

12 - Referer token validated being present

unpredictable user Id exposed somewhere (ex: comment href=https://0a5500a803cc582c811df86a00d40076.web-security-academy.net/blogs?userId=9cbae210-99d3-49ea-97c5-4887f8d9b73f)

Information disclosure in a redirection when changing parameters of a request (ex: ?id=carlos = 302)

Directo Object references (ex: /download-transcript/X.txt)

```

4:
![[Pasted image 20260721190704.png]]

6:
![[Pasted image 20260721191619.png]]

8:
![[Pasted image 20260721193236.png]]
![[Pasted image 20260721193257.png]]
![[Pasted image 20260721193314.png]]

9:
![[Pasted image 20260721194214.png]]

10:
![[Pasted image 20260721194630.png]]

12:
![[Pasted image 20260721195631.png]]


-----------------------------------------------------------------------

##### X-Original-URL
```
Try to load /admin and observe that you get blocked. Notice that the response is very plain, suggesting it may originate from a front-end system.
Send the request to Burp Repeater. Change the URL in the request line to / and add the HTTP header X-Original-URL: /invalid. Observe that the application returns a "not found" response. This indicates that the back-end system is processing the URL from the X-Original-URL header.

Change the value of the X-Original-URL header to /admin. Observe that you can now access the admin page.

To delete carlos, add ?username=carlos to the real query string, and change the X-Original-URL path to /admin/delete.

```


##### Username Enumeration via response timing
If username correct time response will increase every time we increase the password lenght, such as a password of 100 chars.

If blocked attempts, you can bypass it if X-Forwarded-For header is available
Select PitchFork attack, X-Forwarded-For with a number payload and username with a wordlist simple payload. Select columns send and recieve time to show the one that was made in more time than the others


Another thing to take into consideration is the resource pool tab, maybe you need to set it to 1 because 10 is to much speed to fetch a correct response.


