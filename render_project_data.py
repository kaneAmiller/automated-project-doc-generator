import json
from jinja2 import Environment, FileSystemLoader
from asana_integration import fetch_projects_from_asana, fetch_tasks_from_project
import pdfkit

def load_config():
    """Load configuration settings from config.json."""
    with open("config.json", "r") as config_file:
        return json.load(config_file)

def render_template(api_token, workspace_id, project_id, template_name, output_format="html", use_sample_data=False):
    """
    Populates the specified template with project and task data from the Asana API or sample data for testing.

    :param api_token: Asana API token
    :param workspace_id: Asana workspace ID
    :param project_id: Project ID to fetch tasks from
    :param template_name: Template file name ('project_template.html' or 'project_template.md')
    :param output_format: Format to render ('html' or 'markdown')
    :param use_sample_data: Boolean to indicate whether to load sample data instead of real API data
    :return: Rendered template as a string
    """
    
    # Load sample data if specified
    if use_sample_data:
        with open("sample_data/sample_project.json") as project_file:
            project_data = json.load(project_file)
        
        with open("sample_data/sample_tasks.json") as tasks_file:
            tasks = json.load(tasks_file)
    else:
        # Fetch real project and task data from Asana
        project_data = fetch_projects_from_asana(api_token, workspace_id)
        tasks = fetch_tasks_from_project(api_token, project_id)

        # Find the specific project by ID
        project = next((p for p in project_data if p["id"] == project_id), None)
        if project is None or tasks is None:
            print("Error: Could not retrieve project or task data.")
            return None

    # Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)

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
        project_name=project_data["name"],
        milestones=milestones,
        tasks=regular_tasks
    )

    # Save to output file with the specified format
    output_filename = f"output/project_report.{output_format}"
    with open(output_filename, "w") as file:
        file.write(rendered_template)

    print(f"Template rendered and saved to {output_filename}")
    return rendered_template

def convert_html_to_pdf(html_file_path, output_pdf_path):
    """
    Converts an HTML file to PDF format.

    :param html_file_path: Path to the HTML file to convert
    :param output_pdf_path: Path where the output PDF will be saved
    """
    try:
        pdfkit.from_file(html_file_path, output_pdf_path)
        print(f"PDF generated successfully: {output_pdf_path}")
    except Exception as e:
        print(f"Error generating PDF: {e}")

def save_markdown(rendered_template, output_md_path):
    """
    Saves the rendered Markdown template to a file.

    :param rendered_template: The rendered Markdown template as a string
    :param output_md_path: Path where the output Markdown file will be saved
    """
    with open(output_md_path, "w") as md_file:
        md_file.write(rendered_template)
    print(f"Markdown file saved to {output_md_path}")

# Main execution for rendering both HTML and Markdown templates
if __name__ == "__main__":
    # Replace these placeholders with actual values
    api_token = "<YOUR_ASANA_API_TOKEN>"
    workspace_id = "<YOUR_WORKSPACE_ID>"
    project_id = "<YOUR_PROJECT_ID>"

    # Render HTML version with sample data
    render_template(api_token, workspace_id, project_id, template_name="project_template.html", output_format="html", use_sample_data=True)
    
    # Render Markdown version with sample data
    markdown_output = render_template(api_token, workspace_id, project_id, template_name="project_template.md", output_format="md", use_sample_data=True)

    # Save the rendered Markdown to a file
    save_markdown(markdown_output, "output/project_report.md")

    # Convert rendered HTML to PDF
    convert_html_to_pdf("output/project_report.html", "output/project_report.pdf")
