# Lab: Blind SQL injection with conditional responses

### Instructions

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and no error messages are displayed. But the application includes a Welcome back message in the page if the query returns any rows.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user. 

### Solution

#### Concepts Covered

- Blind SQL injection (no data returned directly)
- Boolean oracle — inferring data from conditional page responses
- Character-by-character password extraction via SUBSTRING + ASCII
- Cookie-based injection point

---

#### Vulnerability

The TrackingId cookie value is inserted unsanitised into a SQL query. The
application executes the query and renders "Welcome back!" only when the query
returns a row — creating a boolean oracle.

Likely backend query:
```sql
SELECT * FROM tracking WHERE id = ''
```

Injecting a condition appends a boolean expression:
```sql
SELECT * FROM tracking WHERE id = 'xyz' AND (SELECT ASCII(SUBSTRING(password,1,1)) FROM users WHERE username='administrator')='97'--'
```

If the condition is true → Welcome back! appears  
If the condition is false → Welcome back! absent

---

#### Exploitation Approach

##### Step 1 — Confirm injection point

Append `' AND '1'='1` and `' AND '1'='2` to the TrackingId cookie.
- True condition → Welcome back! present
- False condition → Welcome back! absent
This confirms boolean control over the query.

##### Step 2 — Detect password length

Iterate `(SELECT LENGTH(password) FROM users WHERE username='administrator')=N`
for N=1..50 until oracle fires. Password length: **20**

##### Step 3 — Extract password

For each position 1–20, iterate ASCII values 32–126 testing:
`(SELECT ASCII(SUBSTRING(password,N,1)) FROM users WHERE username='administrator')=J`
Record the character when oracle fires. Repeat for all 20 positions.

---

#### Payload

```sql
' AND (SELECT ASCII(SUBSTRING(password,1,1)) FROM users WHERE username='administrator')='97'--
```

#### Automation

Solved via Python script — see `sqli_09.py`

Manual exploitation of this variant is impractical due to the volume of
requests required (up to 20 positions × 94 possible chars = 1,880 requests
worst case). This lab is intentionally designed to motivate automation.

```
python3 sqli_09.py <LAB_URL>
python3 sqli_09.py <LAB_URL> http://127.0.0.1:8080  # with Burp proxy
```


---

#### Takeaways

- The oracle doesn't have to be an error — any binary difference in response
  works (text present/absent, status code, response time)
- ASCII + SUBSTRING is the core primitive for blind data extraction
- Dynamic length detection before brute forcing avoids hardcoded assumptions
- Blind SQLi is inherently slow — threading or binary search would speed it up
  significantly (improvement to implement later)

---