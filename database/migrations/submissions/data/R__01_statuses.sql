INSERT INTO statuses (
    processing_status_id,    
    processing_status_description    
)
VALUES
(1, 'uploading'),
(2, 'upload complete'),
(3, 'validating xsd'),
(4, 'validating xsd failed'),
(5, 'shredding submission'),
(6, 'shredding submission complete'),
(7, 'processing raw data'),
(8, 'processing complete'),
(9, 'running rule engine'),
(10, 'rule engine complete'),
(11, 'running llm deid check'),
(12, 'running llm medication normalization'),
(13, 'archiving processed file'),
(14, 'processing file complete'),
(15, 'upload failed'),
(16, 'upload shredding failed'),
(17, 'processing raw data failed'),
(18, 'llm deid check failed'),
(19, 'llm medication normalization failed'),
(20, 'processing file failed'),
(21, 'archiving file failed'),
(22, 'rule engine failed'),
(23, 'running deid check eng'),
(24, 'running medication normalization eng')


