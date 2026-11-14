# Task Management System

## 1. Project Overview
The Task Management System is a simple Python-based application designed to help users create, view, and manage tasks. It uses a JSON file to store tasks, making it easy to manage and persist data across sessions.

## 2. Features
- **Add new tasks**: Allows users to create new tasks with a title and mark them as completed.
- **View all tasks**: Displays a list of all tasks, including their titles and completion status.
- **Mark tasks as completed**: Enables users to mark tasks as completed, which helps in tracking progress.
- **Store tasks in a JSON file**: Persists tasks across sessions using a JSON file, ensuring data is not lost.

## 3. Technologies Used
- **Python**: The primary programming language used for developing the application.
- **JSON**: Used for storing and retrieving tasks in a structured format.

## 4. Project Architecture
The project consists of the following files:
- `config.json`: Configuration file containing application settings.
- `main.py`: Main Python script containing the application logic.
- `README.md`: Markdown file containing project documentation.
- `tasks.json`: JSON file used to store tasks.

## 5. File Structure
```
sample_project/
├── config.json
├── main.py
├── README.md
└── tasks.json
```

## 6. Installation and Setup
To run the Task Management System, follow these steps:
1. Ensure Python is installed on your system.
2. Clone the project repository or download the files.
3. Navigate to the project directory in your terminal.
4. Run the application using the command:
   ```bash
   python main.py
   ```

## 7. Main Functions
### `add_task`
- **Purpose**: Adds a new task to the task list.
- **Parameters**:
  - `title` (str): The title of the task.
- **Returns**: None

### `complete_task`
- **Purpose**: Marks a task as completed.
- **Parameters**:
  - `task_id` (int): The ID of the task to mark as completed.
- **Returns**: None

### `list_tasks`
- **Purpose**: Lists all tasks.
- **Parameters**: None
- **Returns**: List of tasks

### `load_tasks`
- **Purpose**: Loads tasks from the JSON file.
- **Parameters**: None
- **Returns**: List of tasks

### `save_tasks`
- **Purpose**: Saves the current list of tasks to the JSON file.
- **Parameters**: None
- **Returns**: None

## 8. Configuration
The `config.json` file contains the following configuration settings:
- `application_name`: Name of the application.
- `version`: Version of the application.
- `language`: Programming language used.
- `storage`: Type of storage used for tasks.
- `description`: Description of the application.

Example `config.json`:
```json
{
  "application_name": "Task Management System",
  "version": "1.0.0",
  "language": "Python",
  "storage": "JSON",
  "description": "A simple application to create, view and manage tasks."
}
```

## 9. Usage Instructions
### Adding a Task
To add a new task, run the application and use the `add_task` function:
```python
from main import add_task

add_task("Learn Python")
```

### Listing Tasks
To list all tasks, run the application and use the `list_tasks` function:
```python
from main import list_tasks

tasks = list_tasks()
print(tasks)
```

### Completing a Task
To mark a task as completed, run the application and use the `complete_task` function:
```python
from main import complete_task

complete_task(1)
```

## 10. Limitations
- The application does not support task prioritization.
- The application does not have a user interface; it is intended to be run from the command line.

## 11. Conclusion
The Task Management System is a straightforward and effective tool for managing tasks. Its simplicity and ease of use make it ideal for individuals looking for a basic task management solution.