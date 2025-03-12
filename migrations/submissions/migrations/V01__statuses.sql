CREATE TABLE statuses (
    processing_status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    processing_status_description TEXT NOT NULL,
    load_date DATETIME DEFAULT (CURRENT_TIMESTAMP)
);