-- 收支紀錄表
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    note TEXT,
    date TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
