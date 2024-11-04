import pytest
import os
from render_project_data import save_markdown, convert_html_to_pdf

def test_save_markdown():
    # Test with valid data
    test_output = "# Sample Project\n\n## Milestones\n\n- **Milestone 1** - Due: 2024-11-20\n\n## Tasks\n\n- Task 1 - Status: Incomplete\n"
    output_md_path = "output/test_project_report.md"
    
    # Call the save_markdown function
    save_markdown(test_output, output_md_path)
    
    # Check if the file has been created
    assert os.path.exists(output_md_path)
    
    # Check file content
    with open(output_md_path, "r") as f:
        content = f.read()
        assert content == test_output
    
    # Clean up the test file
    os.remove(output_md_path)

def test_convert_html_to_pdf():
    # Create a simple HTML file for testing
    html_content = "<h1>Test Project</h1><p>Milestone: Phase Completion</p>"
    html_file_path = "output/test_project_report.html"
    pdf_file_path = "output/test_project_report.pdf"

    with open(html_file_path, "w") as f:
        f.write(html_content)

    # Call the conversion function
    convert_html_to_pdf(html_file_path, pdf_file_path)

    # Check if the PDF has been created
    assert os.path.exists(pdf_file_path)

    # Clean up the test files
    os.remove(html_file_path)
    os.remove(pdf_file_path)

def test_save_markdown_missing_data():
    # Test with missing data handling
    empty_data = ""
    output_md_path = "output/test_empty_report.md"
    
    # Call the save_markdown function with empty data
    save_markdown(empty_data, output_md_path)
    
    # Check if the file has been created
    assert os.path.exists(output_md_path)

    # Check file content is empty
    with open(output_md_path, "r") as f:
        content = f.read()
        assert content == empty_data
    
    # Clean up the test file
    os.remove(output_md_path)
