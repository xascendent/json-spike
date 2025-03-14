## visits.py

# # used for local testing
# def init_db():
#     try:
#         # Use SessionLocal from context.py
#         with SessionLocal() as session:
#             ed_mrn = generate_hash('mrn-123')
#             ed_visit_id = generate_hash('visit-123')
#             submissionYYYYMM = 202503
#             site_name = 'Test Site'

#             # Generate a unique visit ID
#             visit_id_lnk = generate_unique_visit_id(ed_mrn, ed_visit_id, submissionYYYYMM, site_name)

#             new_visit = Visits(
#                 visit_id_lnk=visit_id_lnk,
#                 ed_mrn=ed_mrn,
#                 ed_visit_id=ed_visit_id,
#                 submissionYYYYMM=submissionYYYYMM,
#                 site_name=site_name,
#                 birth_date=datetime(1985, 5, 21).date(),
#                 sex='Male',
#                 ed_door_date=datetime(2025, 3, 13).date(),
#                 ed_door_time=datetime(2025, 3, 13, 10, 30).time()
#             )

#             session.add(new_visit)
#             session.commit()
#             print("✅ Data inserted successfully!")

#     except Exception as e:
#         print(f"❌ Error inserting data: {e}")


# def main():
#     print("Hello from json-spike!")
#     init_db()


# if __name__ == "__main__":
#     main()
