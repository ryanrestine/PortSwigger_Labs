# Lab: Inconsistent security controls

### Instructions

This lab's flawed logic allows arbitrary users to access administrative functionality that should only be available to company employees. To solve the lab, access the admin panel and delete the user carlos. 

### Solution

Looking at the site there is a `register` page with the note:

```
If you work for DontWannaCry, please use your @dontwannacry.com email address
```

Supplying test data to register an account we are given the following message:

```
Please check your emails for your account registration link
```

Registering an account and inputting the provided exploit server/ email client address, we get an registration email:

```
Hello!

Please follow the link below to confirm your email and complete registration.

https://0a180023041ae72e81f452ed00f3004c.web-security-academy.net/register?temp-registration-token=LCTphEpkRgshjpQGC79Bkog1QGyu0cPD

Thanks,
Support team
```

We can follow this link to register our account.

Once logged in there is an option to update our email. We can update this to `test@dontwannacry.com` based on the note found on the site.

Once this is updated, a new link appears in the menu to navigate to the admin panel.

```
Home - Admin panel - My account - Log out
```

We can then delete the user carlos to solve the lab:

```

Users
wiener - Delete
carlos - Delete
test - Delete
```

### Python Solution

See `logic_vuln_03.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Business_Logic_Vulnerabilities/Logic_Vuln_03_inconsistent_security_controls]
└─$ python logic_vuln_03.py https://0ad200ba037c74a78137bb440024009e.web-security-academy.net/
[*] Registering the account test:test...
target: https://0ad200ba037c74a78137bb440024009e.web-security-academy.net
[+] The email client address is: https://exploit-0ad5007803fc748d81e3ba910103001e.exploit-server.net/email
[*] Registering with email: test@exploit-0ad5007803fc748d81e3ba910103001e.exploit-server.net
[*] Grabbing confirmation link...
[+] Confirmation link: https://0ad200ba037c74a78137bb440024009e.web-security-academy.net/register?temp-registration-token=rb7Uc7NKsK1ktqH5gBA0OHidc85ect53
[+] Login successful
[*] Changing email to: test@dontwannacry.com
[*] Deleting user Carlos from admin panel...
[+] Lab solved
```