from database.deid_eng import pull_random_subset, pull_narratives, visits_to_deid, narratives_to_deid, narratives_to_deid_return_list, add_llm_findings
from database.med_eng import pull_stg_hashed_medication_list, get_grp_non_matched_hashed_medications
from llms.llm_deid import detect_pii_phi
from pipeline_utils.sleep_pipeline import sleep_llm_process


def run_workflow4(submission_id):
    run_deid_workflow(submission_id)
    run_med_workflow(submission_id)

    
def run_deid_workflow(submission_id):
    visit_data, visit_ids = pull_random_subset(submission_id)
    narratives_data = pull_narratives(visit_ids)
    visits_to_deid(visit_data)
    #narratives_to_deid(narratives_data)
    narrative_list = narratives_to_deid_return_list(narratives_data)
    
    for narrative in narrative_list:
        narrative_hash = narrative['hash_narrative_text']  #narrative.hash_narrative_text
        narrative_text = narrative['narrative_text']
        visit_id_lnk = narrative['visit_id_lnk']
        if(narrative['site_name'] == 'qbert'):
            i = 1

        result = detect_pii_phi(narrative_text)        
        print(result)
        add_llm_findings(visit_id_lnk, narrative_hash, result)
        sleep_llm_process()     # prevent rate limits


    # input_text = """
    # John Doe, born on 01/15/1980, lives at 1234 Elm Street, New York, NY. 
    # His social security number is 123-45-6789 and his phone number is (555) 123-4567. 
    # He visited the hospital on 03/10/2023 for a knee injury.
    # """
    
    # result = detect_pii_phi(input_text)
    # print("\n=== Identified PII/PHI ===")
    # print(result)





    print("De-identification workflow complete") 

def run_med_workflow(submission_id):
    staging_med_data = pull_stg_hashed_medication_list(submission_id)
    meds_to_be_grouped = get_grp_non_matched_hashed_medications(staging_med_data)
    print(f"Non-matched medications:")
    for hash_val, med_name in meds_to_be_grouped:
        print(f"Hash: {hash_val}, Medication: {med_name}")