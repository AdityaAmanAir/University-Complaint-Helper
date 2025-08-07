const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcryptjs');
const db = require('./database/database');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static('public'));

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// User registration
app.post('/register', async (req, res) => {
  try {
    const { username, password, email, full_name } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    
    db.run(
      `INSERT INTO users (username, password, email, full_name) 
       VALUES (?, ?, ?, ?)`,
      [username, hashedPassword, email, full_name],
      function(err) {
        if (err) {
          return res.status(400).json({ error: err.message });
        }
        res.json({ success: true, userId: this.lastID });
      }
    );
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// User login
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  
  db.get(
    `SELECT * FROM users WHERE username = ?`, 
    [username],
    async (err, user) => {
      if (err || !user) {
        return res.status(401).json({ error: 'Invalid username or password' });
      }
      
      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch) {
        return res.status(401).json({ error: 'Invalid username or password' });
      }
      
      // Successful login - in a real app, you'd create a session or JWT here
      res.json({ 
        success: true, 
        user: {
          id: user.id,
          username: user.username,
          full_name: user.full_name,
          role: user.role
        }
      });
    }
  );
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});