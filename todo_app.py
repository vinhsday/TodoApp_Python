import csv
from task import Task
from datetime import datetime
class TodoApp:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, title, deadline):
        self.tasks.append(Task(title=title,deadline=deadline).create_deadline(deadline))
        self.sort_tasks()

    def show_tasks(self):
        return self.tasks.copy()
    
    def complete_task(self, index) -> None:
        self.get_index(index)
        self.tasks[index - 1].complete()

    def edit_task(self,index,title):
        self.get_index(index)
        self.tasks[index - 1].rename(title)

    def delete_task(self,index):
        self.get_index(index)
        self.tasks.pop(index-1)

    def edit_deadline(self,index,deadline):
        self.get_index(index)
        self.tasks[index-1].create_deadline(deadline)
        self.tasks[index-1].calculate_days_remaining()
        self.tasks[index-1].priority = self.tasks[index-1].prioritize()
        
        self.sort_tasks()

    def sort_tasks(self):
        self.tasks.sort(key=lambda task:(task.days_remaining, task.created_at))
    
    def save(self,filename):
        tasks = [{'title': task.title,
                  'completed': task.completed,
                  'created_at': task.created_at,
                  'deadline': task.deadline,
                  'priority': task.priority,
                  'days_remaining': task.days_remaining
                }
                  for task in self.tasks]
        with open(file=filename, newline='', mode='w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title','completed','created_at','deadline','priority','days_remaining'])
            writer.writeheader()
            writer.writerows(tasks)

    def load(self,filename):
        self.tasks.clear()
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.tasks.append(Task(
                    title=row['title'],
                    completed=(row['completed'] == 'True'),
                    created_at=datetime.strptime(row['created_at'], "%Y-%m-%d %H:%M:%S"),
                    deadline=datetime.strptime(row['deadline'],"%Y-%m-%d %H:%M:%S")
                ))

    def get_index(self,index):
        if index < 1 or index > len(self.tasks):
            raise IndexError("Invalid task index")
        
    