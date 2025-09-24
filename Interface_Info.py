# Import the requests library to make HTTP requests to REST APIs
import requests

# Import HTTPBasicAuth for basic username/password authentication
from requests.auth import HTTPBasicAuth

# Import getpass to securely accept a password input without showing it on screen
from getpass import getpass

# Prompt the user to enter their username (usually for authentication with a network device or API)
r1_usernmae = input("Enter your username: ")

# Prompt the user to securely enter their password (input is hidden)
r1_password = getpass("Enter your password: ")

# Define the RESTCONF API endpoint URL for accessing interface data on a device
xe_url = "https://172.16.166.133/restconf/data/ietf-interfaces:interfaces"

# Create a Basic Auth object using the provided username and password
creds = HTTPBasicAuth(username=r1_usernmae, password=r1_password)

# Define the HTTP headers to indicate we want data in YANG-based JSON format
xe_headers = {"Accept": "application/yang-data+json"}

# Send a GET request to the RESTCONF API endpoint with authentication and headers
# verify=False is used to ignore SSL certificate warnings (not safe for production)
int_details = requests.get(url=xe_url, auth=creds, headers=xe_headers, verify=False)

# Print the HTTP status code of the response (e.g., 200 for success, 401 for unauthorized)
print(int_details.status_code)

# Print the actual response body (usually JSON data of the network interfaces or an error message)
print(int_details.text)
