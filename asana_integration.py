import asana
from asana.rest import ApiException
from pprint import pprint

# Configure API client with your Asana API token
def create_asana_client(api_token):
    configuration = asana.Configuration()
    configuration.access_token = api_token
    api_client = asana.ApiClient(configuration)
    return asana.ProjectsApi(api_client)

# Function to fetch all projects in a specific workspace and parse project names and IDs
def fetch_projects_from_asana(api_token, workspace_id):
    # Create Asana Projects API client
    projects_api = create_asana_client(api_token)
    
    try:
        # Specify the workspace in the opts dictionary
        opts = {'workspace': workspace_id}
        response_generator = projects_api.get_projects(opts=opts)
        
        # Convert the generator to a list and extract project names and IDs
        projects = []
        for project in response_generator:
            project_info = {
                "id": project["gid"],
                "name": project["name"]
            }
            projects.append(project_info)
        
        return projects

    except ApiException as e:
        print(f"Exception when calling ProjectsApi->get_projects: {e}")
        return None

# Testing the function
if __name__ == "__main__":
    # Replace these with your actual API token and workspace ID
    api_token = "<YOUR_ASANA_API_TOKEN>"
    workspace_id = "<YOUR_WORKSPACE_ID>"

    # Fetch and display projects
    projects = fetch_projects_from_asana(api_token, workspace_id)
    if projects:
        print("Projects retrieved from Asana:")
        for project in projects:
            pprint(project)
    else:
        print("No projects found or an error occurred.")
