#!/usr/bin/env python3

"""
Network Agent Script

This script is designed to collect system and network activity data on a Linux machine.
It includes functionality for detecting Common Vulnerabilities and Exposures (CVEs) based on open ports and a CVE database.

Key Features:
- Collects various system metrics such as CPU usage, memory information, disk usage, and network statistics.
- Collects network-related data such as hostname and IP address.
- Detects CVEs based on the services running on open ports and the CVE database.
- Generates HMAC for the collected data using a secret key for authentication.
- Writes the collected data and HMAC to a JSON file with a timestamped filename.

Recent Changes:
- Refactored the `load_cve_database` function to accept `cve_database_path` as an argument.
- Refactored the `detect_cves` function to accept `cve_database` as an argument.
- Updated the `main` function to pass the necessary arguments to the refactored functions.

Environment Variables:
- SECRET_KEY: The secret key used for HMAC generation.
- DATA_COLLECTION_INTERVAL: The interval (in seconds) at which data is collected (default is 60 seconds).

Usage:
- Ensure the required environment variables are set.
- Run the script to start the network agent data collection process.

Author: kasinadhsarma
Date: 2024-07-12
"""

import psutil
import socket
import json
import time
import hashlib
import hmac
import os
import logging
import csv
import re
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve secret key for HMAC authentication from environment variable
SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY:
    logging.error("SECRET_KEY environment variable not set")
    raise EnvironmentError("SECRET_KEY environment variable not set")

# Retrieve data collection interval from environment variable or use default
DATA_COLLECTION_INTERVAL = int(os.getenv('DATA_COLLECTION_INTERVAL', 60))

# Load CVE database
CVE_DATABASE = {}
CVE_DATABASE_PATH = "CVE Databases/cve.csv"

def load_cve_database(cve_database_path):
    """
    Load the CVE database from the specified file path and populate the global CVE_DATABASE dictionary.

    Args:
        cve_database_path (str): The path to the CVE database CSV file.

    Raises:
        Exception: If there is an error loading the CVE database.
    """
    global CVE_DATABASE
    try:
        CVE_DATABASE = parse_cve_database(cve_database_path)
        logging.info("CVE database loaded successfully")
    except Exception as e:
        logging.error(f"Error loading CVE database: {e}")

def parse_cve_database(file_path, chunk_size=1024):
    """
    Parse the CVE database file and populate a dictionary with CVE IDs and descriptions.

    Args:
        file_path (str): The path to the CVE database CSV file.
        chunk_size (int): The number of rows to process in each chunk (default is 1024).

    Returns:
        dict: A dictionary mapping CVE IDs to their descriptions.
    """
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
    """
    Process a chunk of rows from the CVE database and populate the CVE mapping.

    Args:
        chunk (list): A list of rows from the CVE database.
        cve_mapping (dict): A dictionary to populate with CVE IDs and descriptions.
    """
    for row in chunk:
        try:
            cve_id = row[0]
            description = ';'.join(row[1:])  # Join the rest of the columns as the description
            cve_mapping[cve_id] = description
        except IndexError:
            logging.warning(f"Skipping malformed row: {row}")

def collect_system_data():
    """
    Collect various system metrics such as CPU usage, memory information, disk usage, and network statistics.

    Returns:
        dict: A dictionary containing system metrics including CPU usage, memory info, disk usage, network info, and active connections.
    """
    data = {}
    try:
        data['cpu_usage'] = psutil.cpu_percent(interval=1)
        data['memory_info'] = psutil.virtual_memory()._asdict()
        data['disk_usage'] = psutil.disk_usage('/')._asdict()
        data['network_info'] = psutil.net_io_counters()._asdict()
        data['load_avg'] = psutil.getloadavg()
        data['connections'] = [conn._asdict() for conn in psutil.net_connections()]
    except Exception as e:
        logging.error(f"Error collecting system data: {e}")
    return data

def collect_network_data():
    """
    Collect network-related data such as hostname and IP address.

    Returns:
        dict: A dictionary containing the hostname and IP address.
    """
    data = {}
    try:
        hostname = socket.gethostname()
        data['hostname'] = hostname
        data['ip_address'] = socket.gethostbyname(hostname)
    except Exception as e:
        logging.error(f"Error collecting network data: {e}")
    return data

def detect_cves(connections, cve_database):
    """
    Detect CVEs based on the services running on open ports and the CVE database.

    Args:
        connections (list): A list of network connections with local addresses and ports.
        cve_database (dict): A dictionary mapping CVE IDs to their descriptions.

    Returns:
        dict: A dictionary mapping service names to the count of detected CVEs.
    """
    cve_counts = {}
    software_pattern = re.compile(r'([a-zA-Z0-9\-_]+)\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)')

    # Mapping of common port numbers to service names and versions
    port_service_mapping = {
        80: ("httpd", "2.4.41"),
        443: ("nginx", "1.18.0"),
        22: ("openssh", "8.2p1"),
        # Add more mappings as needed
    }

    try:
        for conn in connections:
            port = conn.get('laddr', {}).get('port')
            if port and port in port_service_mapping:
                service_name, service_version = port_service_mapping[port]
                cve_counts[service_name] = 0
                for cve_id, description in cve_database.items():
                    matches = software_pattern.findall(description)
                    for match in matches:
                        cve_software_name, cve_version = match
                        # Check if the service name and version match the CVE description
                        if service_name in cve_software_name and service_version in cve_version:
                            cve_counts[service_name] += 1
        logging.info("CVE detection completed successfully")
    except Exception as e:
        logging.error(f"Error detecting CVEs: {e}")
    return cve_counts

def generate_hmac(data, secret_key):
    """
    Generate HMAC for the given data using the secret key.

    Args:
        data (str): The data for which to generate the HMAC.
        secret_key (str): The secret key used for HMAC generation.

    Returns:
        str: The generated HMAC as a hexadecimal string.
    """
    return hmac.new(secret_key.encode(), data.encode('utf-8'), hashlib.sha256).hexdigest()

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def main():
    """
    Main function to start the network agent data collection process.

    The function performs the following steps:
    1. Loads the CVE database.
    2. Enters an infinite loop to collect system and network data at regular intervals.
    3. Detects CVEs based on the collected data.
    4. Generates an HMAC for the collected data.
    5. Writes the collected data and HMAC to a JSON file with a timestamped filename.
    6. Logs the success or failure of each data collection cycle.

    The data collection interval is determined by the DATA_COLLECTION_INTERVAL environment variable.
    """
    logging.info("Starting network agent data collection")
    load_cve_database(CVE_DATABASE_PATH)

    # Function to start the HTTP server
    def start_http_server():
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, CORSRequestHandler)
        logging.info("Starting HTTP server on port 8000")
        httpd.serve_forever()

    # Start the HTTP server in a separate thread
    http_server_thread = threading.Thread(target=start_http_server)
    http_server_thread.daemon = True
    http_server_thread.start()

    while True:
        try:
            system_data = collect_system_data()
            network_data = collect_network_data()
            combined_data = {**system_data, **network_data}
            combined_data['cve_counts'] = detect_cves(system_data.get('connections', []), CVE_DATABASE)
            combined_data_json = json.dumps(combined_data, indent=4)

            # Generate HMAC for the data
            data_hmac = generate_hmac(combined_data_json, SECRET_KEY)

            # Create a filename with a timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f'network_agent_data_{timestamp}.json'

            # Write data and HMAC to timestamped file
            with open(filename, 'w') as f:
                json.dump({'data': combined_data, 'hmac': data_hmac}, f, indent=4)

            # Write data and HMAC to latest.json
            with open('latest.json', 'w') as f:
                json.dump({'data': combined_data, 'hmac': data_hmac}, f, indent=4)

            logging.info("Data collection and HMAC generation successful")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        time.sleep(DATA_COLLECTION_INTERVAL)

if __name__ == "__main__":
    main()
