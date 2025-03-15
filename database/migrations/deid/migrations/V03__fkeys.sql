ALTER TABLE narratives
ADD CONSTRAINT FK_narratives_visits
FOREIGN KEY (visit_id_lnk)
REFERENCES visits_check (visit_id_lnk);