import asana
import json
from asana.rest import ApiException
from pprint import pprint

# Asana API Token and Workspace ID
# Replace these placeholders with your actual values
api_token = "<YOUR_ASANA_API_TOKEN>"
workspace_id = "<YOUR_WORKSPACE_ID>"

# Configure API client with your Asana API token
def create_asana_client(api_token):
    configuration = asana.Configuration()
    configuration.access_token = api_token
    return asana.ApiClient(configuration)

# Function to fetch all projects in a specific workspace and parse project names and IDs
def fetch_projects_from_asana(api_token, workspace_id):
    # Create Asana Projects API client
    api_client = create_asana_client(api_token)
    projects_api = asana.ProjectsApi(api_client)
    
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

    except Exception as e:
        print(f"Exception when calling ProjectsApi->get_projects: {e}")
        return None

# Enhanced function to fetch all tasks for a given project, parse task data, and filter by completion status
def fetch_tasks_from_project(api_token, project_id, status_filter=None, save_to_file=False):
    # Create Asana Tasks API client
    api_client = create_asana_client(api_token)
    tasks_api = asana.TasksApi(api_client)
    
    try:
        # Retrieve tasks for the specified project with an empty opts dictionary
        response_generator = tasks_api.get_tasks_for_project(project_id, opts={})
        
        # Parse relevant task data (e.g., names, status, due dates)
        tasks = []
        for task in response_generator:
            task_info = {
                "id": task["gid"],
                "name": task["name"],
                "status": task.get("completed", False),  # Status as completed/incomplete
                "due_date": task.get("due_on")  # Due date, if available
            }
            
            # Apply status filter if specified
            if status_filter is None or (status_filter == "completed" and task_info["status"]) or (status_filter == "incomplete" and not task_info["status"]):
                tasks.append(task_info)
        
        # Save tasks to a JSON file if requested
        if save_to_file:
            with open(f"tasks_{project_id}.json", "w") as file:
                json.dump(tasks, file, indent=4)
            print(f"Tasks saved to tasks_{project_id}.json")
        
        return tasks

    except Exception as e:
        print(f"Exception when calling TasksApi->get_tasks_for_project: {e}")
        return None

# Testing the functions
if __name__ == "__main__":
    # Fetch and display projects
    print("Fetching projects from Asana...")
    projects = fetch_projects_from_asana(api_token, workspace_id)
    if projects:
        print("Projects retrieved from Asana:")
        for project in projects:
            pprint(project)
    else:
        print("No projects found or an error occurred.")
    
    # Fetch and display tasks for each project with enhanced features
    if projects:
        for project in projects:
            print(f"\nFetching incomplete tasks for project '{project['name']}' (ID: {project['id']})...")
            tasks = fetch_tasks_from_project(api_token, project["id"], status_filter="incomplete", save_to_file=True)
            if tasks:
                print("Tasks retrieved from Asana:")
                for task in tasks:
                    pprint(task)
            else:
                print("No tasks found or an error occurred.")
