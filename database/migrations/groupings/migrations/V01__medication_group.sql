CREATE TABLE medications_group (
    medication_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    hash_medication_name BINARY(32) NULL,
    medication_name NVARCHAR(MAX) NOT NULL,    
    algorithm_used NVARCHAR(MAX) DEFAULT('SHA-256') NULL,
    opioid BIT DEFAULT(0),
    antibiotic BIT DEFAULT(0),
    nsaid BIT DEFAULT(0),
    rxnorm_mappings NVARCHAR(MAX) NOT NULL,
    reviewed BIT DEFAULT(0),    
    load_date DATETIMEOFFSET(7)   
);