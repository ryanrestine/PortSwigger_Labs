# Lab: SQL injection UNION attack, finding a column containing text

### Instructions

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you first need to determine the number of columns returned by the query. You can do this using a technique you learned in a previous lab. The next step is to identify a column that is compatible with string data.

The lab will provide a random value that you need to make appear within the query results. To solve the lab, perform a SQL injection UNION attack that returns an additional row containing the value provided. This technique helps you determine which columns are compatible with string data. 

### Solution

Repeating the steps from lab 03 to determine the amount of columns, we can incrementally manually add `NULL` values to the category parameter until the app stops returning an error or the response renders normally:

```
https://0aca00fd03ddaf7281bc253a00ba00f3.web-security-academy.net/filter?category=Gifts%27union%20select%20null,null,null--
```

This lets us know that there are three columns. 

Next, we can begin testing these columns for string data by inserting a test string.

The application gives us the instructions:

`Make the database retrieve the string: '4TvVOT'`

```
/filter?category=Gifts'union select '4TvVOT',null,null--
```

throws an error, but trying the next column:

```
/filter?category=Gifts'union select null,'4TvVOT',null--
```

successfully returns the value, letting us know the second column is string compatible, which solves the lab. 
