import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_cve_database(file_path, chunk_size=1024):
    cve_mapping = {}
    with open(file_path, mode='r', encoding='ISO-8859-1', errors='ignore') as file:
        reader = csv.reader(file, delimiter=';')
        chunk = []
        for row in reader:
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
            cve_mapping[cve_id] = description
        except IndexError:
            logging.warning(f"Skipping malformed row: {row}")

if __name__ == "__main__":
    file_path = 'CVE Databases/cve.csv'
    cve_mapping = parse_cve_database(file_path)
    # Log the first 5 entries to understand the structure
    for cve_id, description in list(cve_mapping.items())[:5]:
        logging.info(f"{cve_id}: {description}")

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