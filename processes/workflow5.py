from database.clean_db_eng import remove_submission_from_staging
from pipeline_utils.file_pipeline import archive_file


def run_workflow5(submission_id, xml_file):
    clean_staging_by_submission(submission_id)
    move_submission_to_archive(xml_file)

def clean_staging_by_submission(submission_id):
    remove_submission_from_staging(submission_id)
    print("Submission removed from staging")

def move_submission_to_archive(xml_file):
    source_path = str(xml_file)
    archive_file(source_path)
    print(f"Submission moved to archive: {source_path}")
    
    