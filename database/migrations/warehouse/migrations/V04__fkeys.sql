ALTER TABLE narratives
ADD CONSTRAINT FK_narratives_visits
FOREIGN KEY (visit_id_lnk)
REFERENCES visits (visit_id_lnk);


ALTER TABLE medications
ADD CONSTRAINT FK_medications_visits
FOREIGN KEY (visit_id_lnk)
REFERENCES visits (visit_id_lnk);
