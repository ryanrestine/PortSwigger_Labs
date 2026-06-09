# Lab: Username enumeration via account lock

### Instructions

This lab is vulnerable to username enumeration. It uses account locking, but this contains a logic flaw. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

- Candidate usernames - https://portswigger.net/web-security/authentication/auth-lab-usernames
- Candidate passwords - https://portswigger.net/web-security/authentication/auth-lab-passwords

### Solution

I'm not really sure what the issue with this lab was, whether there is a problem with the lab itself or if it was user-error on my end, but I was never able to solve this lab manually using Burp Suite. 

I do not have Burp pro and am using the community edition, but despite reading the solution as well as several other walkthroughs, I never was able to isolate a valid username based on account lock info. I've read of a few others out there who experienced this as well.

Instead I was able to solve the lab via a custom Python script (see auth_07.py).

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Authentication/Auth_07_username_enumeration_via_account_lock]
└─$ python auth_07.py https://0a7d00cc04fb4506859ef4dd00e70003.web-security-academy.net/ ../candidate_usernames.txt ../candidate_passwords.txt
[*] Target: https://0a7d00cc04fb4506859ef4dd00e70003.web-security-academy.net/login
[*] Enumerating usernames...
[*] Trying: atlas               
[+] Valid username: atlas
[*] Waiting 65 seconds for lockout to reset...
[*] Bruteforcing password for: atlas
[*] Trying: yankees             
[+] Valid password: yankees
[*] Waiting 65 seconds for lockout to reset before final login...
[+] Logged in as atlas:yankees
[+] Lab solved
```

Here is the PortSwigger solution, but again, this did not work for me, and after several days of fiddling with it, it didn't seem worth my time to solve manually anymore. 


1. With Burp running, investigate the login page and submit an invalid username and password. Send the POST /login request to Burp Intruder.
2. Select Cluster bomb attack from the attack type drop-down menu. Add a payload position to the username parameter. Add a blank payload position to the end of the request body by clicking Add §. The result should look something like this:
`username=§invalid-username§&password=example§§`
3. In the Payloads side panel, add the list of usernames for the first payload position. For the second payload position, select the Null payloads type and choose the option to generate 5 payloads. This will effectively cause each username to be repeated 5 times. Start the attack.
4. In the results, notice that the responses for one of the usernames were longer than responses when using other usernames. Study the response more closely and notice that it contains a different error message: You have made too many incorrect login attempts. Make a note of this username.
5. Create a new Burp Intruder attack on the POST /login request, but this time select Sniper attack from the attack type drop-down menu. Set the username parameter to the username that you just identified and add a payload position to the password parameter.
6. Add the list of passwords to the payload set and create a grep extraction rule for the error message. Start the attack.
7. In the results, look at the grep extract column. Notice that there are a couple of different error messages, but one of the responses did not contain any error message. Make a note of this password.
8. Wait for a minute to allow the account lock to reset. Log in using the username and password that you identified and access the user account page to solve the lab.

