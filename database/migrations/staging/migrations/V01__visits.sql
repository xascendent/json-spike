CREATE TABLE visits (
    visit_id_lnk BINARY(32) PRIMARY KEY,
    site_name VARCHAR(100) NOT NULL,
    submissionYYYYMM INT NOT NULL,
    ed_visit_id BINARY(32) NOT NULL,
    ed_mrn BINARY(32) NOT NULL,
    birth_date DATE NOT NULL,
    sex VARCHAR(10) NOT NULL,
    ed_door_date DATE NOT NULL,
    ed_door_time TIME NOT NULL,
    load_date DATETIMEOFFSET(7) DEFAULT ((CONVERT([datetimeoffset],sysutcdatetime(),(126)) AT TIME ZONE 'Mountain Standard Time'))  
);