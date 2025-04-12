import json
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class TodoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self, filename="todo.json"):
        """Load tasks from JSON file"""
        try:
            with open(filename, 'r') as f:
                self.tasks = json.load(f)
            print(Fore.GREEN + "✓ Tasks loaded successfully!")
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def save_tasks(self, filename="todo.json"):
        """Save tasks to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)
        print(Fore.GREEN + "✓ Tasks saved successfully!")

    def add_task(self, description, priority="medium", due_date=None):
        """Add a new task to the list"""
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "priority": priority.lower(),
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        print(Fore.GREEN + f"✓ Added task: {description}")

    def display_tasks(self, show_completed=False):
        """Display tasks in a formatted table"""
        if not self.tasks:
            print(Fore.YELLOW + "No tasks found!")
            return

        print(Fore.CYAN + "\n" + "="*80)
        print(f"{'TO-DO LIST':^80}")
        print("="*80 + Style.RESET_ALL)
        print(f"{'ID':<5} {'Status':<10} {'Priority':<10} {'Due Date':<15} {'Description':<40}")
        print("-" * 80)

        for task in self.tasks:
            if task["completed"] and not show_completed:
                continue

            # Status indicator
            status = Fore.GREEN + "✓ Done" if task["completed"] else Fore.YELLOW + "Pending"

            # Priority color coding
            priority_colors = {
                "high": Fore.RED,
                "medium": Fore.YELLOW,
                "low": Fore.GREEN
            }
            priority = priority_colors.get(task["priority"], "") + task["priority"].capitalize()

            # Due date warning
            due_date = task["due_date"] or "No deadline"
            if task["due_date"] and not task["completed"]:
                due_date_obj = datetime.strptime(task["due_date"], "%Y-%m-%d")
                if due_date_obj < datetime.now():
                    due_date = Fore.RED + "OVERDUE: " + task["due_date"]

            print(f"{task['id']:<5} {status:<10} {priority:<10} {due_date:<15} {task['description'][:38]:<40}")

    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                print(Fore.GREEN + f"✓ Completed task: {task['description']}")
                return
        print(Fore.RED + "Task not found!")

    def delete_task(self, task_id):
        """Remove a task from the list"""
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        print(Fore.GREEN + f"✓ Deleted task ID: {task_id}")

    def edit_task(self, task_id, new_description):
        """Modify an existing task"""
        for task in self.tasks:
            if task["id"] == task_id:
                old_desc = task["description"]
                task["description"] = new_description
                print(Fore.GREEN + f"✓ Updated task: {old_desc} → {new_description}")
                return
        print(Fore.RED + "Task not found!")

def get_user_input(prompt, options=None):
    """Helper function to get validated user input"""
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print(Fore.RED + "Input cannot be empty!")
            continue
        if options and user_input.lower() not in options:
            print(Fore.RED + f"Please choose from: {', '.join(options)}")
            continue
        return user_input

def main():
    todo = TodoList()

    while True:
        print(Fore.CYAN + "\n" + "="*40)
        print(f"{'TO-DO LIST MENU':^40}")
        print("="*40 + Style.RESET_ALL)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. Save Tasks")
        print("7. Load Tasks")
        print("0. Exit")
        print(Style.RESET_ALL + "-" * 40)

        choice = get_user_input("Enter your choice (0-7): ", [str(i) for i in range(8)])

        if choice == '1':
            print(Fore.BLUE + "\n" + "="*40)
            print(f"{'ADD NEW TASK':^40}")
            print("="*40 + Style.RESET_ALL)

            description = get_user_input("Task description: ")
            priority = get_user_input("Priority (high/medium/low): ", ["high", "medium", "low"])
            due_date = input("Due date (YYYY-MM-DD, leave empty if none): ")

            # Validate date format
            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    print(Fore.RED + "Invalid date format! Use YYYY-MM-DD")
                    due_date = None

            todo.add_task(description, priority, due_date)

        elif choice == '2':
            show_completed = get_user_input("Show completed tasks? (y/n): ", ["y", "n"]).lower() == 'y'
            todo.display_tasks(show_completed)

        elif choice == '3':
            todo.display_tasks()
            task_id = int(get_user_input("Enter task ID to complete: "))
            todo.complete_task(task_id)

        elif choice == '4':
            todo.display_tasks()
            task_id = int(get_user_input("Enter task ID to edit: "))
            new_desc = get_user_input("Enter new description: ")
            todo.edit_task(task_id, new_desc)

        elif choice == '5':
            todo.display_tasks()
            task_id = int(get_user_input("Enter task ID to delete: "))
            todo.delete_task(task_id)

        elif choice == '6':
            todo.save_tasks()

        elif choice == '7':
            todo.load_tasks()

        elif choice == '0':
            save = get_user_input("Save before exiting? (y/n): ", ["y", "n"]).lower() == 'y'
            if save:
                todo.save_tasks()
            print(Fore.CYAN + "Goodbye!")
            break

if __name__ == "__main__":
    main()