import requests

# Your Asana API Token (replace with the actual token)
api_token = "your_asana_api_token_here"

# Function to set up headers for API requests
def get_asana_headers(api_token):
    return {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

# Function to test the API connection by making a sample request
def test_asana_connection(api_token):
    headers = get_asana_headers(api_token)
    try:
        response = requests.get('https://app.asana.com/api/1.0/users/me', headers=headers)
        # Check for a successful response
        if response.status_code == 200:
            print('Connection successful.')
            print('User info:', response.json())
        else:
            print(f'Connection failed. Status code: {response.status_code}')
            print('Response:', response.text)
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

# Run the test
if __name__ == "__main__":
    test_asana_connection(api_token)
