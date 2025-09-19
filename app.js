const express = require("express");
const bodyParser = require("body-parser");
const bcrypt = require("bcryptjs");
const session = require("express-session");
const db = require("./database/database");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static("public"));

// Session middleware
app.use(
  session({
    secret: "your-secret-key", // Replace with a strong secret
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false }, // Set to true for HTTPS
  })
);

// Helper function for timestamp
function getTimestamp() {
  return new Date().toISOString();
}

// Serve index.html (login/register page)
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Protected: Serve VTOP4.html (dashboard)
app.get("/VTOP4.html", (req, res) => {
  if (!req.session.user) {
    return res.redirect("/");
  }
  res.sendFile(path.join(__dirname, "public", "VTOP4.html"));
});

// Protected: Serve VITChat.html (chat page)
app.get("/VITChat.html", (req, res) => {
  if (!req.session.user) {
    return res.redirect("/");
  }
  res.sendFile(path.join(__dirname, "public", "VITChat.html"));
});

// User registration
app.post("/register", async (req, res) => {
  try {
    const { username, password, email, full_name } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);

    db.run(
      `INSERT INTO users (username, password, email, full_name) 
       VALUES (?, ?, ?, ?)`,
      [username, hashedPassword, email, full_name],
      function (err) {
        if (err) {
          return res.status(400).json({ success: false, message: err.message });
        }
        res.json({ success: true, userId: this.lastID });
      }
    );
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

// User login
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  db.get(
    `SELECT * FROM users WHERE username = ?`,
    [username],
    async (err, user) => {
      if (err || !user) {
        return res
          .status(401)
          .json({ success: false, message: "Invalid username or password" });
      }

      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch) {
        return res
          .status(401)
          .json({ success: false, message: "Invalid username or password" });
      }

      // Store user in session
      req.session.user = {
        id: user.id,
        username: user.username,
        full_name: user.full_name,
        role: user.role,
      };

      res.json({
        success: true,
        user: req.session.user,
        redirect: "/VTOP4.html", // Redirect to dashboard after login
      });
    }
  );
});

// Message logging (from server.js)
app.post("/log", (req, res) => {
  const { message, username } = req.body;

  if (!message || !username || !req.session.user) {
    return res
      .status(400)
      .json({ success: false, message: "Message and valid session required" });
  }

  const timestamp = getTimestamp();
  const logEntry = `[${timestamp}] User: ${username} - Message: ${message}\n`;

  fs.appendFile("messages01.log", logEntry, (err) => {
    if (err) {
      console.error("Failed to write to log file:", err);
      return res
        .status(500)
        .json({ success: false, message: "Failed to log message" });
    }

    console.log("Message logged:", logEntry.trim());
    res.json({ success: true, message: "Message logged successfully" });
  });
});

// Logout
app.post("/logout", (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res
        .status(500)
        .json({ success: false, message: "Failed to logout" });
    }
    res.json({
      success: true,
      message: "Logged out successfully",
      redirect: "/",
    });
  });
});

// Check session (for client-side validation)
app.get("/check-session", (req, res) => {
  res.json({
    isAuthenticated: !!req.session.user,
    user: req.session.user || null,
  });
});

app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log("Messages will be saved to messages.log file");
});

// const express = require('express');
const { spawn } = require("child_process");
//const app = express();

// for server -> html
app.post("/log", (req, res) => {
  const { message, username } = req.body;

  if (!message || !username || !req.session.user) {
    return res
      .status(400)
      .json({
        success: false,
        message: "Message, username, and valid session required",
      });
  }

  const pythonProcess = spawn("python", ["processor.py"]);

  let output = "";
  let errorOutput = "";

  pythonProcess.stdout.on("data", (data) => {
    output += data.toString();
  });

  pythonProcess.stderr.on("data", (data) => {
    errorOutput += data.toString();
  });

  pythonProcess.on("close", (code) => {
    if (code !== 0) {
      console.error(`Python error: ${errorOutput}`);
      return res.json({ success: false, message: "Error processing message" });
    }

    try {
      const result = JSON.parse(output);
      res.json(result); // Send Python output to client
    } catch (err) {
      res.json({ success: false, message: "Error parsing Python output" });
    }
  });

  // Send JSON input to Python
  pythonProcess.stdin.write(JSON.stringify({ message, username }));
  pythonProcess.stdin.end();

  // Log original message to messages.log (optional, if still needed)
  const timestamp = getTimestamp();
  const logEntry = `[${timestamp}] User: ${username} - Message: ${message}\n`;
  fs.appendFile("messages.log", logEntry, (err) => {
    if (err) console.error("Failed to write to log file:", err);
  });
});

app.get("/get-processed-messages", (req, res) => {
  if (!req.session.user) {
    return res.status(401).json({ success: false, message: "Unauthorized" });
  }
  try {
    const messages = [];
    if (fs.existsSync("messages2.log")) {
      const data = fs.readFileSync("messages2.log", "utf8");
      const lines = data.split("\n").filter((line) => line.trim());
      for (const line of lines) {
        const match = line.match(/\[.*?\] Processing message: (.*)/);
        if (match) {
          messages.push(match[1]);
        }
      }
      console.log("Read from messages2.log:", messages); // Debug log
    } else {
      console.log("messages2.log does not exist");
    }
    res.json({ success: true, messages });
  } catch (err) {
    console.error("Error reading messages2.log:", err);
    res.json({
      success: false,
      messages: [],
      message: "Error reading messages",
    });
  }
});

app.post("/clear-processed-messages", (req, res) => {
  if (!req.session.user) {
    return res.status(401).json({ success: false, message: "Unauthorized" });
  }
  try {
    fs.writeFileSync("messages2.log", "");
    console.log("Cleared messages2.log"); // Debug log
    res.json({ success: true });
  } catch (err) {
    console.error("Error clearing messages2.log:", err);
    res.json({ success: false, message: "Error clearing messages" });
  }
});
