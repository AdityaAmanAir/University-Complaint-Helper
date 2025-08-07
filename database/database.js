const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcryptjs');
const path = require('path');

const dbPath = path.join(__dirname, 'users.db');
const db = new sqlite3.Database(dbPath);

// Create users table
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      email TEXT UNIQUE,
      full_name TEXT,
      role TEXT DEFAULT 'user',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Insert admin user if not exists
  const adminPassword = bcrypt.hashSync('admin123', 10);
  db.get(`SELECT id FROM users WHERE username = 'admin'`, (err, row) => {
    if (!row) {
      db.run(
        `INSERT INTO users (username, password, email, full_name, role) 
         VALUES (?, ?, ?, ?, ?)`,
        ['admin', adminPassword, 'admin@example.com', 'Admin User', 'admin']
      );
    }
  });
});

module.exports = db;