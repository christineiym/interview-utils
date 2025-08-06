"""Get location from IP addresses, using a free tier of https://vpnapi.io/ (see site for request limits).

Usage: python -m ip_to_location_and_vpn
"""

import os
from dotenv import load_dotenv
import requests
import csv
import pandas as pd


# Change as necessary
TEST_IP_LIST = ["your-test-ip-here"]  # Use this with an IP address to verify everything works before sending all the requests
BASE_SITE = 'https://vpnapi.io/api/'
INPUT_CSV = 'input.csv'
INPUT_CSV_IP_COLUMN_LABEL = 'IPAddress'
OUTPUT_CSV = 'output_vpn.csv'
CSV_MODE = 'w'  # overwrites the file. If you prefer to append information from multiple runs, use 'a' instead.


def main():
    # Load in credentials
    load_dotenv()
    VPN_API_TOKEN = os.getenv("VPN_API_TOKEN")
    params = {
        'key': VPN_API_TOKEN,  # DO NOT push your private token to a public repository. Make a .env file instead!
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

        # Our flattened format
        current_info = {
            'ip': '',
            'vpn': '',
            'proxy': '',
            'tor': '',
            'relay': '',
            'city': '',
            'region': '',
            'country': '',
            'continent': '',
            'region_code': '',
            'country_code': '',
            'continent_code': '',
            'latitude': '',
            'longitude': '',
            'time_zone': '',
            'locale_code': '',
            'metro_code': '',
            'is_in_european_union': '',
            'network': '',
            'autonomous_system_number': '',
            'autonomous_system_organization': '',
        }

        ip = data['ip']
        security = data['security']
        location = data['location']
        network = data['network']

        # Extract data from the nested dictionaries in the response
        current_info.update({'ip': ip})
        keys_security = dict(security).keys()
        for key in keys_security:
            current_info.update({key: security[key]})
        keys_location = dict(location).keys()
        for key in keys_location:
            current_info.update({key: location[key]})
        keys_network = dict(network).keys()
        for key in keys_network:
            current_info.update({key: network[key]})
        
        all_info.append(current_info)

    # Write to file
    fieldnames = dict(all_info[0]).keys()
    with open(OUTPUT_CSV, CSV_MODE, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_info)


if __name__ == "__main__":
    main()