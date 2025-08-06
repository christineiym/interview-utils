# interview-utils
Scripts for common screening tasks. 

Usage of specific sites does not imply endorsement. Make sure to comply with privacy laws relevant to your jurisdiction.

## Usage
0) (Optional, but generally recommended; instructions vary based on OS) Create a Python virtual environment.
1) pip install -r requirements.txt
2) Sign up for a personal token to `BASE_SITE` (sites provided in files). Make sure to check sites for the most up-to-date free limits.
    - If I recall correctly, the Location+VPN site has a lower limit than the Location site, so it is wise to screen out people by just location first before inputting the trimmed down list to the script that gives you the VPN. 
3) Rename the .env file to `.env` and paste your token on the appropriate line (no quotes).
4) Adjust constant values in the Python script as necessary.
5) Run Python script with the provided command on the terminal.