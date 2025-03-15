CREATE TABLE narratives (  
    visit_id_lnk BINARY(32) NOT NULL,
    site_name VARCHAR(100) NOT NULL,
    submissionYYYYMM INT NOT NULL,    
    narrative_text NVARCHAR(MAX) NOT NULL,          
    load_date DATETIMEOFFSET(7) 
);