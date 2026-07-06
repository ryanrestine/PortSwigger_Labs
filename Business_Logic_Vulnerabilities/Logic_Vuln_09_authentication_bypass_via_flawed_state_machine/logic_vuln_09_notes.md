# Lab: Authentication bypass via flawed state machine

### Instructions

This lab makes flawed assumptions about the sequence of events in the login process. To solve the lab, exploit this flaw to bypass the lab's authentication, access the admin interface, and delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

Logging in as wiener we notice we get redirected to a role selection page before being taken to the home page. We also discover that `/admin` exists via content discovery. Browsing to `/admin` directly from the role selection page doesn't work though.

The interesting behavior here is what happens if we never complete the role selection step at all. We log out, turn on Burp intercept and log in again. We forward the POST to `/login` but when the GET to `/role-selector` comes through we drop it instead of forwarding it.

Browsing to the home page now we find our account has defaulted to the administrator role. The application assigned a default role when the role selection step was skipped entirely, and that default happened to be administrator.

We head to `/admin` and delete carlos to solve the lab.

### Python Solution

See `logic_vuln_09.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Business_Logic_Vulnerabilities/Logic_Vuln_09_authentication_bypass_via_flawed_state_machine]
└─$ python logic_vuln_09.py https://0ae700b204fcf5ab81ba2ff20060005d.web-security-academy.net/
[+] Logged in as wiener
[*] Skipping role selector...
[+] Administrator role granted
[*] Deleting carlos...
[+] Carlos deleted - Lab solved!
```