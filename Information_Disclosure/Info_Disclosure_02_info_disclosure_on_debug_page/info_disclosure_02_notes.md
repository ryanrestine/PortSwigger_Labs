# Lab: Information disclosure on debug page

### Instructions

This lab contains a debug page that discloses sensitive information about the application. To solve the lab, obtain and submit the `SECRET_KEY` environment variable. 

### Solution

Intercepting the URL in Burp and setting it as our target, we can inspect the site map and find the following endpoint: `/cgi-bin/phpinfo.php`

Scrolling down to the `Environment` table, the `SECRET_KEY` environment variable is found:

```
Environment
Variable	Value
GATEWAY_INTERFACE 	CGI/1.1
SUDO_GID 	10000
REMOTE_HOST 	74.194.156.33
USER 	carlos
HTTP_TE 	trailers
SECRET_KEY 	1bfx844on06rx5ijjiteu8l9yx0j8u4o 
```

We can submit this value to solve the lab.

### Python Solution

See `info_disclosure_02.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Information_Disclosure/Info_Disclosure_02_info_disclosure_on_debug_page]
└─$ python info_disclosure_02.py https://0ab500030442e406809b946e00e000fb.web-security-academy.net/
[*] Fetching SECRET_KEY environment variable...
[+] SECRET_KEY discovered
[+] SECRET_KEY: m1bv8xhraqbq4bzp3vwlwzlet8o3mhp3
[*] Submitting answer...
[+] Lab solved
```