import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass
import json

# Prompt user for device credentials
username = input("Enter your username: ")
password = getpass("Enter your password: ")

# RESTCONF endpoint for configuring interfaces on the device
restconf_url = "https://172.16.166.133/restconf/data/ietf-interfaces:interfaces"

# HTTP Basic Authentication using the entered credentials
auth = HTTPBasicAuth(username=username, password=password)

# RESTCONF headers indicating we're using JSON with YANG data format
headers = {"Content-Type": "application/yang-data+json"}

# JSON payload to configure a Loopback10 interface with IPv4 address
interface_payload = {
    "interface": {
        "name": "Loopback10",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [{"ip": "192.168.10.10", "netmask": "255.255.255.0"}]
        },
    }
}

# Make POST request to create/configure the interface
response = requests.post(
    url=restconf_url,
    auth=auth,
    headers=headers,
    data=json.dumps(interface_payload),
    verify=False,  # SSL verification is disabled; not recommended for production
)

# Print the HTTP response status code and response text for debugging
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")
