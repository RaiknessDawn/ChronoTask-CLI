"""
ChronoTask CLI

A simple command-line task manager built in Python.
Allows users to add, list, filter, and delete tasks with due dates and categories.
Stores tasks locally in a JSON file.

Author: Jason Acuna
"""

from task_Manager import TaskManager
from datetime import datetime

# Initialize TaskManager (handles file I/O and task storage)
tm = TaskManager()

def parse_due_date(raw_date):
    """
        Parses a date string in MM-DD-YYYY format and returns a YYYY-MM-DD string.
        Returns None if the input is invalid.
    """
    try:
        parsed = datetime.strptime(raw_date, "%m-%d-%Y")
        return parsed.strftime("%Y-%m-%d")  # store in clean format
    except ValueError:
        return None

def show_banner():
    """
        Displays the ChronoTask ASCII banner.
    """
    print(r"""
            ('-. .-.             _  .-')                    .-') _               .-') _      ('-.      .-')   .-. .-')   
           ( OO )  /            ( \( -O )                  ( OO ) )             (  OO) )    ( OO ).-. ( OO ). \  ( OO )  
   .-----. ,--. ,--. .-'),-----. ,------.  .-'),-----. ,--./ ,--,'  .-'),-----. /     '._   / . --. /(_)---\_),--. ,--.  
  '  .--./ |  | |  |( OO'  .-.  '|   /`. '( OO'  .-.  '|   \ |  |\ ( OO'  .-.  '|'--...__)  | \-.  \ /    _ | |  .'   /  
  |  |('-. |   .|  |/   |  | |  ||  /  | |/   |  | |  ||    \|  | )/   |  | |  |'--.  .--'.-'-'  |  |\  :` `. |      /,  
 /_) |OO  )|       |\_) |  |\|  ||  |_.' |\_) |  |\|  ||  .     |/ \_) |  |\|  |   |  |    \| |_.'  | '..`''.)|     ' _) 
 ||  |`-'| |  .-.  |  \ |  | |  ||  .  '.'  \ |  | |  ||  |\    |    \ |  | |  |   |  |     |  .-.  |.-._)   \|  .   \   
(_'  '--'\ |  | |  |   `'  '-'  '|  |\  \    `'  '-'  '|  | \   |     `'  '-'  '   |  |     |  | |  |\       /|  |\   \  
   `-----' `--' `--'     `-----' `--' '--'     `-----' `--'  `--'       `-----'    `--'     `--' `--' `-----' `--' '--'  
""")

# Show banner once at startup
show_banner()

# Main CLI loop
def show_menu():
    """
        Prints the main ChronoTask menu.
    """
    print("\n--- ChronoTask CLI — Your terminal task tracker ---")
    print("1. Add Task")
    print("2. List All Tasks")
    print("3. List Tasks by Category")
    print("4. Delete Task")
    print("5. Quit")


while True:
    show_menu()
    choice = input("Choose an option: ")

    if choice == '1':
        # Add new task
        desc = input("Task description: ")
        cat = input("Category (e.g., home, school, work): ").strip().lower()
        due_input = input("Due date (MM-DD-YYYY, optional): ")
        due_date = parse_due_date(due_input) if due_input else None

        if due_input and not due_date:
            print("Invalid date format. Please use MM-DD-YYYY. Saving without due date.")

        tm.add_task(desc, cat, due_date)
        print("Task added!")

    elif choice == '2':
        # List all tasks
        tasks = tm.list_tasks()
        if not tasks:
            print("No tasks found.")

        else:
            for idx, t in enumerate(tasks, start=1):
                created = datetime.fromisoformat(t.created_at)
                pretty_time = created.strftime('%B %d, %Y at %I:%M %p')

                if t.due_date:
                    try:
                        due = datetime.strptime(t.due_date, "%Y-%m-%d")
                        pretty_due = due.strftime("%B %d, %Y")
                    except ValueError:
                        pretty_due = t.due_date
                else:
                    pretty_due = "No due date"
                print(f"{idx}. {t.description} | Category: {t.category} | Due: {pretty_due} | Created: {pretty_time}")

    elif choice == '3':
        # Filter tasks by category
        category = input("Enter category to filter by: ").strip().lower()
        filtered = [t for t in tm.list_tasks() if t.category.lower() == category]
        if not filtered:
            print(f"No tasks found in category '{category}'.")
        else:
            for idx, t in enumerate(filtered, start=1):
                created = datetime.fromisoformat(t.created_at)
                pretty_time = created.strftime('%B %d, %Y at %I:%M %p')
                if t.due_date:
                    try:
                        due = datetime.strptime(t.due_date, "%Y-%m-%d")
                        pretty_due = due.strftime("%B %d, %Y")
                    except ValueError:
                        pretty_due = t.due_date
                else:
                    pretty_due = "No due date"
                print(f"{idx}. {t.description} | Category: {t.category} | Due: {pretty_due} | Created: {pretty_time}")


    elif choice == '4':
        # Delete task by index
        tasks = tm.list_tasks()
        if not tasks:
            print(" No tasks to delete.")
        else:
            for idx, t in enumerate(tasks, start=1):
                print(f"{idx}. {t.description}")

            try:
                idx = int(input("Enter task number to delete: ")) - 1
                if 0 <= idx < len(tasks):
                    tm.delete_task(idx)
                    print(" Task deleted.")
                else:
                    print(" Invalid task number.")
            except ValueError:
                print(" Please enter a valid number.")

    elif choice == '5':
        # Closes the program
        print("Goodbye!")
        break

    else:
        print("Invalid option. Try again.")