# Project Task Quality Review

Custom Odoo 19 module for implementing a Task Quality Review workflow in the Project app.

## Business Context

Projects require a QA step before tasks are completed. Each project has a designated Quality Inspector who reviews tasks when they reach the review stage.

The expected task workflow is:

```text
To-do -> In Progress -> Ready for Review -> Done
```

A task cannot be moved to `Done` unless the quality review has passed.

## Features

- Adds `Quality Inspector` to Project.
- Adds `Quality Review Passed` to Task.
- Adds `Quality Inspected Date` to Task.
- Shows the related project quality inspector on Task.
- Auto-assigns the project quality inspector when a task enters `Ready for Review`.
- Adds a `Mark Review Passed` button on the task form.
- Blocks moving a task to `Done` unless the review has passed.
- Resets review status when a task is moved back from `Done` to an earlier stage.

## Technical Design

### Extended Models

#### `project.project`

Adds:

```python
quality_inspector_id = fields.Many2one("res.users")
```

#### `project.task`

Adds:

```python
is_done = fields.Boolean("Quality Review Passed")
quality_inspected_date = fields.Datetime("Quality Inspected Date")
quality_inspector_id = fields.Many2one(related="project_id.quality_inspector_id")
```

### Workflow Rules

1. When a task is moved to `Ready for Review`, the project's Quality Inspector is automatically added to `task.user_ids`.
2. When a user tries to move a task to `Done`, the server checks whether `is_done` is `True`.
3. If `is_done` is `False`, a `ValidationError` is raised.
4. When a task is moved back from `Done` to an earlier stage, the current review status is reset.

## Module Structure

```
project_task_quality_review/
├── project_task_quality_review/
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project_project.py
│   │   └── project_task.py
│   └── views/
│       └── project_task_views.xml
├── README.md
└── .gitignore
```

## Installation

1. Clone this repository into your Odoo custom addons directory:

```bash
git clone https://github.com/YOUR_USERNAME/project_task_quality_review.git
```

2. Add the custom addons directory to your Odoo configuration:

```ini
addons_path = /path/to/odoo/addons,/path/to/custom/addons
```

3. Restart Odoo.
4. Activate Developer Mode.
5. Update the Apps list.
6. Search for `Project Task Quality Review`.
7. Install the module.

## Usage

1. Open the Project app.
2. Open or create a project.
3. Set the `Quality Inspector`.
4. Create a task under that project.
5. Move the task to `Ready for Review`.
6. The project's Quality Inspector is automatically assigned to the task.
7. The inspector clicks `Mark Review Passed`.
8. The task can now be moved to `Done`.

## Test Scenarios

### Scenario 1: Auto-assign inspector

1. Create a project.
2. Set a Quality Inspector.
3. Create a task in that project.
4. Move the task to `Ready for Review`.

Expected result:

```
The Quality Inspector is automatically assigned to the task.
```

### Scenario 2: Block Done before review

1. Create a task.
2. Move it directly to `Done` without clicking `Mark Review Passed`.

Expected result:

```
ValidationError: Task cannot be moved to Done until the Quality Review has been passed.
```

### Scenario 3: Pass review and move to Done

1. Move a task to `Ready for Review`.
2. Click `Mark Review Passed`.
3. Move the task to `Done`.

Expected result:

```
The task is successfully moved to Done.
```

### Scenario 4: Move Done task back to In Progress

1. Move a reviewed task to `Done`.
2. Move it back to `In Progress`.

Expected result:

```
Quality Review Passed is reset to False.
Quality Inspected Date is cleared.
```
