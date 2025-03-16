from datetime import datetime
from database.context_staging import SessionLocal as staging_session
from database.context_warehouse import SessionLocal as warehouse_session
from database.models.staging import Visits as StagingVisit, Medications as StagingMedication, Narratives as StagingNarrative
from database.models.warehouse import Visits as WarehouseVisit, Medications as WarehouseMedication, Narratives as WarehouseNarrative
from sqlalchemy import text

def staging_to_warehouse(submission_id):
    try:
        # Open staging session to read data
        with staging_session() as stg_session:
            visits = stg_session.query(StagingVisit).filter(StagingVisit.submission_id == submission_id).all()

        if not visits:
            print(f"No data found for submission_id: {submission_id}")
            return

        # Open warehouse session to write data
        with warehouse_session() as wh_session:
            for visit in visits:
                # Step 1: Insert Visits
                warehouse_visit = WarehouseVisit(
                    visit_id_lnk=visit.visit_id_lnk,
                    site_name=visit.site_name,
                    submissionYYYYMM=visit.submissionYYYYMM,
                    submission_id=visit.submission_id,
                    ed_visit_id=visit.ed_visit_id,
                    ed_mrn=visit.ed_mrn,
                    birth_date=visit.birth_date,
                    sex=visit.sex,
                    ed_door_date=visit.ed_door_date,
                    ed_door_time=visit.ed_door_time,
                    load_date=datetime.utcnow()
                )
                wh_session.add(warehouse_visit)
                wh_session.flush()  # Flush to get the visit_id_lnk available for relationships

                # Step 2: Insert Medications
                medications = stg_session.query(StagingMedication).filter(
                    StagingMedication.visit_id_lnk == visit.visit_id_lnk
                ).all()

                for med in medications:
                    warehouse_med = WarehouseMedication(
                        visit_id_lnk=med.visit_id_lnk,
                        site_name=med.site_name,
                        submissionYYYYMM=med.submissionYYYYMM,
                        submission_id=med.submission_id,
                        hash_medication_name=med.hash_medication_name,
                        medication_name=med.medication_name,
                        order_entry_date=med.order_entry_date,
                        order_entry_time=med.order_entry_time,
                        medication_route=med.medication_route,
                        load_date=datetime.utcnow()
                    )
                    wh_session.add(warehouse_med)

                # Step 3: Insert Narratives
                narratives = stg_session.query(StagingNarrative).filter(
                    StagingNarrative.visit_id_lnk == visit.visit_id_lnk
                ).all()

                for narrative in narratives:
                    warehouse_narrative = WarehouseNarrative(
                        visit_id_lnk=narrative.visit_id_lnk,
                        site_name=narrative.site_name,
                        submissionYYYYMM=narrative.submissionYYYYMM,
                        submission_id=narrative.submission_id,
                        narrative_text=narrative.narrative_text,
                        narrative_author=narrative.narrative_author,
                        narrative_type=narrative.narrative_type,
                        load_date=datetime.utcnow()
                    )
                    wh_session.add(warehouse_narrative)

            # Commit after all inserts for transaction safety
            wh_session.commit()
            print(f"Data transfer for submission_id {submission_id} completed successfully")

    except Exception as e:
        print(f"Error during ETL transfer: {e}")
        wh_session.rollback()


def remove_previous_site_yyyymm_from_warehouse(site_name, submission_yyyymm):
    with warehouse_session() as session:
        # Use parameterized queries to prevent injection
        session.execute(
            text("DELETE FROM dbo.medications WHERE site_name = :site_name AND submissionYYYYMM = :submissionYYYYMM"),
            {"site_name": site_name, "submissionYYYYMM": submission_yyyymm}            
        )
        session.execute(
            text("DELETE FROM dbo.narratives WHERE site_name = :site_name AND submissionYYYYMM = :submissionYYYYMM"),
            {"site_name": site_name, "submissionYYYYMM": submission_yyyymm}            
        )
        session.execute(
            text("DELETE FROM dbo.visits WHERE site_name = :site_name AND submissionYYYYMM = :submissionYYYYMM"),
            {"site_name": site_name, "submissionYYYYMM": submission_yyyymm}            
        )
        
        # Commit once after all statements
        session.commit()
        print(f"Warehouse cleaned for {site_name} by {submission_yyyymm}")