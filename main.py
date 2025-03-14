from database import reset_demo_sql
from pipeline_utils import reset_files
from processes import intake

def process_loop():
    print("Processing loop...")
    intake.process_submissions()
    print("Processing loop complete!")

def reset_demo_project():
    print("Resetting the demo system...")
    reset_demo_sql.reset_demo_staging_sql()
    reset_demo_sql.reset_demo_submission_sql()
    reset_files.reset_quarantine()
    reset_files.reset_archive()
    print("Demo system reset!")

def main():
    print("Hello from json-spike!")
    reset_demo_project()
    process_loop()


if __name__ == "__main__":
    main()
