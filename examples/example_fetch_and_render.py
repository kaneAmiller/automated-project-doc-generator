import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from asana_integration import fetch_projects_from_asana, fetch_tasks_from_project, render_template

def main():
    # Add the project directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # Replace with your actual API token, workspace ID, and project ID
    api_token = "<YOUR_ASANA_API_TOKEN>"
    workspace_id = "<YOUR_WORKSPACE_ID>"
    project_id = "<YOUR_PROJECT_ID>" 

    # Step 1: Fetch Projects from Asana
    print("Fetching projects...")
    projects = fetch_projects_from_asana(api_token, workspace_id)
    print("Projects fetched:", projects)

    # Step 2: Fetch Tasks for a Specific Project
    print(f"Fetching tasks for project ID {project_id}...")
    tasks = fetch_tasks_from_project(api_token, project_id)
    print("Tasks fetched:", tasks)

    # Step 3: Render the Report
    print("Rendering report...")
    # Render HTML report
    render_template(api_token, workspace_id, project_id, template_name="project_template.html", output_format="html")
    
    # Render Markdown report
    render_template(api_token, workspace_id, project_id, template_name="project_template.md", output_format="md")

    print("Reports rendered successfully!")

if __name__ == "__main__":
    main()
