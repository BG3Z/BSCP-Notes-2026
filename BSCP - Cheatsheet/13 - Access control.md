### Para el caso de URL's Impredecibles

Siempre revisar los DOM de la aplicación, en los <script></script> siempre se pueden encontrar los endpoints a puntos ciegos que se suponen que son impredecibles pero el desarrollador no los sanitizó correctamente.

![[Pasted image 20260810211309.png]]

### Checks a tener en cuenta: 

```js
1. Find /robots.txt
	//Nos aparece el Disallow: /administrator-panel ahora es tan simple como navegar a la interfaz desde la url principal y ver que podemos hacer.

2. /admin route in javascript source code ctr+shift+i
	//es un nombre de interfaz impredecible, pero basta con buscarla en el source code. 

3. cookie modification to become admin (ex: cookie-> Admin:False->Admin:True)
	//El rol de un usuario se puede modificar desde la cookie `admin` 

4. roleid can be modified in some request to become admin role (ex: {"email":"wiener@admin-user.net","roleid":2})
	//Cambiando el #del roleId podemos pasar de user normal a admin user.
	//{"roleId":1 en la POST lo podemos modificar para otro Id.} para be admin

5. Use X-Original-URL to bypass /admin acces denied:
	// GET / HTTP/1.1 OR GET /my-account HTTP/1.1
	// X-Original-URL: /admin 
	//Y así de facil podemos tener acceso a admin. 

6. userid can be controlled by a request parameter (ex: /my-account?id=carlos)
	//Podemos modificarlo por cualquier user, ex:admin

7. unpredictable user Id exposed somewhere - en los post se divulgan los ID's
	//ex: comment href=https://ID-LAB.web-security-academy.net/blogs?userId=9cbae210-99d3-49ea-97c5-4887f8d9b73f)
	//Osea basicamente en los post encontramos ids que podemos probar en el endpoint: 
	//GET /my-account?id=ID-FOUNDED

Information disclosure in a redirection when changing parameters of a request (ex: ?id=carlos = 302)

8. Direct Object references (ex: /download-transcript/X.txt) //Cambiamos el numero del file.txt pa' ver a cual podemos llegar y si se nos revela password.

9. GET /admin-roles?username=VictimUser&action=upgrade HTTP/1.1 
	//Simplemente cambiando el method POST,PUT,DELETE,diferente a GET.
	//este lo podemos modificar para subirle los privilegios a un user victim que es el que queremos aumentarle los privilegios.

10. Password disclosure <hidden> se puede ver en el DOM, con la request GET /my-account?id=wiener se puede cambiar a /my-account?id=administrator
	//Y se actualiza la password hidden por la del nuevo user que se puso en el id. 

11. Change request method to POSTX or GET with parameters ?
Referer token validated being present

12. Si llega a haber un endpoint POST /admin-roles HTTP/2 : Automaticamente tener en cuenta el body, por ejm: 
	//action=upgrade&confirmed=true&username=wiener 
	//para poder subirle los privilegios a un user normal. 

13. Referer Based Access Control
	 GET /admin-roles?username=wiener&action=upgrade con el header
	 Referer:https://ID-LAB.com/admin 
	//y así podemos subirle los privilegios a un user normal. 
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

!!!!!!!!!!!!!!!!
Another thing to take into consideration is the resource pool tab, maybe you need to set it to 1 because 10 is to much speed to fetch a correct response.
!!!!!!!!!!!!!!!!!
