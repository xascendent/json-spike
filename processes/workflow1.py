from database.submissions_eng import submission_id_from_file_name, update_submission_status
from database.enums import SubmissionStatus
from pipeline_utils import xml_pipeline


def run_workflow1(xml_file, submission_id, XSD_SCHEMA):
    # process file: check file against xsd and shred submission    
    result = False
    if file_xsd_check(xml_file, XSD_SCHEMA, submission_id):
        result = xml_processing(xml_file, submission_id)                        
    
    if result == False:        
        raise Exception("Error processing file: {xml_file}")


def xml_processing(xml_file, submission_id)->bool:
    # process file: check file against xsd and shred submission
    try:
        update_submission_status(submission_id, SubmissionStatus.SHREDDING_SUBMISSION)
        xml_pipeline.stage_submission(xml_file, submission_id)        
        update_submission_status(submission_id, SubmissionStatus.SHREDDING_SUBMISSION_COMPLETE)
        return True
    except Exception as e:
        print(f"Error processing file: {xml_file}")
        print(e)
        update_submission_status(submission_id, SubmissionStatus.SHREDDING_SUBMISSION_FAILED)
        return False        

def file_xsd_check(xml_file, XSD_SCHEMA, submission_id)->bool:
    # check file against xsd
    update_submission_status(submission_id, SubmissionStatus.VALIDATING_XSD)
    result = xml_pipeline.validate_submission(XSD_SCHEMA, xml_file)
    if result:        
        return True
    else:
        update_submission_status(submission_id, SubmissionStatus.VALIDATING_XSD_FAILED)
        return False