# Lab: Unprotected admin functionality

### Instructions

This lab has an unprotected admin panel.

Solve the lab by deleting the user `carlos`. 

### Solution

Launching the lab a `/robots.txt` file is found: `https://0a5f00e304fcd50781d67f2d004e00f7.web-security-academy.net/robots.txt`

```
User-agent: *
Disallow: /administrator-panel
```

This reveals the application's admin panel.

Suprisingly there is not authentication needed and we can simply navigate to the dashboard:

```
https://0a5f00e304fcd50781d67f2d004e00f7.web-security-academy.net/administrator-panel
```

```
Users
wiener - Delete
carlos - Delete
```
The user carlos can be deleted, which solves the lab.

### Python Solution

See `access_control_01.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_01_unprotected_admin_functionality]
└─$ python access_control_01.py https://0ac800740444400682ca16f100b000f2.web-security-academy.net/                             
[+] Deleted Carlos... Lab solved
```