# Asana Integration Project

This project provides functions to integrate with Asana’s API, allowing you to fetch project and task data from your Asana workspace. The code includes error handling and unit tests to ensure functionality and resilience.

## Table of Contents
1. [Setup](#setup)
2. [Obtaining an Asana API Key](#obtaining-an-asana-api-key)
3. [Configuration](#configuration)
4. [Example Usage](#example-usage)
5. [Troubleshooting](#troubleshooting)

---

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install required packages**:
   The project relies on the Asana Python client and `pytest` for testing:
   ```bash
   pip install asana pytest
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
   - Replace `"<YOUR_ASANA_API_TOKEN>"` with your actual token to list all accessible workspaces and their IDs.

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
