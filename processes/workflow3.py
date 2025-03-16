from database.warehouse_eng import staging_to_warehouse, remove_previous_site_yyyymm_from_warehouse
from database.staging_eng import get_submission_info

def run_workflow3(submission_id):
    site_name, submission_yyyymm = get_submission_info(submission_id)
    remove_previous_site_yyyymm_from_warehouse(site_name, submission_yyyymm)
    staging_to_warehouse(submission_id)