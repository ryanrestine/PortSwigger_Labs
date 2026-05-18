# Lab: SQL injection UNION attack, determining the number of columns returned by the query

### Instructions

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. The first step of such an attack is to determine the number of columns that are being returned by the query. You will then use this technique in subsequent labs to construct the full attack.

To solve the lab, determine the number of columns returned by the query by performing a SQL injection UNION attack that returns an additional row containing null values. 

### Solution
Clicking through the site, we can access item inventory and filter products by category.

The application uses the `category` parameter in a database query:

https://0aee007104346a5d80050885002500a8.web-security-academy.net/filter?category=

We can test for SQL injection by submitting a single quote `'`, which causes the application to return a server error.

To determine the number of columns returned by the query, we increment the number of NULL values in a UNION SELECT statement until the request succeeds:

```sql
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
```
The payload:

```sql
' UNION SELECT NULL,NULL,NULL--
```
returns a successful response without a SQL error, indicating that the original query returns 3 columns.