# Lab: Username enumeration via different responses

### Instructions

This lab is vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:

- Candidate usernames - https://portswigger.net/web-security/authentication/auth-lab-usernames
- Candidate passwords - https://portswigger.net/web-security/authentication/auth-lab-passwords

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page. 

### Solution

Clicking on `/login` we can enter a random string for the username `testing` and any character for the password and we get the message: `Invalid username`.

Let's capture this request in Burp and send it to Intruder for testing.

Once the request is in Intruder, we can paste in the provided usernames list in a Sniper attack, input any password we'd like, and begin to bruteforce, searching for a different response message which would indicate we have discovered a valid username. 

```
POST /login HTTP/1.1
Host: 0a2b00cc036213698149934a0022008c.web-security-academy.net
Cookie: session=dKZVdo1fdQItvhHyNTq1n5eXjAOHGqA6
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 27
Origin: https://0a2b00cc036213698149934a0022008c.web-security-academy.net
Referer: https://0a2b00cc036213698149934a0022008c.web-security-academy.net/login
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive

username=test&password=test
```

Running Intruder, each response size is 3352, except one:

```
18	azureuser	200	333	false	false	3354	
```

This response size is 3354.

Inspecting this username's response in Burp we find the error:

`Incorrect password` Letting us know we now have a working username.

We can repeat our steps with Intruder, now entering the username `azureuser` as the username and pasting in the provided passwords list to brute force the users password:

`username=azureuser&password=test`

This time only one request returns a 302 status code (redirect), while all others return a 200:

```
74	ginger	302	328	false	false	191	
```

This let's us know we have discovered working credentials: `azureuser:ginger`.

These can be used to login to the app and finish the lab.