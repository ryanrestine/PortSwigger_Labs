# Lab: Username enumeration via subtly different responses

### Instructions

This lab is subtly vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:

- Candidate usernames - https://portswigger.net/web-security/authentication/auth-lab-usernames
- Candidate passwords - https://portswigger.net/web-security/authentication/auth-lab-passwords

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page. 

### Solution

Clicking on `/login` we can enter a random string for the username testing and any character for the password and we get the message: "Invalid username or password."

Let's capture this request in Burp and send it to Intruder for testing.

Once the request is in Intruder, we can paste in the provided usernames list in a Sniper attack, input any password we'd like, and then before launching the attack we can go to Settings > Grep - Match, and add the string "Invalid username or password." (The period inside the string is important here)

This will flag every username that contains that exact string in the HTML response.

We can then kick of the Intruder scan of usernames, and only one username contains a different response than: "Invalid username or password." - `announcements`

```
65	announcements	200	329	false	false	3447	0	
0		200	339	false	false	3464	1	
1	carlos	200	189	false	false	3444	1	
2	root	200	328	false	false	3443	1	
3	admin	200	328	false	false	3444	1	
```

This response is missing the `.`:

```html
<p class=is-warning>Invalid username or password </p>
```

Now that we have a potential working username we can update the request to:

`username=announcements&password=testing`

We can then send the request to Intruder, and again using a Sniper attack, paste in our password list in the payload position and bruteforce this user's password.

One response contains a 302 redirect code rather than the 200 all other passwords returned:

```
31	qazwsx	302	325	false	false	195	
```

This indicates the password is valid.

We can now login at `/login` with `announcements:qazwsx` to finish the lab.
