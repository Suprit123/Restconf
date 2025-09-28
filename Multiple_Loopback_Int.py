# Import the requests library to make HTTP requests to REST APIs
import requests

# Import HTTPBasicAuth for basic username/password authentication
from requests.auth import HTTPBasicAuth

# Import getpass to securely accept a password input without showing it on screen
from getpass import getpass

# Imports Python's built-in JSON module to convert Python dictionaries to JSON strings
# (for sending in RESTCONF requests), and to parse JSON responses from the server.
import json


# Define RESTCONF server base URL for interface configuration
BASE_URL = "https://172.16.166.133/restconf/data/ietf-interfaces:interfaces"

# Prompt the user for credentials (username is hardcoded as "admin")
username = "admin"
password = getpass("Enter your password: ")

# HTTP Basic Authentication using provided credentials
auth = HTTPBasicAuth(username=username, password=password)

# HTTP headers indicating JSON data formatted according to YANG models
headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json",
}

# Ask user how many loopback interfaces they want to configure
num_interfaces = int(input("Enter the number of loopback interfaces to configure: "))

# Loop to configure each interface one by one
for i in range(num_interfaces):
    # Prompt user for interface name (e.g., Loopback10)
    interface_name = input(
        f"\nEnter the name of Loopback interface (e.g., Loopback10): "
    )

    # Prompt user for IP address and subnet mask
    ip_address = input(f"Enter the IP address for {interface_name}: ")
    subnet_mask = input(f"Enter the subnet mask for {interface_name}: ")

    # Construct the JSON payload for the RESTCONF request
    interface_payload = {
        "interface": {
            "name": interface_name,
            "type": "iana-if-type:softwareLoopback",  # YANG model identifier for loopbacks
            "enabled": True,
            "ietf-ip:ipv4": {"address": [{"ip": ip_address, "netmask": subnet_mask}]},
        }
    }

    # Send a POST request to the RESTCONF interface list endpoint
    response = requests.post(
        url=BASE_URL,
        auth=auth,
        headers=headers,
        data=json.dumps(interface_payload),
        verify=False,  # SSL verification disabled; NOT recommended for production
    )

    # Display the result of the POST request
    print(f"\nResult for {interface_name}:")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
