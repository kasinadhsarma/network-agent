import csv
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_cve_database(file_path, chunk_size=1024):
    cve_mapping = {}
    with open(file_path, mode='r', encoding='ISO-8859-1', errors='ignore') as file:
        reader = csv.reader(file, delimiter=';')
        chunk = []
        for row in reader:
            # Skip reserved entries
            if '** RESERVED **' in row[1]:
                continue
            chunk.append(row)
            if len(chunk) >= chunk_size:
                process_chunk(chunk, cve_mapping)
                chunk = []
        if chunk:
            process_chunk(chunk, cve_mapping)
    return cve_mapping

def process_chunk(chunk, cve_mapping):
    for row in chunk:
        try:
            cve_id = row[0]
            description = ';'.join(row[1:])  # Join the rest of the columns as the description
            cve_info = extract_cve_info(description)
            cve_mapping[cve_id] = cve_info
        except IndexError:
            logging.warning(f"Skipping malformed row: {row}")

def extract_cve_info(description):
    """Extract relevant information from the CVE description."""
    # Extract software name and version using regex
    software_patterns = [
        re.compile(r'([a-zA-Z0-9\-_]+)\s+([0-9]+\.[0-9]+(\.[0-9]+)?)'),
        re.compile(r'([a-zA-Z0-9\-_]+)\s+version\s+([0-9]+\.[0-9]+(\.[0-9]+)?)'),
        re.compile(r'([a-zA-Z0-9\-_]+)\s+v([0-9]+\.[0-9]+(\.[0-9]+)?)'),
        re.compile(r'([a-zA-Z0-9\-_]+)\s+([0-9]+\.[0-9]+(\.[0-9]+)?\s+\(.*\))'),
        re.compile(r'([a-zA-Z0-9\-_]+)\s+([0-9]+\.[0-9]+\.[0-9]+)'),
        re.compile(r'([a-zA-Z0-9\-_]+)\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)')
    ]
    common_words = {'before', 'version', 'v'}
    for pattern in software_patterns:
        match = pattern.search(description)
        if match:
            software_name = match.group(1)
            software_version = match.group(2)
            if software_name.lower() not in common_words:
                return {'description': description, 'software_name': software_name, 'software_version': software_version}
    return {'description': description, 'software_name': None, 'software_version': None}

if __name__ == "__main__":
    file_path = 'CVE Databases/cve.csv'
    cve_mapping = parse_cve_database(file_path)
    # Log the first 5 entries to understand the structure
    for cve_id, cve_info in list(cve_mapping.items())[:5]:
        logging.info(f"{cve_id}: {cve_info}")

    # Print the headers and first few rows to understand the structure
    with open(file_path, mode='r', encoding='ISO-8859-1', errors='ignore') as file:
        reader = csv.reader(file, delimiter=';')
        headers = next(reader)
        logging.info(f"Headers: {headers}")
        for i, row in enumerate(reader):
            if i < 5:
                logging.info(f"Row {i+1}: {row}")
            else:
                break
