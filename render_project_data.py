import json
from jinja2 import Environment, FileSystemLoader
from asana_integration import fetch_projects_from_asana, fetch_tasks_from_project

def load_config():
    """Load configuration settings from config.json."""
    with open("config.json", "r") as config_file:
        return json.load(config_file)

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

    # Fetch project and task data
    project_data = fetch_projects_from_asana(api_token, workspace_id)
    tasks = fetch_tasks_from_project(api_token, project_id)

    # Find the specific project
    project = next((p for p in project_data if p["id"] == project_id), None)
    
    if project is None or tasks is None:
        print("Error: Could not retrieve project or task data.")
        return None

    # Separate tasks into milestones and regular tasks based on keywords
    config = load_config()
    milestone_keywords = config.get("milestone_keywords", [])
    milestones = [
        task for task in tasks 
        if any(keyword.lower() in task.get("name", "").lower() for keyword in milestone_keywords)
    ]
    regular_tasks = [task for task in tasks if task not in milestones]

    # Render the template with project data
    rendered_template = template.render(
        project_name=project["name"],
        milestones=milestones,
        tasks=regular_tasks
    )

    # Save to output file with the specified format
    output_filename = f"output/project_report.{output_format}"
    with open(output_filename, "w") as file:
        file.write(rendered_template)

    print(f"Template rendered and saved to {output_filename}")
    return rendered_template

# Main execution for rendering both HTML and Markdown templates
if __name__ == "__main__":
    # Replace these placeholders with your actual values
    api_token = "<YOUR_ASANA_API_TOKEN>"
    workspace_id = "<YOUR_WORKSPACE_ID>"
    project_id = "<YOUR_PROJECT_ID>"


    # Render HTML version
    render_template(api_token, workspace_id, project_id, template_name="project_template.html", output_format="html")
    # Render Markdown version
    render_template(api_token, workspace_id, project_id, template_name="project_template.md", output_format="md")
