import pytest
from unittest.mock import patch, MagicMock
from asana_integration import fetch_projects_from_asana, fetch_tasks_from_project

# Mock API token and workspace/project IDs for testing
api_token = "test_token"
workspace_id = "test_workspace_id"
project_id = "test_project_id"

# Test the project fetching function
@patch("asana_integration.asana.ProjectsApi.get_projects")
def test_fetch_projects_success(mock_get_projects):
    # Simulate a successful response from Asana API
    mock_response = MagicMock()
    mock_response.__iter__.return_value = [{"gid": "123", "name": "Test Project"}]
    mock_get_projects.return_value = mock_response

    projects = fetch_projects_from_asana(api_token, workspace_id)
    assert projects == [{"id": "123", "name": "Test Project"}]

@patch("asana_integration.asana.ProjectsApi.get_projects")
def test_fetch_projects_error(mock_get_projects):
    # Simulate an API error
    mock_get_projects.side_effect = Exception("API error")
    
    projects = fetch_projects_from_asana(api_token, workspace_id)
    assert projects is None

# Test the task fetching function with successful response
@patch("asana_integration.asana.TasksApi.get_tasks_for_project")
def test_fetch_tasks_success(mock_get_tasks_for_project):
    # Simulate a successful response with tasks
    mock_response = MagicMock()
    mock_response.__iter__.return_value = [
        {"gid": "1", "name": "Task 1", "completed": False, "due_on": "2023-12-31"},
        {"gid": "2", "name": "Task 2", "completed": True, "due_on": None},
    ]
    mock_get_tasks_for_project.return_value = mock_response

    tasks = fetch_tasks_from_project(api_token, project_id, status_filter="incomplete")
    assert tasks == [
        {"id": "1", "name": "Task 1", "status": False, "due_date": "2023-12-31"},
    ]

@patch("asana_integration.asana.TasksApi.get_tasks_for_project")
def test_fetch_tasks_error(mock_get_tasks_for_project):
    # Simulate an API error
    mock_get_tasks_for_project.side_effect = Exception("API error")
    
    tasks = fetch_tasks_from_project(api_token, project_id)
    assert tasks is None
