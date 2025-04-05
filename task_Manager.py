"""
task_Manager.py

Contains the Task and TaskManager classes for ChronoTask CLI.
Handles creating, saving, loading, listing, and deleting tasks using a local JSON file.

Author: Jason Acuna
"""

import json
from datetime import datetime

class Task:
    """
        Represents a single task with a description, category, optional due date, and creation timestamp.
    """
    def __init__(self, description, category, due_date=None, created_at=None):
        self.description = description
        self.category = category
        self.created_at = created_at or datetime.now().isoformat()
        self.due_date = due_date

    def to_dict(self):
        """
        Converts the Task object into a dictionary for JSON serialization.
        """
        return {
            'description': self.description,
            'category': self.category,
            'created_at': self.created_at,
            'due_date': self.due_date
        }

class TaskManager:
    """
    Manages task operations: load, save, add, list, delete.
    Stores tasks in a JSON file.
    """
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """
        Loads tasks from the JSON file into memory.
        Creates an empty list if the file doesn't exist or is empty.
        """
        try:
            with open(self.filename, 'r') as f:
                content = f.read().strip()
                if not content:
                    self.tasks = []
                    return
                data = json.loads(content)
                self.tasks = [Task(**task) for task in data]
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        """
        Saves the current list of tasks to the JSON file.
        """
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, description, category, due_date=None):
        """
        Adds a new task to the task list and saves it.
        """
        task = Task(description, category,due_date)
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        """
        Returns the list of current tasks.
        """
            return self.tasks

    def delete_task(self, index):
        """
        Deletes a task by its zero-based index in the list and saves the change.
        (UI shows 1-based numbers; user input is adjusted before calling this)
        """
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()