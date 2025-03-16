CREATE TABLE narratives (  
    visit_id_lnk BINARY(32) NOT NULL,
    site_name VARCHAR(100) NOT NULL,
    submissionYYYYMM INT NOT NULL,
    hash_narrative_text BINARY(32) NOT NULL,    
    narrative_text NVARCHAR(MAX) NOT NULL,
    human_findings NVARCHAR(MAX) NULL,
    llm_findings NVARCHAR(MAX) NULL,          
    load_date DATETIMEOFFSET(7) 
);