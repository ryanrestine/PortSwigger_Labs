# Lab: Forced OAuth profile linking

### Instructions

This lab gives you the option to attach a social media profile to your account so that you can log in via OAuth instead of using the normal username and password. Due to the insecure implementation of the OAuth flow by the client application, an attacker can manipulate this functionality to obtain access to other users' accounts.

To solve the lab, use a CSRF attack to attach your own social media profile to the admin user's account on the blog website, then access the admin panel and delete `carlos`.

The admin user will open anything you send from the exploit server and they always have an active session on the blog website.

You can log in to your own accounts using the following credentials:

-  Blog website account: `wiener:peter`
-  Social media profile: `peter.wiener:hotdog`

### Solution


Logging in to the blog as `wiener:peter`, we go to "My account" and see an option to attach a social media profile:

```
Attach a social profile to make it easier to log in
```

Clicking it kicks off the same OAuth flow we've seen before, except this time it's not a fresh login, it's linking our social media identity (`peter.wiener`) onto our existing `wiener` blog account.

Capturing the flow in Burp, we see the familiar request to the identity provider:

```
GET /auth?client_id=...&redirect_uri=https://0aXXXXXX.web-security-academy.net/oauth-linking?email=wiener@normal-user.net&response_type=code&scope=openid%20profile%20email HTTP/2
Host: oauth-0aXXXXXX.oauth-server.net
Cookie: _session=...
```

After we authenticate with `peter.wiener:hotdog` and approve, we land on:

```
GET /oauth-linking?code=9TgCqUYsSNkEnWTwbEXL2bJVa05pGh6SLnkbOg8HLH9 HTTP/2
Host: 0aXXXXXX.web-security-academy.net
Cookie: session=...
```

This is the important request as the blog app exchanges this `code` for a token and links whatever social profile that code belongs to onto the session that made the request.

There's no `state` parameter anywhere in this flow. `state` is supposed to be a value the client generates and binds to the user's session before redirecting to the OAuth server, then checks matches on the way back; that's what proves the request on return actually belongs to the browser that initiated it. Without it, `/oauth-linking?code=...` is just a bare, replayable URL. Nothing ties this code to our session over anyone else's. Whichever account's browser requests `/oauth-linking?code=...` with a still-valid code is the account it gets linked to.

That means we can get a code issued for our social profile, then trick the admin's browser into making this exact request — linking our `peter.wiener` identity to the admin's blog account instead of ours.

Steps:

1. Repeat the "Attach a social profile" flow, with Burp set to intercept. Go through the login at the identity provider again with `peter.wiener:hotdog`.

2. Catch the `GET /oauth-linking?code=...` request and drop it before forwarding. We don't want to consume the code ourselves, just capture the URL:
   ```
   https://0aXXXXXX.web-security-academy.net/oauth-linking?code=9TgCqUYsSNkEnWTwbEXL2bJVa05pGh6SLnkbOg8HLH9
   ```
   The code stays valid since it was never submitted.

3. Log out of the blog (so we're acting as an outside attacker, not still authenticated as `wiener`).

4. Go to the exploit server (`Go to exploit server` from the lab banner) and set the body to an iframe pointing at the captured URL:

   ```html
   <iframe src="https://0aXXXXXX.web-security-academy.net/oauth-linking?code=9TgCqUYsSNkEnWTwbEXL2bJVa05pGh6SLnkbOg8HLH9"></iframe>
   ```

5. Store it, then click "Deliver to victim." The lab's simulated admin visits the exploit server with an active, authenticated blog session. Their browser loads our iframe, which fires `GET /oauth-linking?code=...` using their session cookie, and since there's no `state` to check against, the app happily links our `peter.wiener` social profile to the admin's account.

6. Go to the blog's login page and choose "Log in with social media." Complete the OAuth flow with `peter.wiener:hotdog` as before, only now that identity is linked to the admin account, so we land in the admin's session.

7. Navigate to `/admin`. Confirm we're looking at the admin panel, then delete `carlos`:
   
   ```
   GET /admin/delete?username=carlos
   ```

8. The lab registers as solved once `carlos` is deleted.

Root cause: the OAuth client trusted the linking callback purely by session cookie, with no CSRF token (`state` or otherwise) binding the authorization code's origin request to the account it gets attached to. Any client-side request that can be forced cross-site and lacks a per-session, unpredictable, checked `state` value is forgeable this way.

### Python Solution

See `oauth_03.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/OAuth_Authentication/OAuth_03_forced_oauth_profile_linking]
└─$ python oauth_03.py https://0a24006a0380cce1804803f100390001.web-security-academy.net/
[+] Found exploit server: https://exploit-0a14004a0334cce38019022a01d8005a.exploit-server.net
[+] Logged in as wiener
[+] Captured unused linking URL: https://0a24006a0380cce1804803f100390001.web-security-academy.net/oauth-linking?code=ueBWMKjZzRpKriGvVX52OPRSiat_ZzwwL_c7MLBckC8
[+] Stored exploit
[+] Delivered exploit to victim (admin)
[+] Logged out as wiener
[+] Logged in as administrator via linked social profile
[+] Deleted carlos
[+] Lab solved!
```