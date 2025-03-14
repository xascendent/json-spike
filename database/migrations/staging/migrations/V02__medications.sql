CREATE TABLE medications (
    medication_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    visit_id_lnk BINARY(32) NOT NULL,
    site_name VARCHAR(100) NOT NULL,
    submissionYYYYMM INT NOT NULL,
    medication_name NVARCHAR(MAX) NOT NULL,
    order_entry_date DATE NOT NULL,
    order_entry_time TIME NOT NULL,
    medication_route NVARCHAR(MAX) NOT NULL,    
    load_date DATETIMEOFFSET(7) DEFAULT ((CONVERT([datetimeoffset],sysutcdatetime(),(126)) AT TIME ZONE 'Mountain Standard Time'))  
);