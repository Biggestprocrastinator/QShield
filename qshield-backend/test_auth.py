import urllib.request
import urllib.parse
import json
import time
import urllib.error

time.sleep(2)

def post_json(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    return urllib.request.urlopen(req)

def post_form(url, data):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode('utf-8'), headers={'Content-Type': 'application/x-www-form-urlencoded'})
    return urllib.request.urlopen(req)

try:
    print("1. SQLi Proof Check - Signup with normal email, password with SQLi payload")
    res = post_json("http://127.0.0.1:8000/auth/register", {"email": "sqli@test.com", "password": "' OR 1=1 --"})
    print("Signup Response:", res.status, res.read().decode())
except urllib.error.HTTPError as e:
    print("Signup Error Response:", e.code, e.read().decode())

try:
    print("\n2. Normal Login Check")
    res = post_form("http://127.0.0.1:8000/auth/login", {"username": "sqli@test.com", "password": "' OR 1=1 --"})
    print("Login Response:", res.status, res.read().decode())
except urllib.error.HTTPError as e:
    print("Login Error Response:", e.code, e.read().decode())

try:
    print("\n3. Failed Login Check (Incorrect Password)")
    post_form("http://127.0.0.1:8000/auth/login", {"username": "sqli@test.com", "password": "wrong"})
except urllib.error.HTTPError as e:
    print("Failed Login Response:", e.code, e.read().decode())

try:
    print("\n4. Failed Login Check (SQLi Payload as password doesn't bypass auth)")
    post_form("http://127.0.0.1:8000/auth/login", {"username": "admin@nonexistent.com", "password": "' OR '1'='1"})
except urllib.error.HTTPError as e:
    print("SQLi Login Payload Attempt:", e.code, e.read().decode())
