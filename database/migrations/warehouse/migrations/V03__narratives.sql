CREATE TABLE narratives (
    narrative_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    visit_id_lnk BINARY(32) NOT NULL,
    site_name VARCHAR(100) NOT NULL,
    submissionYYYYMM INT NOT NULL,
    submission_id BIGINT NULL,
    narrative_text NVARCHAR(MAX) NOT NULL,
    narrative_author VARCHAR(200) NOT NULL,
    narrative_type VARCHAR(200) NOT NULL,        
    load_date DATETIMEOFFSET(7) 
);