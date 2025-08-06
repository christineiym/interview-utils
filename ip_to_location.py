"""Get location from IP addresses, using a free tier of http://ipinfo.io/ (see site for request limits).

Usage: python -m ip_to_location
"""

import os
from dotenv import load_dotenv
import requests
import csv
import pandas as pd


# Change as necessary
TEST_IP_LIST = ["your-test-ip-here"]  # Use this with an IP address to verify everything works before sending all the requests
BASE_SITE = 'http://ipinfo.io/'
INPUT_CSV = 'input.csv'
INPUT_CSV_IP_COLUMN_LABEL = 'IPAddress'
OUTPUT_CSV = 'output.csv'
CSV_MODE = 'w'  # overwrites the file. If you prefer to append information from multiple runs, use 'a' instead.


def main():
    # Load in credentials
    load_dotenv()
    IP_INFO_TOKEN = os.getenv("IP_INFO_TOKEN")
    params = {
        'token': IP_INFO_TOKEN,  # DO NOT push your private token to a public repository. Make a .env file instead!
    }

    # Load in IP addresses
    df = pd.read_csv(INPUT_CSV)
    ip_list = list(df[INPUT_CSV_IP_COLUMN_LABEL])
    # ip_list = TEST_IP_LIST

    # Collect information
    all_info = []
    for ip_address in ip_list:
        response = requests.get(BASE_SITE + ip_address, params=params)
        data = response.json()

        current_info = {
            'ip': '',
            'hostname': '',
            'city': '',
            'region': '',
            'country': '',
            'loc': '',
            'org': '',
            'postal': '',
            'timezone': ''
        }
        data_info_keys = dict(data).keys()
        for key in data_info_keys:
            current_info.update({key: data[key]})
        all_info.append(current_info)

    # Write to file
    fieldnames = dict(all_info[0]).keys()
    with open(OUTPUT_CSV, CSV_MODE, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_info)


if __name__ == "__main__":
    main()