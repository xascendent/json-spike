from database.warehouse_eng import staging_to_warehouse


def run_workflow3(submission_id):
    staging_to_warehouse(submission_id)