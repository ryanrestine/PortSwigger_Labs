# Lab: 2FA simple bypass

### Instructions

This lab's two-factor authentication can be bypassed. You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. To solve the lab, access Carlos's account page.

```
Your credentials: wiener:peter
Victim's credentials carlos:montoya
```

### Solution

Using the testing credentials `wiener:peter` we can login to the application, where a 2fa input is found. Once logged in, and before we input the 2fa pin, we can select the button "Email client".

This forwards us to: `https://exploit-0a82002103ca610a81476a3901bf0043.exploit-server.net/email`

Following this we find a note:

```
Hello!

Your security code is 1474.

Please enter this in the app to continue.

Thanks,
Support team
```

This code can be used for the 2fa input.

Once entered we are directed to: `/my-account?id=wiener`

We can recreate the steps using carlos' provided credentials, and because we are effectively logged in even before inputting the 2fa code, we can manually navigate to: `/my-account?id=carlos` which bypasses the 2fa protection, provides account access, and solves the lab.