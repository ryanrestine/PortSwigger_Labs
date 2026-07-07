# Lab: Authentication bypass via encryption oracle

### Instructions

This lab contains a logic flaw that exposes an encryption oracle to users. To solve the lab, exploit this flaw to gain access to the admin panel and delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

Logging in as wiener with "Stay logged in" checked we get a `stay-logged-in` cookie. Browsing to a blog post and submitting a comment with an invalid email address we notice two things: the error message reflects our input back in cleartext in the page header, and the response sets an encrypted `notification` cookie.

This gives us two endpoints we can abuse as an encryption oracle:

- The comment POST encrypts whatever we put in the email field and returns the ciphertext as the notification cookie
- The blog GET decrypts whatever we put in the notification cookie and reflects the plaintext in the page

Send the `POST /post/comment` to Repeater and label it encrypt. Send the `GET /post?postId=1` to Repeater and label it decrypt.

**Decrypt the stay-logged-in cookie**

In the decrypt tab, swap the notification cookie value for our `stay-logged-in` cookie value and send it. The page reflects the decrypted content:

```
wiener:1671605400893
```

So the format is `username:timestamp`. Copy the timestamp.

**Encrypt a forged admin cookie**

In the encrypt tab, set the email to:

```
administrator:your-timestamp
```

Send it and copy the notification cookie from the response. If we try to use this directly we have a problem, the server prepends `Invalid email address: ` to everything we encrypt through the email parameter, which is 23 characters. We need to strip those 23 bytes from the ciphertext.

**The block size problem**

The encryption uses a block cipher with 16-byte blocks, so we can only drop bytes in multiples of 16. We can't drop exactly 23 bytes cleanly. The fix is to pad our input so the prefix fills exactly 2 complete blocks (32 bytes):

```
32 - 23 = 9 padding characters needed
```

Go back to the encrypt tab and change the email to:

```
AAAAAAAAAadministrator:your-timestamp
```

That's 9 A's. Send it and copy the new notification cookie.

**Strip the prefix bytes**

Take the notification cookie to Decoder. URL-decode it, then Base64-decode it. Switch to the Hex tab, select the first 32 bytes, right click and delete them. Now Base64-encode and then URL-encode the result.

Paste this back into the decrypt tab as the notification cookie and send it. The response should now show:

```
administrator:your-timestamp
```

No prefix. The ciphertext is clean.

**Log in as administrator**

Take that final encoded notification cookie value and use it as the `stay-logged-in` cookie on a GET to `/`. Delete the `session` cookie entirely first, the server falls back to `stay-logged-in` for authentication when no session cookie is present. The page loads with admin access. Browse to `/admin/delete?username=carlos` and the lab is solved.

### Python Solution

See `logic_vuln_11.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Business_Logic_Vulnerabilities/Logic_Vuln_11_authentication_bypass_via_encryption_oracle]
└─$ python logic_vuln_11.py https://0a7d005504cb49aa80eb35e000e800f0.web-security-academy.net/
[+] Logged in as wiener
[+] stay-logged-in cookie: 0eck2O9DuwzEfULjw96ZS3N37smQynOrcPaUf5B8tYo%3d
[+] Decrypted stay-logged-in: wiener:1783455625278
[+] Timestamp: 1783455625278
[+] Encrypting: xxxxxxxxxadministrator:1783455625278
[+] Encrypted cookie: r4Mrse7bRY17jJR5G2mY0exICy4zoic%2fnsBiFLXwhzbtdEPppClf4ViwWInaJDbcKP4Rh2dZ%2fMKFqXcSRd6UrA%3d%3d
[+] Forged cookie: 7XRD6aQpX%2BFYsFiJ2iQ23Cj%2BEYdnWfzChal3EkXelKw%3D
[+] Verified decryption: administrator:1783455625278
[*] Logging in as administrator...
[+] Logged in as administrator
[+] Carlos deleted - Lab solved!
```