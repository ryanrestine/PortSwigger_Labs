# Lab: Infinite money logic flaw

### Instructions

This lab has a logic flaw in its purchasing workflow. To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: `wiener:peter` 

### Solution

Logging in as wiener we notice two things on the account page: we can redeem gift cards, and there is a newsletter signup. Signing up for the newsletter gives us the coupon code `SIGNUP30`.

Poking around the shop we find we can buy a $10 gift card. We add one to our cart, apply `SIGNUP30` at checkout and capture the flow in Burp:

```
POST /cart                                          (add gift card, productId=2)
POST /cart/coupon                                   (apply SIGNUP30, brings price to $7)
POST /cart/checkout                                 (place order)
GET  /cart/order-confirmation?order-confirmed=true  (contains the gift card code)
POST /gift-card                                     (redeem the gift card for $10 credit)
```

We just spent $7 and got $10 back, $3 profit per cycle. The jacket costs $1337 and we start with $100 so we need roughly 413 cycles. We automate this using a Burp macro.

**Setting up the macro**

In Burp, go to Settings > Sessions > Session handling rules and click Add. Under the Scope tab set URL scope to "Include all URLs". Back on the Details tab, click Add > Run a macro, then Add again to open the Macro Recorder. Select these five requests in order:

```
POST /cart
POST /cart/coupon
POST /cart/checkout
GET  /cart/order-confirmation?order-confirmed=true
POST /gift-card
```

Click OK to open the Macro Editor. The key problem here is that the gift card code is dynamically generated each cycle, so we need to extract it from the confirmation response and automatically feed it into the redemption request.

Select the `GET /cart/order-confirmation` request and click Configure item. Click Add to create a custom parameter, name it `gift-card`, and highlight the gift card code in the response at the bottom of the page. Click OK.

Now select the `POST /gift-card` request and click Configure item. In the Parameter handling section, set the `gift-card` parameter to be derived from the prior response. Click OK.

Click Test macro to verify it works, check that the gift card code in the confirmation response matches what gets sent in the `POST /gift-card` request, and that the redemption gets a 302 response.

**Running the attack**

Send any request for `GET /my-account` to Intruder. Set the payload type to Null payloads and generate 412 repeats. Under Resource pool, set maximum concurrent requests to 1. This is important because the requests need to fire sequentially, not in parallel, otherwise the macro will break. Start the attack.

Each iteration the macro fires the full five-request cycle, extracts the fresh gift card code and redeems it automatically. When it finishes we have enough credit to add the jacket to the cart and checkout normally.

### Python Solution

See `logic_vuln_10.py`.
```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Business_Logic_Vulnerabilities/Logic_Vuln_10_infinite_money_logic_flaw]
└─$ python logic_vuln_10.py https://0a7100bf041d3a7d80d9b79700800048.web-security-academy.net/
[+] Logged in as wiener
[*] Running cycles: 450/450
[*] Buying jacket...
[+] Jacket purchased - Lab solved!
```