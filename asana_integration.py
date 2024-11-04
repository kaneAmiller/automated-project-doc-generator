import asana
import json
from asana.rest import ApiException
from pprint import pprint
from jinja2 import Environment, FileSystemLoader

# Asana API Token and Workspace ID
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
def fetch_tasks_from_project(api_token, project_id, status_filter=None):
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
        
        return tasks

    except Exception as e:
        print(f"Exception when calling TasksApi->get_tasks_for_project: {e}")
        return None

def render_template(api_token, workspace_id, project_id, template_name, output_format="html"):
    """
    Populates the specified template with project and task data from the Asana API.

    :param api_token: Asana API token
    :param workspace_id: Asana workspace ID
    :param project_id: Project ID to fetch tasks from
    :param template_name: Template file name ('project_template.html' or 'project_template.md')
    :param output_format: Format to render ('html' or 'markdown')
    :return: Rendered template as a string
    """

    # Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)

    # Fetch project data
    project_data = fetch_projects_from_asana(api_token, workspace_id)

    # Fetch task data
    tasks = fetch_tasks_from_project(api_token, project_id)

    # Find the specific project
    project = next((p for p in project_data if p["id"] == project_id), None)

    if project is None or tasks is None:
        print("Error: Could not retrieve project or task data.")
        return None

    # Render the template with project data
    rendered_template = template.render(
        project_name=project["name"],
        milestones=[],
        tasks=tasks
    )

    # Save to output file with the specified format
    output_filename = f"output/project_report.{output_format}"
    with open(output_filename, "w") as file:
        file.write(rendered_template)

    print(f"Template rendered and saved to {output_filename}")
    return rendered_template

# Testing the functions
if __name__ == "__main__":
    # Fetch and display projects
    print("Fetching projects from Asana...")
    projects = fetch_projects_from_asana(api_token, workspace_id)
    if projects:
        print("Projects retrieved from Asana:")
        for project in projects:
            pprint(project)
            
            # Fetch and display tasks for each project
            print(f"\nFetching tasks for project '{project['name']}' (ID: {project['id']})...")
            tasks = fetch_tasks_from_project(api_token, project["id"])
            if tasks:
                print("Tasks retrieved from Asana:")
                for task in tasks:
                    pprint(task)
            else:
                print("No tasks found or an error occurred.")
    else:
        print("No projects found or an error occurred.")
