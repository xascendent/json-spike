import os
from pathlib import Path
from pipeline_utils import xml_pipeline

XSD_PATH = os.getenv("XSD_PATH")
XSD_SCHEMA = xml_pipeline.load_xsd_into_memory(XSD_PATH) 
XML_FILES_PATH = os.getenv("LANDING_PATH")

def process_submissions():
    landing_path = Path(XML_FILES_PATH)
    
    # Loop through first-level subfolders
    for subfolder in landing_path.iterdir():
        if subfolder.is_dir():
            print(f"📂 Processing folder: {subfolder}")

            # Find all XML files under the subfolder (first-level only)
            xml_files = list(subfolder.glob("*.xml"))
            
            for xml_file in xml_files:
                print(f"🔎 Processing file: {xml_file}")
                
                # Validate the file
                if xml_pipeline.validate_submission(XSD_SCHEMA, xml_file):                
                    print(f"✅ {xml_file} is valid")
                    xml_pipeline.stage_submission(xml_file)
                    print(f"✅ {xml_file} processed")
                else:
                    print(f"❌ {xml_file} is invalid")

if __name__ == "__main__":
    process_submissions()