from database.deid_eng import pull_random_subset, pull_narratives, visits_to_deid, narratives_to_deid
from database.med_eng import pull_stg_hashed_medication_list, get_grp_non_matched_hashed_medications


def run_workflow4(submission_id):
    run_deid_workflow(submission_id)
    run_med_workflow(submission_id)

    
def run_deid_workflow(submission_id):
    visit_data, visit_ids = pull_random_subset(submission_id)
    narratives_data = pull_narratives(visit_ids)
    visits_to_deid(visit_data)
    narratives_to_deid(narratives_data)
    print("De-identification workflow complete") 

def run_med_workflow(submission_id):
    staging_med_data = pull_stg_hashed_medication_list(submission_id)
    meds_to_be_grouped = get_grp_non_matched_hashed_medications(staging_med_data)
    print(f"Non-matched medications:")
    for hash_val, med_name in meds_to_be_grouped:
        print(f"Hash: {hash_val}, Medication: {med_name}")