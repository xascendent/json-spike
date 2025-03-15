import os
from pathlib import Path
from pipeline_utils import xml_pipeline
from database.submissions_interface import submission_id_from_file_name, update_submission_status
from database.enums import SubmissionStatus
from processes.workflow1 import run_workflow1
from processes.workflow2 import run_workflow2
from processes.workflow3 import run_workflow3
from processes.workflow4 import run_workflow4

#from database.staging_rule_eng import check_visits_for_dups
import time # used to simulate processing time

XSD_PATH = os.getenv("XSD_PATH")
XSD_SCHEMA = xml_pipeline.load_xsd_into_memory(XSD_PATH) 
XML_FILES_PATH = os.getenv("LANDING_PATH")

def sleep_process():
    print("🛌 Sleeping...")
    time.sleep(3) # Simulate processing time
    print("🍭 Waking up...")


def fail_workflow(submission_id):
    update_submission_status(submission_id, SubmissionStatus.PROCESSING_FILE_FAILED)

def process_submissions():
    landing_path = Path(XML_FILES_PATH)
    
    # Loop through first-level subfolders
    for subfolder in landing_path.iterdir():
        if subfolder.is_dir():
            print(f"📂 Processing folder: {subfolder}")

            # Find all XML files under the subfolder (first-level only)
            xml_files = list(subfolder.glob("*.xml"))
            
            for xml_file in xml_files:
                try:
                    print(f"🔎 Processing file: {xml_file}")
                    submission_id = submission_id_from_file_name(xml_file.name)                                
                    
                    run_workflow1(xml_file, submission_id, XSD_SCHEMA)
                    sleep_process()                    
                    run_workflow2(submission_id)
                    sleep_process()        
                    run_workflow3(submission_id)
                    sleep_process()
                    run_workflow4(submission_id)
                    sleep_process()
                    
                    update_submission_status(submission_id, SubmissionStatus.PROCESSING_FILE_COMPLETE)
                except Exception as e:
                    print(f"Error processing file: {xml_file}")
                    print(e)
                    fail_workflow(submission_id)
                    continue
                


if __name__ == "__main__":
    process_submissions()

  