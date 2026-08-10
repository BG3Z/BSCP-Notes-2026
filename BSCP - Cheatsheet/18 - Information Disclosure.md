```
phpinfo
robots
error traces
backup files exposed
TRACE /admin information disclosure
```
##### Custom HTTP headers?
use OPTIONS for protocols
use TRACE for headers
Notice X-Custom-IP-Authorization: 81.33.215.45 is being reflected
add X-Custom-IP-Authorization: with 127.0.0.1
GET /admin/delete?username=carlos

![[Pasted image 20260728164724.png]]
##### git exposed
/ffuf -c -w /usr/share/seclists/Discovery/Web-Content/big.txt -u https://0af200f8048145328134cb5100bb00a3.web-security-academy.net/FUZZ -fc 404
.git found
https://github.com/arthaud/git-dumper
git status
git reset --hard
git show ..

---

- [Fuzzing](https://portswigger.net/web-security/information-disclosure/exploiting#fuzzing)
- [Usando el escaner de Burp](https://portswigger.net/web-security/information-disclosure/exploiting#using-burp-scanner)
- [Usando las herramientas de participación de Burp](https://portswigger.net/web-security/information-disclosure/exploiting#using-burp-s-engagement-tools)
- [Ingeniería de respuestas informativas.](https://portswigger.net/web-security/information-disclosure/exploiting#engineering-informative-responses)
* >Engagement Tools>Discover **Content**
* >Engagement Tools>Discover **Comments**

```python
wget https://raw.githubusercontent.com/botesjuan/Burp-Suite-Certified-Practitioner-Exam-Study/main/wordlists/burp-labs-wordlist.txt

ffuf -c -w ./burp-labs-wordlist.txt -u https://TARGET.web-security-academy.net/FUZZ
```

### Disclosure Information Via Error Message: 

![[Pasted image 20260810213725.png]]

### Disclosure Information Via Debug Page: 

![[Pasted image 20260810213729.png]]

![[Pasted image 20260810213732.png]]

![[Pasted image 20260810213735.png]]

![[Pasted image 20260810213739.png]]

### Disclosure Information Via Backup Files: 

![[Pasted image 20260810213742.png]]

![[Pasted image 20260810213745.png]]

![[Pasted image 20260810213749.png]]

Se puede apreciar como contiene la contraseña de la DB. (Estos resumenes son solo con fines de poder demostrar rapidamente los dislosures que hicé de los labs de portswigger, para hacerme una idea rápida en caso de que los necesite durante el examen). 

### Disclosure information Via omisión de Autenticación

![[Pasted image 20260810213753.png]]

El header de la response X-Custom-IP-Authorization tiene la clave de esto, admin interface solo accesible a través de la interfaz local, localhost, 127.0.0.1 etc.

![[Pasted image 20260810213756.png]]

### Disclosure information Via Git History 
* Una forma de encontrar este directorio y todos los demás posibles es con `FFUF` con el comando de arriba: 
![[Pasted image 20260810213803.png]]

```python
ffuf -c -w ./burp-labs-wordlist.txt -u https://ID-LAB.web-security-academy.net/FUZZ
```

![[Pasted image 20260810213807.png]]

![[Pasted image 20260810213813.png]]

Descargar el lab con wget e inspeccionar como detective todo el historial de git, el comando ganador para este ataque fue: (toca tener paciencia que se descargue todo)
`wget -r "https://ID-LAB.web-security-academy.net/.git"`

```
git show <hash del commit> - PAYLOAD

git log --stat --patch - ADICIONAL PAYLOAD PARA VER TODO A DETALLE.
```

![[Pasted image 20260810213821.png]]

