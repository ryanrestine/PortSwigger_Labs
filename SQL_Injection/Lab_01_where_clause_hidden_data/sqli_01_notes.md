# Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

### Instructions
This lab contains a SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following: 

```sql
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```

To solve the lab, perform a SQL injection attack that causes the application to display one or more unreleased products. 

### Solution

Sorting products by type and selecting `Gifts`, we are forwarded to the URL: 

```
https://0af500c4036be08a81788499008c00cc.web-security-academy.net/filter?category=Gifts
```

Based on the instructions we know this runs a SQL query which selects all products in the 'Gifts' category, and also filters out un-released products using `AND released = 1`.

This query returns three released items in the 'Gifts' category.

The filter can be bypassed by injecting a condition that always evaluates to true, such as `1=1`, and commenting out the rest of the query using `--`. The payload `' OR 1=1--` closes the original string and forces the `WHERE` clause to evaluate to true, returning all rows and bypassing the released filter.

Now, capturing the request in Burp and updating the syntax we have:

```
GET /filter?category=Gifts' OR 1=1--
```
Which returns all products, regardless of category or release status.