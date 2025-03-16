from database import clean_db_eng
from pipeline_utils import reset_files
from processes import intake
from database.submissions_eng import create_submission

def process_loop():
    print("Processing loop...")
    intake.process_submissions()
    print("Processing loop complete!")

def reset_demo_project():
    print("Resetting the demo system...")
    clean_db_eng.reset_demo_staging_sql()
    clean_db_eng.reset_demo_submission_sql()
    clean_db_eng.reset_demo_deid_sql()
    clean_db_eng.reset_demo_warehouse_sql()
    clean_db_eng.reset_demo_grouping_sql()

    reset_files.reset_quarantine()
    reset_files.reset_archive()
    reset_files.reset_claw_submission()
    reset_submissions()
    print("Demo system reset!")

def reset_submissions():
    create_submission("ghost_202303.xml", ".\\files\\landing\\ghost\\")
    create_submission("ghost_202304.xml", ".\\files\\landing\\ghost\\")
    create_submission("claw.xml", ".\\files\\landing\\dirk\\")
    create_submission("dirk_202501.xml", ".\\files\\landing\\dirk\\")
    create_submission("qbert_202401.xml", ".\\files\\landing\\qbert\\")


def main():
    print("Ready Player One!")
    reset_demo_project()
    process_loop()


if __name__ == "__main__":
    main()