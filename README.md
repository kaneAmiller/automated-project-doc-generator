# Asana Integration Project

This project provides functions to integrate with Asana’s API, allowing you to fetch project and task data from your Asana workspace. The code includes error handling and unit tests to ensure functionality and resilience.

## Table of Contents
1. [Setup](#setup)
2. [Obtaining an Asana API Key](#obtaining-an-asana-api-key)
3. [Configuration](#configuration)
4. [Example Usage](#example-usage)
5. [Exporting Documents](#exporting-documents)
6. [Template Customization](#template-customization)
7. [API Integration](#api-integration)
8. [Usage Examples](#usage-examples)
9. [Troubleshooting](#troubleshooting)

---

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install required packages**:
   The project relies on the Asana Python client, `pytest`, and `pdfkit` for testing and PDF conversion:
   ```bash
   pip install asana pytest pdfkit
   ```

### Obtaining an Asana API Key

To connect to the Asana API, you'll need a personal API token.

1. Go to [Asana's developer console](https://app.asana.com/0/developer-console).
2. Under **Personal Access Tokens**, create a new token.
3. Copy the token and save it securely; you’ll need it to authenticate API requests.

### Configuration

1. In the `asana_integration.py` file, replace the placeholders with your actual API token and workspace ID:
   ```python
   api_token = "<YOUR_ASANA_API_TOKEN>"
   workspace_id = "<YOUR_WORKSPACE_ID>"
   ```

2. **Find your Workspace ID**:
   - To find the `workspace_id`, run the following code snippet after setting up your API token:
     ```python
     import asana

     client = asana.Client.access_token("<YOUR_ASANA_API_TOKEN>")
     workspaces = client.workspaces.find_all()
     for workspace in workspaces:
         print("Workspace name:", workspace["name"], "| Workspace ID:", workspace["gid"])
     ```

### Example Usage

1. **Fetch Projects in a Workspace**:
   ```python
   from asana_integration import fetch_projects_from_asana

   projects = fetch_projects_from_asana(api_token="<YOUR_ASANA_API_TOKEN>", workspace_id="<YOUR_WORKSPACE_ID>")
   print("Projects:", projects)
   ```

2. **Fetch Tasks for a Specific Project**:
   ```python
   from asana_integration import fetch_tasks_from_project

   tasks = fetch_tasks_from_project(api_token="<YOUR_ASANA_API_TOKEN>", project_id="<PROJECT_ID>", status_filter="incomplete")
   print("Incomplete Tasks:", tasks)
   ```

### Exporting Documents

This project supports exporting project reports in multiple formats, including PDF, Markdown, and HTML.

1. **Exporting to PDF**:
   - Ensure that you have the necessary dependencies installed (`pdfkit` and `wkhtmltopdf`).
   - Use the following function in your script:
     ```python
     convert_html_to_pdf("output/project_report.html", "output/project_report.pdf")
     ```

2. **Exporting to Markdown**:
   - After rendering the Markdown template, save it using the `save_markdown` function:
     ```python
     save_markdown(rendered_markdown, "output/project_report.md")
     ```

3. **Exporting to HTML**:
   - To export the project report as an HTML file, use the `render_template` function:
     ```python
     render_template(api_token, workspace_id, project_id, template_name="project_template.html", output_format="html")
     ```

### Template Customization

This section provides guidance on how users can modify templates and customize their layout.

1. **Modify Templates**:
   - The templates for rendering project data are located in the `templates` folder. You can customize `project_template.html` and `project_template.md` to fit your styling needs.

2. **Adding New Placeholders**:
   - To add new placeholders, edit the Jinja2 templates directly. Placeholders must correspond to the keys passed in the `render_template` function. For example, if you want to display a project description, add a placeholder like `{{ project_description }}` in the template and ensure it's passed in the `render_template` call.

3. **Supported Variables**:
   - Here is a list of supported variables that can be used in the templates:
     - `project_name`: The name of the project.
     - `milestones`: A list of milestone tasks (contains task details).
     - `tasks`: A list of regular tasks (contains task details).

### API Integration

This project utilizes the Asana API to fetch project and task data. 

1. **Setup API Integration**:
   - Ensure you have a valid Asana API token and have set it in the configuration.
   - The integration is facilitated through the `asana_integration.py` file.

2. **Authentication**:
   - The API token must be passed with every API request for authentication. Make sure to replace the placeholder in your code.

### Usage Examples

- **Integrating API and Rendering**:
   - Here’s how you can integrate fetching data from the API and rendering it to different formats:

   ```python
   api_token = "<YOUR_ASANA_API_TOKEN>"
   workspace_id = "<YOUR_WORKSPACE_ID>"
   project_id = "<YOUR_PROJECT_ID>"

   # Fetch projects and render report
   render_template(api_token, workspace_id, project_id, template_name="project_template.html", output_format="html")
   ```

### Troubleshooting

- **Invalid API Key**:
  - Ensure you’re using the correct API token. If you receive an authentication error, double-check the token in your Asana Developer Console.
  - Ensure your token is not expired or revoked by Asana.

- **Workspace or Project Not Found**:
  - Double-check the workspace and project IDs, as they must match exactly with the ones in your Asana account.
  - If you recently created a workspace or project, ensure your API permissions allow access to it.

- **Rate Limit Exceeded**:
  - Asana imposes rate limits on API requests. If you encounter this, reduce the frequency of requests and try again later.

For additional support, refer to the [Asana API Documentation](https://developers.asana.com/docs/).
