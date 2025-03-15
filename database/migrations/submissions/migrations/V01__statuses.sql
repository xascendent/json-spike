CREATE TABLE statuses (
    processing_status_id INT NOT NULL PRIMARY KEY,
    processing_status_description VARCHAR(200) NOT NULL,
    load_date DATETIMEOFFSET(7) DEFAULT ((CONVERT([datetimeoffset],sysutcdatetime(),(126)) AT TIME ZONE 'Mountain Standard Time'))
)