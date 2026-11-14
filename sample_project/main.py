import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "tasks.json"


def load_tasks():
    """Load saved tasks from the JSON file."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []


def save_tasks(tasks):
    """Save tasks into the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task(title):
    """Add a new task to the task list."""
    tasks = load_tasks()

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)

    return task


def list_tasks():
    """Display all available tasks."""
    return load_tasks()


def complete_task(task_id):
    """Mark a task as completed."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            return True

    return False


if __name__ == "__main__":
    add_task("Learn Python")
    add_task("Build an AI documentation assistant")

    print("Task Management System")
    print(json.dumps(list_tasks(), indent=4))