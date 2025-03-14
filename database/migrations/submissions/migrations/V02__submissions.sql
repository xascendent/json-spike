CREATE TABLE submissions (
    submission_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    file_name VARCHAR(200) NOT NULL,
    upload_start_time DATETIME NOT NULL,
    upload_end_time DATETIME NULL,
    file_path VARCHAR(500) NOT NULL,
    processing_status_id INTEGER,
    load_date DATETIMEOFFSET(7) DEFAULT ((CONVERT([datetimeoffset],sysutcdatetime(),(126)) AT TIME ZONE 'Mountain Standard Time'))
    CONSTRAINT fk_processing_status
        FOREIGN KEY (processing_status_id) 
        REFERENCES statuses(processing_status_id)
);
