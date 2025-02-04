import os
import subprocess
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# **1. Command Injection Vulnerability**
@app.route("/run", methods=["GET"])
def run_command():
    cmd = request.args.get("cmd")  # Taking user input directly
    output = subprocess.check_output(cmd, shell=True)  # Vulnerable to command injection
    return output.decode("utf-8")


# **2. SQL Injection Vulnerability**
def get_user_data(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"  # Directly using user input (vulnerable)
    cursor.execute(query)  # SQL injection possible
    data = cursor.fetchall()
    conn.close()
    return data


# **3. Hardcoded Credentials**
DB_USERNAME = "admin"
DB_PASSWORD = "password123"  # Hardcoded password (bad practice)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == DB_USERNAME and password == DB_PASSWORD:
        return "Login successful"
    return "Invalid credentials"


# **4. Insecure File Handling**
@app.route("/read-file", methods=["GET"])
def read_file():
    filename = request.args.get("file")  # User-controlled input
    with open(filename, "r") as f:  # Possible Path Traversal vulnerability
        return f.read()


# **5. Using Insecure Random for Security**
import random

def generate_token():
    return str(random.randint(100000, 999999))  # Not cryptographically secure

if __name__ == "__main__":
    app.run(debug=True)
