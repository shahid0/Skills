-- Sample Database Schema for iOS Todo Application
-- Used for reference when inspecting local SQLite databases inside the simulator sandbox.

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Todo Items Table
CREATE TABLE IF NOT EXISTS todo_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    completed INTEGER DEFAULT 0, -- Boolean mapping: 0 = false, 1 = true
    due_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. App Settings Table (Key-Value Store alternative to UserDefaults)
CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    value_type TEXT DEFAULT 'string', -- string, integer, boolean, json
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indices for optimization and audit reference
CREATE INDEX IF NOT EXISTS idx_todo_items_user_id ON todo_items(user_id);
CREATE INDEX IF NOT EXISTS idx_todo_items_completed ON todo_items(completed);
