import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

def load_tasks():
    """Loads tasks from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

def save_tasks(tasks):
    """Saves tasks to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(tasks, description):
    """Adds a new task."""
    task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{description}' added.")

def view_tasks(tasks, status=None):
    """Views all tasks or filters by status."""
    if not tasks:
        print("No tasks found.")
        return

    if status:
        filtered_tasks = [task for task in tasks if task['status'] == status]
        if not filtered_tasks:
            print(f"No tasks found with status '{status}'.")
            return
        tasks_to_display = filtered_tasks
        print(f"\n--- {status.capitalize()} Tasks ---")
    else:
        tasks_to_display = tasks
        print("\n--- All Tasks ---")

    for task in tasks_to_display:
        print(f"{task['id']}. {task['description']} - Status: {task['status'].capitalize()}")

def mark_complete(tasks, task_id):
    """Marks a task as complete."""
    try:
        task_id = int(task_id)
        for task in tasks:
            if task['id'] == task_id:
                task['status'] = "completed"
                save_tasks(tasks)
                print(f"Task {task_id} marked as complete.")
                return
        print(f"Task with ID {task_id} not found.")
    except ValueError:
        print("Invalid task ID. Please enter a number.")

def delete_task(tasks, task_id):
    """Deletes a task."""
    try:
        task_id = int(task_id)
        initial_len = len(tasks)
        tasks[:] = [task for task in tasks if task['id'] != task_id]
        if len(tasks) < initial_len:
            save_tasks(tasks)
            print(f"Task {task_id} deleted.")
        else:
            print(f"Task with ID {task_id} not found.")
    except ValueError:
        print("Invalid task ID. Please enter a number.")

def display_help():
    """Displays available commands."""
    print("\n--- Task Tracker CLI Help ---")
    print("Commands:")
    print("  add <description>   - Add a new task.")
    print("  view [pending|completed|all] - View all tasks or filter by status.")
    print("  complete <task_id>  - Mark a task as complete.")
    print("  delete <task_id>    - Delete a task.")
    print("  help                - Show this help message.")
    print("  exit                - Exit the task tracker.")
    print("---------------------------")

def main():
    """Main function to run the CLI."""
    tasks = load_tasks()

    while True:
        command = input("> ").strip().split()

        if not command:
            continue

        action = command[0].lower()

        if action == "add":
            if len(command) > 1:
                description = " ".join(command[1:])
                add_task(tasks, description)
            else:
                print("Please provide a description for the task.")
        elif action == "view":
            if len(command) > 1:
                status = command[1].lower()
                if status in ["pending", "completed", "all"]:
                    view_tasks(tasks, status if status != "all" else None)
                else:
                    print("Invalid view option. Use 'pending', 'completed', or 'all'.")
            else:
                view_tasks(tasks)
        elif action == "complete":
            if len(command) > 1:
                task_id = command[1]
                mark_complete(tasks, task_id)
            else:
                print("Please provide the ID of the task to mark as complete.")
        elif action == "delete":
            if len(command) > 1:
                task_id = command[1]
                delete_task(tasks, task_id)
            else:
                print("Please provide the ID of the task to delete.")
        elif action == "help":
            display_help()
        elif action == "exit":
            print("Exiting task tracker. Goodbye!")
            break
        else:
            print("Invalid command. Type 'help' for available commands.")

if __name__ == "__main__":
    main()
