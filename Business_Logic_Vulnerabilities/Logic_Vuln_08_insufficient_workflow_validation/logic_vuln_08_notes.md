# Lab: Insufficient workflow validation

### Instructions

This lab makes flawed assumptions about the sequence of events in the purchasing workflow. To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: `wiener:peter`

### Solution

Logging in as wiener we buy a cheap item we can afford with our $100 store credit and capture the checkout flow in Burp. We notice that after the POST to `/cart/checkout` we get redirected to:

```
GET /cart/order-confirmation?order-confirmed=true
```

This confirmation request is what actually completes the order. The server isn't validating whether the checkout POST was legitimate before honouring the confirmation, it just processes whatever lands on that endpoint.

So we add the leather jacket to our cart, then skip the checkout POST entirely and just send the confirmation request directly:

```
GET /cart/order-confirmation?order-confirmed=true
```

The order goes through, the jacket is ours, and the cost is never deducted from our store credit. This marks the lab as solved.

### Python Solution

See `logic_vuln_08.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Business_Logic_Vulnerabilities/Logic_Vuln_08_insufficient_workflow_validation]
└─$ python logic_vuln_08.py https://0ace009104049708805eb2ae00b20053.web-security-academy.net/
[+] Logged in as wiener
[*] Adding product 1 to cart...
[+] Jacket added to cart
[*] Sending order confirmation...
[+] Order confirmed - Lab solved!
```