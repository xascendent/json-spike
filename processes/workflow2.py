from database.staging_rule_eng import check_visits_for_dups
from database.enums import SubmissionStatus
from database.submissions_interface import update_submission_status


def run_workflow2(submission_id):
    run_rules(submission_id)    
    

def run_rules(submission_id):
    print(f"🔎 Checking for duplicate visits for submission ID: {submission_id}")
    update_submission_status(submission_id, SubmissionStatus.RUNNING_RULE_ENGINE)
    duplicates = check_visits_for_dups(submission_id)
    for ed_visit_id, ed_mrn in duplicates:
        print(f"Duplicate Visit ID: {ed_visit_id}, MRN: {ed_mrn}")    
    update_submission_status(submission_id, SubmissionStatus.RULE_ENGINE_COMPLETE)