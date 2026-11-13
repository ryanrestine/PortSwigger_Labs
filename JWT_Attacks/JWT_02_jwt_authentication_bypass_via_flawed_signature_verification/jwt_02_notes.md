# Lab: JWT authentication bypass via flawed signature verification

### Instructions

This lab uses a JWT-based mechanism for handling sessions. The server is insecurely configured to accept unsigned JWTs.

To solve the lab, modify your session token to gain access to the admin panel at `/admin`, then delete the user carlos.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

We can login with the provided credentials and observe a JWT is assigned:

```
eyJraWQiOiI1NTQyZDAyYi0zODljLTQyY2MtOTQ1My1kMDM2ZjlmMTYwYjQiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5NDU5MDQ4OCwic3ViIjoid2llbmVyIn0.Ulx0mTX2RJYLYEAVR-x-1bMIDTal1h1LKoSZ4vjUdxeQv3pQDuB2xG-tYqI_tIposJ_6AUtD625N9Nid-pKjHTfeeFftX1-2X_YtxpNWWMBTenGo6LpgwVgbm_otlwvMJg_L0t_XzDG0_SSt8FYebadv_cwXJv8kchb9euq1ySn2uFp1sCJUYBTJXsegEQ6tn6oSj18tOcWNY31YTwRPLoQc_P5wbreJ6KTGsSc_vGC1p_3G4YiGvqWCwXT5ewvLA8fot-cqLlmQA7wR0oh_qaiG6pZZaN-Oo-_wSpLqW9iAzpV_V864Hz3vzgJA5--dZai7u18zVyGpZjv9U7qnRw
```

Decoding this in Burp using the JWT Editor plugin or in a site like jwt.io, we see the following header:

```json
{
  "kid": "5542d02b-389c-42cc-9453-d036f9f160b4",
  "alg": "RS256"
}
```

And the payload:

```json
{
  "iss": "portswigger",
  "exp": 1794590488,
  "sub": "wiener"
}
```

We can edit the JWT to set `alg` to `none` (removing the signature) and setting the user (`sub`) to administrator.

The `alg` field tells the server’s JWT library how to verify the signature. If the backend doesn’t explicitly block `none` as an accepted algorithm, setting `alg` to `none` tells the verifier to skip signature validation entirely, meaning we can forge any claims we want without knowing the signing key.

Once these changes are made the newly forged JWT can be sent via Burp or the cookie editor (make sure to include that final trailing `.`), the page refreshed, and we now have admin access.

The user carlos can be deleted which solves the lab.



### Python Solution

See `jwt_02.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/JWT_Attacks/JWT_02_jwt_authentication_bypass_via_flawed_signature_verification]
└─$ python jwt_02.py https://0a4e0089036177818099f8bc00c000c2.web-security-academy.net/
[+] Logged in as wiener
[+] Forged session cookie with alg=none, sub=administrator
[+] Deleted carlos
[+] Lab solved!
```