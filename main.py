from db.base import engine, Base
from models.edvisit import EdVisit

def init_db():
    # Create the database and tables if they don’t exist
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database and tables created (if not existing).")

def main():
    print("Hello from json-spike!")
    init_db()

if __name__ == "__main__":
    main()
