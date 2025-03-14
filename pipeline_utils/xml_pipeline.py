from lxml import etree
from database.staging_context import SessionLocal
from database.models.submissions import Visits, Medications, Narratives
from datetime import datetime
from pipeline_utils.hashing import generate_unique_visit_id

def load_xsd_into_memory(xsd_file)->etree.XMLSchema:
    # Load schema into memory.  Everything is passed by reference.
    with open(xsd_file, 'rb') as f:
        return etree.XMLSchema(etree.parse(f))

def validate_submission(xsd, xml_file)->bool:    
    # Load XML file    
    with open(xml_file, 'rb') as f:
        xml = etree.parse(f)

    # Validate
    if xsd.validate(xml):
        print("✅ XML is valid!")
        return True
    else:
        print("❌ XML is invalid!")
        for error in xsd.error_log:
            print(f"Line {error.line}, Col {error.column}: {error.message}")
    return False

def stage_submission(xml_file):
    with open(xml_file, 'rb') as f:
        tree = etree.parse(f)
    
    root = tree.getroot()
    schema_version = root.attrib.get('SchemaVersion')
    submission_yyyymm = int(root.attrib.get('SubmissionYYYYMM'))
    site_name = root.attrib.get('Site')

    submissions = root.findall('.//Submission')
    with SessionLocal() as session:
        for submission in submissions:
            patient_data = submission.find('PatientData')
            ed_visit_id = bytes.fromhex(patient_data.find('EdVisitId').text)
            ed_mrn = bytes.fromhex(patient_data.find('EdMrn').text)
            birth_date = datetime.strptime(patient_data.find('BirthDate').text, '%Y-%m-%d').date()
            sex = patient_data.find('Sex').text
            ed_door_date = datetime.strptime(patient_data.find('EDDoorDate').text, '%Y-%m-%d').date()
            ed_door_time = datetime.strptime(patient_data.find('EDDoorTime').text, '%H:%M:%S').time()

            # Generate unique visit_id_lnk
            visit_id_lnk = generate_unique_visit_id(ed_mrn, ed_visit_id, submission_yyyymm, site_name)
            # Create Visit object
            visit = Visits(
                visit_id_lnk=visit_id_lnk,
                ed_mrn=ed_mrn,
                ed_visit_id=ed_visit_id,
                submissionYYYYMM=submission_yyyymm,
                site_name=site_name,
                birth_date=birth_date,
                sex=sex,
                ed_door_date=ed_door_date,
                ed_door_time=ed_door_time
            )

            # Handle Medications
            medications = patient_data.findall('.//Medication')
            for med in medications:
                med_name = med.find('MedName').text
                order_entry_date = datetime.strptime(med.find('OrderEntryDate').text, '%Y-%m-%d').date()
                order_entry_time = datetime.strptime(med.find('OrderEntryTime').text, '%H:%M:%S').time()
                med_route = med.find('MedRoute').text

                medication = Medications(
                    visit_id_lnk=visit_id_lnk,
                    site_name=site_name,
                    submissionYYYYMM=submission_yyyymm,
                    medication_name=med_name,
                    order_entry_date=order_entry_date,
                    order_entry_time=order_entry_time,
                    medication_route=med_route
                )
                visit.medications.append(medication)

            # Handle Narratives
            narratives = patient_data.findall('.//Narrative')
            for narrative in narratives:
                narrative_text = narrative.find('NarrativeText').text
                narrative_author = narrative.find('NarrativeAuthor').text
                narrative_type = narrative.find('NarrativeType').text

                narrative_obj = Narratives(
                    visit_id_lnk=visit_id_lnk,  # FK reference
                    site_name=site_name,
                    submissionYYYYMM=submission_yyyymm,
                    narrative_text=narrative_text,
                    narrative_author=narrative_author,
                    narrative_type=narrative_type
                )
                visit.narratives.append(narrative_obj)

            # Add visit with medications and narratives
            session.add(visit)

        # Commit once at the end
        session.commit()
        print("✅ Submission processed successfully!")