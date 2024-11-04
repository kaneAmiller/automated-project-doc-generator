from jinja2 import Environment, FileSystemLoader

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))

# Load templates
html_template = env.get_template('project_template.html')
markdown_template = env.get_template('project_template.md')

# Dummy data
project_data = {
    "project_name": "Farmers Market Fundraiser",
    "milestones": [
        {"name": "Complete Venue Booking", "due_date": "2024-11-15"},
        {"name": "Finalize Vendors", "due_date": "2024-11-20"}
    ],
    "tasks": [
        {"name": "Research local venues", "status": False, "due_date": "2024-11-10"},
        {"name": "Send invitations", "status": True, "due_date": None},
        {"name": "Design event flyers", "status": False, "due_date": "2024-11-12"}
    ]
}

# Render templates with dummy data
html_output = html_template.render(project_name=project_data["project_name"], milestones=project_data["milestones"], tasks=project_data["tasks"])
markdown_output = markdown_template.render(project_name=project_data["project_name"], milestones=project_data["milestones"], tasks=project_data["tasks"])

# Save rendered templates
with open("output/project_report.html", "w") as html_file:
    html_file.write(html_output)

with open("output/project_report.md", "w") as md_file:
    md_file.write(markdown_output)

print("Templates rendered and saved successfully!")
