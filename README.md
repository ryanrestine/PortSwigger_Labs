# PortSwigger_Labs

## Solutions and Python automation for PortSwigger training labs

### Goals

After OSCP and CPTS, and generally nerding out on AD pentesting for a long while, I wanted to sharpen my web-app skills and to get faster (and stronger) at Python exploit automation. PortSwigger labs allow me to do both at the same time. The labs are also very stable, come with training, explanations, and walkthroughs, plus they're free, which is a nice perk as well.

Each lab gets two things: a manual exploitation walkthrough and a Python script built to automate the attack end to end, designed to be readable and reusable as reference for real engagements.

I'm not exactly positive how long this project will take. It's a lot of material to work through (as of now there are 235 "Apprentice" and "Practitioner" labs, and  39 "Expert" labs), but I'm enjoying the process so far and believe it is helping me with my goals.

Best case scenario is I keep learning new techniques, sharpen my scripting skills, and maybe help some stranger out there get un-stuck in a lab or with their Python script. Here's to hoping!

### Organization

At the vulnerability class/ type level, I'm following  the order of topics PortSwigger recommends at: https://portswigger.net/web-security/all-topics

As for the lab order specifically, I follow: https://portswigger.net/web-security/all-labs and work my way through each lab for each topic. Currently I'm skipping the "expert" level labs (I plan on circling back to these later) as well as all out-of-band techniques that require Burp Pro. As of now I'm just a lowly Burp Community user, but plan on upgrading to Pro soon.

### Current Progress

Server-Side:

1. SQL Injection 
2. Authentication 
3. Path Traversal
4. Command Injection
5. Business Logic Vulnerabilities
6. Information Disclosure
7. Access Control (in progress)


### Resources

When stuck (which certainly happens...) my two favorite resources to get ideas, inspiration, and at times outright solutions are:

- https://github.com/rkhal101/Web-Security-Academy-Series/tree/main 

and:

- https://github.com/frank-leitner/portswigger-websecurity-academy/tree/main

These repos are goldmines of techniques, both in manual and scripting for pentesters. 
