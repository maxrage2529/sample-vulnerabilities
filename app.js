const express = require("express");
const mysql = require("mysql");
const fs = require("fs");
const { exec } = require("child_process");

const app = express();
app.use(express.urlencoded({ extended: true }));

// **1. Command Injection Vulnerability**
app.get("/run", (req, res) => {
    let cmd = req.query.cmd; // User-controlled input
    exec(cmd, (error, stdout, stderr) => {  // Vulnerable to command injection
        if (error) res.send(`Error: ${error.message}`);
        else res.send(stdout);
    });
});

// **2. SQL Injection Vulnerability**
const db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "password123", // Hardcoded Credentials
    database: "test_db"
});

app.get("/user", (req, res) => {
    let userId = req.query.id; // Taking user input directly
    let query = `SELECT * FROM users WHERE id = ${userId}`; // Vulnerable to SQL Injection
    db.query(query, (err, results) => {
        if (err) res.send("Database error");
        else res.json(results);
    });
});

// **3. Hardcoded Credentials**
const API_KEY = "secret-api-key-123"; // Sensitive information in code

app.get("/apikey", (req, res) => {
    res.send(`Your API key is: ${API_KEY}`); // Exposing sensitive data
});

// **4. Insecure File Handling (Path Traversal)**
app.get("/read-file", (req, res) => {
    let filename = req.query.file; // User-controlled input
    fs.readFile(filename, "utf8", (err, data) => { // Possible Path Traversal vulnerability
        if (err) res.send("Error reading file");
        else res.send(data);
    });
});

// **5. Weak Cryptographic Randomness**
app.get("/generate-token", (req, res) => {
    let token = Math.floor(Math.random() * 1000000); // Not cryptographically secure
    res.send(`Your token is: ${token}`);
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});
