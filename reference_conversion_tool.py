import os
import xml.etree.ElementTree as ET
import json
import yaml

def read_references(input_path, input_format):
    """Reads references from different formats."""
    references = []
    if input_format == "bibtex":
        with open(input_path, "r", encoding="utf-8") as file:
            references = parse_bibtex(file.read())
    elif input_format == "json":
        with open(input_path, "r", encoding="utf-8") as file:
            references = json.load(file)
    elif input_format == "ris":
        with open(input_path, "r", encoding="utf-8") as file:
            references = parse_ris(file.read())
    elif input_format == "yaml":
        with open(input_path, "r", encoding="utf-8") as file:
            references = parse_yaml(file.read())
    else:
        raise ValueError("Unsupported format: " + input_format)
    return references

def parse_bibtex(content):
    """Parse BibTeX content to a reference list."""
    references = []
    entries = content.split("@")
    for entry in entries[1:]:  # Skip the first split which is before the first @
        lines = entry.splitlines()
        reference = {}
        for line in lines:
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip().lower()
                value = value.strip().strip("{}",).strip(",")
                reference[key] = value
        references.append(reference)
    return references

def parse_ris(content):
    """Parse RIS content to a reference list."""
    references = []
    lines = content.splitlines()
    reference = {}
    for line in lines:
        if line.startswith("TY"):  # Start of a new reference
            if reference:
                references.append(reference)
                reference = {}
        if " - " in line:
            key, value = line.split(" - ", 1)
            key = key.strip().lower()
            value = value.strip()
            reference[key] = value
    if reference:  # Add the last reference
        references.append(reference)
    return references

def parse_yaml(content):
    """Parse YAML content to a reference list."""
    references = yaml.safe_load(content)
    return references

def convert_to_endnote_format(references):
    """Converts a list of references to EndNote XML format."""
    root = ET.Element("xml")
    records = ET.SubElement(root, "records")

    for ref in references:
        record = ET.SubElement(records, "record")
        for key, value in ref.items():
            field = ET.SubElement(record, key)
            field.text = value

    return ET.tostring(root, encoding="utf-8", method="xml").decode("utf-8")

def write_endnote_file(output_path, xml_content):
    """Writes the EndNote XML content to a file."""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(xml_content)

def main():
    input_path = input("Enter the path of the reference file: ")
    input_format = input("Enter the input format (bibtex/json/ris/yaml): ").lower()
    output_path = input("Enter the output path for the EndNote file: ")

    if not os.path.exists(input_path):
        print("Input file does not exist.")
        return

    try:
        references = read_references(input_path, input_format)
        endnote_xml = convert_to_endnote_format(references)
        write_endnote_file(output_path, endnote_xml)
        print("Conversion complete! EndNote file saved at:", output_path)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
