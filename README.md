# CodeAlpha_SecureCodingReview
# Secure Coding Review — CodeAlpha Internship Task 3

## Description
A security audit of a Python login application identifying
5 critical vulnerabilities using Bandit static analyzer
and manual code review, with a fully fixed secure version.

## Files
- vulnerable.py — original app with 5 security flaws
- secure.py     — fixed version with all issues resolved
- report.md     — full vulnerability report with remediation
- bandit_report.txt — Bandit scanner output

## Vulnerabilities Found
1. Hardcoded credentials (HIGH)
2. SQL Injection (HIGH)
3. Weak MD5 password hashing (MEDIUM)
4. Command Injection (HIGH)
5. Insecure deserialization with pickle (HIGH)

## Tools Used
- Python 3, Bandit, bcrypt
