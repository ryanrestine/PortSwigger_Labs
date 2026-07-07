# Lab: Information disclosure in error messages

### Instructions

This lab's verbose error messages reveal that it is using a vulnerable version of a third-party framework. To solve the lab, obtain and submit the version number of this framework. 

### Solution

Clicking on an item in the shop, we find the following:

```
https://0a87003704823b28824f617f008000c0.web-security-academy.net/product?productId=1
```

Appending a sing quote character to this: `'` throws a verbose error, which reveals the third-party framework the app is using:

```
https://0a87003704823b28824f617f008000c0.web-security-academy.net/product?productId=1'
```

```
Internal Server Error: java.lang.NumberFormatException: For input string: "1'"
	at java.base/java.lang.NumberFormatException.forInputString(NumberFormatException.java:67)
	at java.base/java.lang.Integer.parseInt(Integer.java:661)
	at java.base/java.lang.Integer.parseInt(Integer.java:777)
	at lab.a.mm.v.o.h(Unknown Source)
	at lab.s.gn.l.n.K(Unknown Source)
	at lab.s.gn.v.x.y.c(Unknown Source)
	at lab.s.gn.v.d.lambda$handleSubRequest$0(Unknown Source)
	at m.d.t.h.lambda$null$3(Unknown Source)
	at m.d.t.h.P(Unknown Source)
	at m.d.t.h.lambda$uncheckedFunction$4(Unknown Source)
	at java.base/java.util.Optional.map(Optional.java:260)
	at lab.s.gn.v.d.q(Unknown Source)
	at lab.server.s.a.t.b(Unknown Source)
	at lab.s.gn.f.z(Unknown Source)
	at lab.s.gn.f.b(Unknown Source)
	at lab.server.s.a.a.w.L(Unknown Source)
	at lab.server.s.a.a.e.lambda$handle$0(Unknown Source)
	at lab.a.w.d.p.u(Unknown Source)
	at lab.server.s.a.a.e.u(Unknown Source)
	at lab.server.s.a.c.R(Unknown Source)
	at m.d.t.h.lambda$null$3(Unknown Source)
	at m.d.t.h.P(Unknown Source)
	at m.d.t.h.lambda$uncheckedFunction$4(Unknown Source)
	at lab.server.m_.z(Unknown Source)
	at lab.server.s.a.c.N(Unknown Source)
	at lab.server.s.g.x.C(Unknown Source)
	at lab.server.s.o.L(Unknown Source)
	at lab.server.s.x.L(Unknown Source)
	at lab.server.ma.C(Unknown Source)
	at lab.server.ma.u(Unknown Source)
	at lab.d.i.lambda$consume$0(Unknown Source)
	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1144)
	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:642)
	at java.base/java.lang.Thread.run(Thread.java:1583)

Apache Struts 2 2.3.31
```

We can click on the "Submit solution" button and provide `Apache Struts 2 2.3.31` which solves the lab.

### Python Solution

See `info_disclosure_01.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Information_Disclosure/Info_Disclosure_01_info_disclosure_in_error_messages]
└─$ python info_disclosure_01.py https://0a520046045fea25833e3cdc00060032.web-security-academy.net/ 
[*] Using single quote character to throw error in product page...
Apache Struts 2 2.3.31
[*] Submitting answer...
[+] Lab solved
```