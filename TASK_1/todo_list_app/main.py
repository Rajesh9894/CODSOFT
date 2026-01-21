import json
import os
from datetime import datetime

class Task:
    def __init__(self, description, id=None, completed=False, created_at=None):
        self.id = id if id else self.generate_id()
        self.description = description
        self.completed = completed
        self.created_at = created_at if created_at else datetime.now().isoformat()

    def generate_id(self):
        # Simple ID generation based on timestamp
        return str(int(datetime.now().timestamp() * 1000000))

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            description=data['description'],
            id=data['id'],
            completed=data['completed'],
            created_at=data['created_at']
        )

class TodoList:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(task) for task in data]
        return []

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, description):
        task = Task(description)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task added: {description}")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        for i, task in enumerate(self.tasks, 1):
            status = "[✓]" if task.completed else "[ ]"
            print(f"{i}. {status} {task.description}")

    def mark_completed(self, task_number):
        if 1 <= task_number <= len(self.tasks):
            self.tasks[task_number - 1].completed = True
            self.save_tasks()
            print(f"Task {task_number} marked as completed.")
        else:
            print("Invalid task number.")

    def delete_task(self, task_number):
        if 1 <= task_number <= len(self.tasks):
            removed = self.tasks.pop(task_number - 1)
            self.save_tasks()
            print(f"Task deleted: {removed.description}")
        else:
            print("Invalid task number.")

def main():
    todo = TodoList()
    while True:
        print("\n--- To-Do List Menu ---")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            desc = input("Enter task description: ").strip()
            if desc:
                todo.add_task(desc)
            else:
                print("Description cannot be empty.")
        elif choice == '2':
            todo.list_tasks()
        elif choice == '3':
            try:
                num = int(input("Enter task number to mark as completed: ").strip())
                todo.mark_completed(num)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '4':
            try:
                num = int(input("Enter task number to delete: ").strip())
                todo.delete_task(num)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
