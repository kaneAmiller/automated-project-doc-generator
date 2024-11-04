# Project: {{ project_name }}

## Milestones
{% for milestone in milestones %}
- **{{ milestone.name }}** - Due: {{ milestone.due_date }}
{% endfor %}

## Tasks
{% for task in tasks %}
- {{ task.name }} - Status: {% if task.status %}Completed{% else %}Incomplete{% endif %}
  {% if task.due_date %} (Due: {{ task.due_date }}){% endif %}
{% endfor %}
