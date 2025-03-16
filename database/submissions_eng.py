from database.context_submission import SessionLocal
from database.models.submission import Submissions
from database.enums import SubmissionStatus
from datetime import datetime, timedelta

def create_submission(file_name: str, file_path: str) -> int:    
    new_submission = Submissions(
        file_name=file_name,
        file_path=file_path,
        upload_start_time=datetime.now() - timedelta(hours=1),
        upload_end_time=datetime.now(),
        processing_status_id=SubmissionStatus.UPLOAD_COMPLETE.value  
    )
    with SessionLocal() as session:
        session.add(new_submission)
        session.commit()
        session.refresh(new_submission)  # Ensure the identity is populated
    
    return new_submission.submission_id


def update_submission_status(submission_id: int, new_status: SubmissionStatus):
    with SessionLocal() as session:
        submission = session.query(Submissions).filter_by(submission_id=submission_id).first()
        if not submission:
            raise ValueError(f"Submission with ID {submission_id} not found.")
        
        submission.processing_status_id = new_status.value    
        session.commit()


def submission_id_from_file_name(file_name: str) -> int:
    with SessionLocal() as session:
        submission = session.query(Submissions).filter_by(file_name=file_name).first()
        if not submission:
            raise ValueError(f"Submission with file name '{file_name}' not found.")                
        
        return submission.submission_id
    return -1 

def file_name_from_submission_id(submissionid) -> str:
    with SessionLocal() as session:
        submission = session.query(Submissions).filter_by(submissionid=submissionid).first()
        if not submission:
            raise ValueError(f"Submission '{submissionid}' not found.")                
        
        return submission.file_name
    
    return "SUBMISSION NOT FOUND"
    
