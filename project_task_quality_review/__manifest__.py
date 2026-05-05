{
    "name": "Project Task Quality Review",
    "version": "19.0.1.0.0",
    "summary": "Add a quality review workflow before project tasks can be completed.",
    "description": """
Project Task Quality Review
===========================

This module adds a QA review step to Odoo Project tasks.

Features:
- Add Quality Inspector on Project.
- Add Quality Review Passed and Quality Inspected Date on Task.
- Auto-assign the project quality inspector when a task enters Ready for Review.
- Add a Mark Review Passed button on the task form.
- Block moving a task to Done unless the quality review has passed.
- Reset review status when a Done task is moved back to an earlier stage.
    """,
    "category": "Project",
    "author": "Nguyen The Luan",
    "depends": ["project"],
    "data": [
        "views/project_task_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}