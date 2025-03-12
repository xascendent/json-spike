CREATE TABLE submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    upload_start_time DATETIME NOT NULL,
    upload_end_time DATETIME NULL,
    file_path TEXT NOT NULL,
    processing_status_id INTEGER,
    load_date DATETIME DEFAULT (CURRENT_TIMESTAMP),
    CONSTRAINT fk_processing_status
        FOREIGN KEY (processing_status_id) 
        REFERENCES statuses(processing_status_id)
);
