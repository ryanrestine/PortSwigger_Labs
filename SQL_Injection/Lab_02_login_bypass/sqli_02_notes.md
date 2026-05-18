# Lab: SQL injection vulnerability allowing login bypass

### Instructions

This lab contains a SQL injection vulnerability in the login function.

To solve the lab, perform a SQL injection attack that logs in to the application as the administrator user. 

### Solution

From the readings we know that when a user authenticates to the login form, this query is being run:

```sql
SELECT * FROM users WHERE username = 'test' AND password = 'password'
```

This logic can be abused in vulnerable login forms to bypass the check in the SQL query, allowing a user to authenticate simply using a username. 

This is done by simply commenting out the rest of the query after the username using: `'--`

To solve the lab the username of `administrator'--` can be used, and any value can be used for the password field, since it is ignored after the comment.

This successfully authenticates us as the administrator user. 