from database.deid_eng import pull_random_subset, pull_narratives, visits_to_deid, narratives_to_deid_return_list, add_llm_findings
from database.med_eng import pull_stg_hashed_medication_list, get_grp_non_matched_hashed_medications, save_medication
from llms.llm_deid import detect_pii_phi
from llms.llm_med import detect_medication
from pipeline_utils.sleep_pipeline import sleep_llm_process


def run_workflow4(submission_id):
    run_deid_workflow(submission_id)
    run_med_workflow(submission_id)

    
def run_deid_workflow(submission_id):
    visit_data, visit_ids = pull_random_subset(submission_id)
    narratives_data = pull_narratives(visit_ids)
    visits_to_deid(visit_data)    
    narrative_list = narratives_to_deid_return_list(narratives_data)
    
    deid_failures = 0
    for narrative in narrative_list:
        try:
            narrative_hash = narrative['hash_narrative_text']  #narrative.hash_narrative_text
            narrative_text = narrative['narrative_text']
            visit_id_lnk = narrative['visit_id_lnk']
            #if(narrative['site_name'] == 'qbert'):  site testing
            #    i = 1

            result = detect_pii_phi(narrative_text)        
            #print(result)
            add_llm_findings(visit_id_lnk, narrative_hash, result)
            sleep_llm_process()     # prevent rate limits
        except Exception as e:
            print(f"Error processing narrative: {narrative_hash}")
            deid_failures += 1
            continue

    push_metrics_deid(submission_id, deid_failures)

    # TESTING CASE
    # input_text = """
    # John Doe, born on 01/15/1980, lives at 1234 Elm Street, New York, NY. 
    # His social security number is 123-45-6789 and his phone number is (555) 123-4567. 
    # He visited the hospital on 03/10/2023 for a knee injury.
    # """
    
    # result = detect_pii_phi(input_text)
    # print("\n=== Identified PII/PHI ===")
    # print(result)
    #print("De-identification workflow complete") 

def run_med_workflow(submission_id):
    staging_med_data = pull_stg_hashed_medication_list(submission_id)
    meds_to_be_grouped = get_grp_non_matched_hashed_medications(staging_med_data)
    medication_failures = 0
    meds_to_be_grouped_count = len(meds_to_be_grouped)
    #print(f"Non-matched medications:")
    for hash_val, med_name in meds_to_be_grouped:
        try:
            result = detect_medication(med_name)
        #   print (result)
        #   print(f"Hash: {hash_val}, Medication: {med_name}")
            save_medication(hash_val, result)
            sleep_llm_process()     # prevent rate limits
        except Exception as e:
            print(f"Error processing medication: {med_name}")
            medication_failures += 1
            continue
    push_metrics_medication(submission_id, medication_failures)
    push_metrics_medication_count(submission_id, meds_to_be_grouped_count)


# PUSHGATEWAY    
from metrics.pushgateway import MetricsReporter

def push_metrics_deid(submission_id, deid_failures):
    reporter = MetricsReporter()
    # Report metrics during processing    
    reporter.report_deid_llm_failure(submission_id, deid_failures)

def push_metrics_medication(submission_id, medication_failures):
    reporter = MetricsReporter()
    # Report metrics during processing    
    reporter.report_med_lookup_failure(submission_id, medication_failures)

def push_metrics_medication_count(submission_id, meds_to_be_grouped_count):
    reporter = MetricsReporter()
    # Report metrics during processing    
    reporter.report_med_lookup(submission_id, meds_to_be_grouped_count)