1. Cambiar el precio a la hora de añadir item al carrito y se refleja en la compra
2. Añadir articulos random en negativo para restarle precio al total del articulo que queremos comprar
3. Hay un mensaje que indica 'si trabajas para X, ponte un email X@dominio.com', te creas una cuenta random y en el apartado de UpdateEmail le cambias el dominio al de admin
4. Se pueden aplicar varios codigos de descuento. La web solo valida con un historial de 1 elemento que no introduzcas dos veces el ultimo introducido. entonces vas alternando entre ambos y consigues el producto por 0€
5. Al aumentar los items del carrito, y llegar al limite del int, comienza de nuevo desde los negativos, conseguimos llegar a 0 en la segunda vuelta y nos llevamos el articulo gratis
6. En la parte de crear correo tiene un limite de 255 caracteres, si pasamos ese limite te deja crear el correo pero lo interpreta por detras:
```
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA@dontwannacry.com.exploit-0a3d0072041095fa82402d7d01b2005b.exploit-server.net
```
7. En el apartado de cambiar contraseña, si borramos el argumento de `current_password`, no lo valida por detras y podemos cambiar la de cualquier usuario
![[Pasted image 20260730142953.png]]
8. Al comprar un producto te encuentras :![[Pasted image 20260730143603.png]]
- Introduciendo otro producto al carrito, y mandando de nuevo esta solicitud de confirmacion de pedido, nos saltamos el pago


```
email registration has maximun length to 255 for example, it truncates the rest, you can register a company user:
-> very-long-string@dontwannacry.com.YOUR-EMAIL-ID.web-security-academy.net (Make sure that the very-long-string is the right number of characters so that the "m" at the end of @dontwannacry.com is character 255 exactly.)
-> echo 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' | wc
-> echo 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@dontwannacry.com.exploit-0aff00310328b657827b500001bb00d0.exploit-server.net' | wc


Current password to change it can be removed to access other account


While login, if you change the GET /role-selector request to /admin in intercept, your are administrator


Oracle encryption bypass (https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-authentication-bypass-via-encryption-oracle)
-> Stay logged in encoded cookie
-> Post comment with invalid mail ('invalid') sets notification cookie that is encrypted and decrypted in the next request with oracle encryption
-> If you copy your stay-logged-in cookie into notification cookie in decrypt tab you see wiener:1711060443422, so we know the cookie is user+timestamp
-> administrator:1711060443422 has appended "Invalid email address: " so in decoder we errase 23 bytes corresponding to that
-> we get an error saying we need to have a multiple of 16, so we padd it with 9 bytes to: xxxxxxxxxadministrator:1711060443422 and delete 32 bytes in encoder
-> Once you have the notification as administrator:timestamp correctly, copy it to stay-logged-in and delete the rest, access /admin
```
