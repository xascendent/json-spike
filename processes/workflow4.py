from database.deid_eng import pull_random_subset, pull_narratives, visits_to_deid, narratives_to_deid


def run_workflow4(submission_id):
    run_deid_workflow(submission_id)
    # Make Flyway databases

    # LLM 1
    # 1- We will pull the medication data from the staging area and hash the value... maybe we do this on the insert.. SQL CHnages
    # 2- We will check the hash against a Grouper table to see if we have already seen this medication before
    # 3- If we havnen't seen this medication before we will run it against a LLM model to normalize it and flag it in the db as a new medication, we will want to add opiod and NHSA flags to the medication
    # 4- We will want to pull the RXNorm code 
    # 5- we will want to update the medication table with the finds.  Otherwsie we do nothing since we have already grouped this medication


    # LLM 2
    # 1- we will want to take a 5% sample of the narritive data and run it against a LLM model to see if we can flag any phi/pii and push the 5% to a new table for review

    
def run_deid_workflow(submission_id):
    visit_data, visit_ids = pull_random_subset(submission_id)
    narratives_data = pull_narratives(visit_ids)
    visits_to_deid(visit_data)
    narratives_to_deid(narratives_data)
    print("De-identification workflow complete") 