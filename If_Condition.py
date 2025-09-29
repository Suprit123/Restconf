# Import the requests library to make HTTP requests to REST APIs
import requests

# Import HTTPBasicAuth for basic username/password authentication
from requests.auth import HTTPBasicAuth

# Import getpass to securely accept a password input without showing it on screen
from getpass import getpass

# Imports Python's built-in JSON module to convert Python dictionaries to JSON strings
# (for sending in RESTCONF requests), and to parse JSON responses from the server.
import json

# Get device login credentials
username = input("Enter your username: ")
password = getpass("Enter your password: ")

# Authentication and headers setup
auth = HTTPBasicAuth(username=username, password=password)
headers = {"Content-type": "application/yang-data+json"}

# Base URL for RESTCONF API
base_url = "https://172.16.166.133/restconf/data/ietf-interfaces:interfaces"

# Ask how many interfaces to configure
interface_count = int(
    input("Enter the number of interfaces you wish to configure on the device: ")
)

# Loop for interface configurations
for _ in range(interface_count):
    # Prompt for interface type
    interface_type_choice = int(
        input(
            "\nSelect the interface type:\n"
            "1. Physical Interface (e.g., GigabitEthernet)\n"
            "2. Loopback Interface\n"
            "Enter your choice (1 or 2): "
        )
    )

    # Configure Physical Interface
    if interface_type_choice == 1:
        interface_number = input("Enter the physical interface number (e.g., 4): ")
        interface_name = f"GigabitEthernet{interface_number}"
        interface_type = "ethernetCsmacd"
        url = f"{base_url}/interface={interface_name}"
        http_method = "PUT"  # PUT for updating or creating physical interfaces

    # Configure Loopback Interface
    elif interface_type_choice == 2:
        loopback_number = input("Enter the Loopback Interface number (e.g., 0): ")
        interface_name = f"Loopback{loopback_number}"
        interface_type = "softwareLoopback"
        url = base_url  # POST for adding new loopback interface
        http_method = "POST"

    # Invalid choice
    else:
        print("Invalid interface type selected. Skipping.")
        continue

    # Collect IP configuration
    ip_address = input("Enter the interface IP address (e.g., 192.168.1.1): ")
    subnet_mask = input("Enter the subnet mask (e.g., 255.255.255.0): ")

    # Prepare RESTCONF JSON payload
    interface_payload = {
        "interface": {
            "name": interface_name,
            "type": f"iana-if-type:{interface_type}",
            "enabled": True,
            "ietf-ip:ipv4": {"address": [{"ip": ip_address, "netmask": subnet_mask}]},
        }
    }

    # Send RESTCONF request using specified method
    if http_method == "PUT":
        response = requests.put(
            url=url,
            auth=auth,
            headers=headers,
            data=json.dumps(interface_payload),
            verify=False,  # Disable SSL cert verification (only for lab/testing)
        )
    elif http_method == "POST":
        response = requests.post(
            url=url,
            auth=auth,
            headers=headers,
            data=json.dumps(interface_payload),
            verify=False,
        )

    # Display response status and output
    print(f"\nConfigured Interface: {interface_name}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
