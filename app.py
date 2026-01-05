from flask import Flask, render_template, request, jsonify
import base64
from cryptography.fernet import Fernet

app = Flask(__name__)

# ---------- Crypto Logic (UNCHANGED) ----------
def caesar_encrypt(text, shift):
    result = ""
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result += chr((ord(c) - base + shift) % 26 + base)
        else:
            result += c
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def generate_key(password):
    return base64.urlsafe_b64encode(password.ljust(32).encode()[:32])

def aes_encrypt(text, password):
    return Fernet(generate_key(password)).encrypt(text.encode()).decode()

def aes_decrypt(text, password):
    return Fernet(generate_key(password)).decrypt(text.encode()).decode()

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")   # Homepage

@app.route("/tool")
def tool():
    return render_template("tool.html")    # Tool page

@app.route("/process", methods=["POST"])
def process():
    d = request.json
    t, k, a = d["text"], d.get("key",""), d["algorithm"]

    try:
        if a == "caesar_encrypt":
            r = caesar_encrypt(t, int(k))
        elif a == "caesar_decrypt":
            r = caesar_decrypt(t, int(k))
        elif a == "base64_encrypt":
            r = base64.b64encode(t.encode()).decode()
        elif a == "base64_decrypt":
            r = base64.b64decode(t).decode()
        elif a == "aes_encrypt":
            r = aes_encrypt(t, k)
        elif a == "aes_decrypt":
            r = aes_decrypt(t, k)
        else:
            r = "Invalid algorithm"
    except:
        r = "Error: Invalid input/key"

    return jsonify({"result": r})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

