import os
import zipfile
from lxml import etree

XSDPATH = os.path.join(os.path.dirname(__file__), 'xsd')
LANDINGPATH = os.path.join(os.path.dirname(__file__), 'landing', 'submissions')

def validate():
    # Load XSD schema
    xsd_file = os.path.join(XSDPATH, 'aie5.xsd')
    with open(xsd_file, 'rb') as f:
        xsd = etree.XMLSchema(etree.parse(f))

    # Load XML file
    xml_file = os.path.join(LANDINGPATH, 'ghost.xml')
    with open(xml_file, 'rb') as f:
        xml = etree.parse(f)

    # Validate
    if xsd.validate(xml):
        print("✅ XML is valid!")
    else:
        print("❌ XML is invalid!")
        for error in xsd.error_log:
            print(f"Line {error.line}, Col {error.column}: {error.message}")

if __name__ == "__main__":
    validate()
