# Lab: Source code disclosure via backup files

### Instructions

This lab leaks its source code via backup files in a hidden directory. To solve the lab, identify and submit the database password, which is hard-coded in the leaked source code. 

### Solution

Launching the lab we can confirm there is a `/robots.txt` file at : `https://0ac5001004b8b33684aa1590007500f1.web-security-academy.net/robots.txt`

This contains an entry called `/backup`:

```
User-agent: *
Disallow: /backup
```

This directory contains a backup file: 

```
Index of /backup
Name	Size
ProductTemplate.java.bak	1647B
```

```
https://0ac5001004b8b33684aa1590007500f1.web-security-academy.net/backup/ProductTemplate.java.bak
```

This file contains a postgres credential:

```java
        ConnectionBuilder connectionBuilder = ConnectionBuilder.from(
                "org.postgresql.Driver",
                "postgresql",
                "localhost",
                5432,
                "postgres",
                "postgres",
                "aviqko623dmm2hu6c66voay6ha1jaa91"
        ).withAutoCommit();
```

We can submit this credential as our answer, which marks the lab as solved.

### Python Solution

See `info_disclosure_03.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Information_Disclosure/Info_Disclosure_03_source_code_disclosure_via_backup_files]
└─$ python info_disclosure_03.py https://0a5700cc03468f5e829048c3005c004c.web-security-academy.net/
[*] Fetching password from backup file...
[+] Password discovered in source code
[+] Password: 464yjijjvcfk1vx440jp8uw41o3j95j1
[*] Submitting answer...
[+] Lab solved
```