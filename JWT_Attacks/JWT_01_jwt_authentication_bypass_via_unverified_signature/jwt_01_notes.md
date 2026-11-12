# Lab: JWT authentication bypass via unverified signature

### Instructions

This lab uses a JWT-based mechanism for handling sessions. Due to implementation flaws, the server doesn't verify the signature of any JWTs that it receives.

To solve the lab, modify your session token to gain access to the admin panel at `/admin`, then delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

We can login with the provided credentials and observe a JWT is assigned:

```
eyJraWQiOiIzZTJlYTY2My04NTlmLTRkNTEtYjI4NC1jZWNlMjQwYjM4YTkiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5NDUyNTU3MSwic3ViIjoid2llbmVyIn0.mmhmFi13v-EzN2LOkb3DdRNToyZxRH-gMJOTo7xukMWVdAP_04lN2G3Azo4BVWQpCmTIG4WQFl7keGhjdAzpU3tf8HXgBbtbCzNgUM0gkaWFgHDvfW4bUMg903IfwDIyUxM_WwZzkMLK1DhYJlaGA_EChZceeDESYL9nG_5qRUJt56ST189bkStkVqxkuYUCHjd0BWu3HqZJi7ijwWBIyt_Dntowu1zn89ACa3zhPGLEcfMfFS5MSiLi7CBpz7hPFdQTHLtOXJ0eZZho8B_u6to7S9N0h-EN2zmDs4TyPI7lMYEPYf1zYx8-NYGPPRX1o0xlNrM9J0CRO7vRssa9zg
```

Decoding this in Burp using the JWT Editor plugin or in a site like jwt.io, we see the following header:

```json
{
  "kid": "3e2ea663-859f-4d51-b284-cece240b38a9",
  "alg": "RS256"
}
```

And the payload:

```json
{
  "iss": "portswigger",
  "exp": 1794525571,
  "sub": "wiener"
}
```

We can edit the JWT to set `alg` to `none` (removing the signature) and setting the user (`sub`) to administrator.

The `alg` field tells the server’s JWT library how to verify the signature. If the backend doesn’t explicitly block `none` as an accepted algorithm, setting `alg` to `none` tells the verifier to skip signature validation entirely, meaning we can forge any claims we want without knowing the signing key.

Once these changes are made the newly forged JWT can be sent via Burp or the cookie editor (make sure to include that final trailing `.`), the page refreshed, and we now have admin access.

The user carlos can be deleted which solves the lab.


### Python Solution

See `jwt_01.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/JWT_Attacks/JWT_01_jwt_authentication_bypass_via_unverified_signature]
└─$ python jwt_01.py https://0a1e00a4047e514b81fc7a12004100d7.web-security-academy.net/
[+] Logged in as wiener
[+] Forged session cookie with alg=none, sub=administrator
[+] Deleted carlos
[+] Lab solved!
```