from database import reset_demo_sql
from pipeline_utils import reset_files
from processes import intake
from database.submissions_interface import create_submission

def process_loop():
    print("Processing loop...")
    intake.process_submissions()
    print("Processing loop complete!")

def reset_demo_project():
    print("Resetting the demo system...")
    reset_demo_sql.reset_demo_staging_sql()
    reset_demo_sql.reset_demo_submission_sql()
    reset_demo_sql.reset_demo_deid_sql()
    reset_demo_sql.reset_demo_warehouse_sql()
    reset_demo_sql.reset_demo_grouping_sql()

    reset_files.reset_quarantine()
    reset_files.reset_archive()
    reset_submissions()
    print("Demo system reset!")

def reset_submissions():
    create_submission("ghost_202303.xml", ".\\files\\landing\\ghost\\")


def main():
    print("Ready Player One!")
    reset_demo_project()
    process_loop()


if __name__ == "__main__":
    main()