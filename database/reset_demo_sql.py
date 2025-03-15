from database.context_staging import SessionLocal as staging_session
from database.context_submission import SessionLocal as submission_session
from database.context_deid import SessionLocal as deid_session
from database.context_warehouse import SessionLocal as warehouse_session
from sqlalchemy import text

def reset_demo_staging_sql():
    with staging_session() as session:
        # Execute multiple statements
        session.execute(text("DELETE dbo.medications"))
        session.execute(text("DELETE dbo.narratives"))
        session.execute(text("DELETE dbo.visits"))
        
        # Commit once after all statements
        session.commit()
        print("Demo system reset!")

        
def reset_demo_submission_sql():
    with submission_session() as session:
        # Execute multiple statements
        session.execute(text("DELETE dbo.submissions"))        
        
        # Commit once after all statements
        session.commit()
        print("Submission system reset!")

def reset_demo_deid_sql():
    with deid_session() as session:
        # Execute multiple statements
        session.execute(text("DELETE dbo.visits_check"))        
        session.execute(text("DELETE dbo.narratives"))
        
        # Commit once after all statements
        session.commit()
        print("De-identification system reset!")

def reset_demo_warehouse_sql():
    with warehouse_session() as session:
        # Execute multiple statements
        session.execute(text("DELETE dbo.medications"))        
        session.execute(text("DELETE dbo.narratives"))
        session.execute(text("DELETE dbo.visits"))
        
        # Commit once after all statements
        session.commit()
        print("Warehouse system reset!")