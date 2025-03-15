CREATE TABLE visits_check (
    visit_id_lnk BINARY(32) PRIMARY KEY,    
    site_name VARCHAR(100) NOT NULL,
    submissionYYYYMM INT NOT NULL,
    submission_id BIGINT NULL,
    ed_visit_id BINARY(32) NOT NULL,
    ed_mrn BINARY(32) NOT NULL,    
    review_batch_id BINARY(32) NULL,
    human_reviewed BIT default(0),
    llm_reviewed BIT default(0),
    human_sensitive_found BIT default(0),
    llm_sensitive_found BIT default(0),
    load_date DATETIMEOFFSET(7)
);