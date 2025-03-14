import hashlib

def generate_hash(value: str) -> bytes:
    return hashlib.sha256(value.encode('utf-8')).digest()


def generate_unique_visit_id(ed_mrn, ed_visit_id, submissionYYYYMM, site_name):
    # Convert binary data back to hex strings for hashing consistency
    mrn_hex = ed_mrn.hex()
    visit_hex = ed_visit_id.hex()
    
    # Combine all fields into a single string and hash it
    combined_value = f"{mrn_hex}-{visit_hex}-{submissionYYYYMM}-{site_name}"
    return generate_hash(combined_value)