from todo_app import TodoApp
from task import Task
from datetime import datetime
edit_menu = ''
with open('edit_menu.txt') as f:
    edit_menu = f.read()

confirm_menu = ''
with open('confirm_menu.txt') as f:
    confirm_menu = f.read()

def handle_show(app: TodoApp):
    if get_choice(app):
        tasks = app.show_tasks()
        for task in tasks:
                print(task)

def handle_add(app: TodoApp):
    while True:
        try:
            title = input_title()
            deadline = input_deadline()
            app.add_task(title, deadline=deadline)
        except ValueError as e:
            print(e)
        else:
            break

def handle_detele(app: TodoApp):
    if get_choice(app):
        while True:
            try:
                index = input_index()
                TodoApp.get_index(app,index)
            except (IndexError, ValueError) as e:
                print(e)
            else:
                if handle_confirm():
                    app.delete_task(index)
                break

def handle_complete(app: TodoApp):
        
        while True:
            try:
                index = input_index()
                app.complete_task(index)
            except (IndexError, ValueError) as e:
                print(e)
            else:
                break

def handle_rename(app: TodoApp):

        while True:
            try:
                index = input_index()
                new_title = input_title()
                app.edit_task(index,new_title)
            except (IndexError, ValueError) as e:
                print(e)
            else:
                break

def input_title():
    return input("Enter a title: ").strip()

def input_index():
    return int(input("Enter an index: ").strip())


def get_choice(app: TodoApp):
    if len(app.tasks) <= 0:
        print("There is no task at all!")
        return False
    return True

def handle_edit(app: TodoApp):
    if get_choice(app):
        while True:
            print(edit_menu)
            try:
                choice = int(input("Choose the utility: ").strip())
                if choice < 0 or choice > 2:
                    raise ValueError()
            except ValueError:
                print("There's no chosen utility. Please choose again")
            else:
                if choice == 1:
                    handle_rename(app)
                elif choice == 2:
                    handle_deadline(app)
                break

def handle_confirm():
    choice_of_yes = ('y','yes')
    choice_of_no = ('n','no')
    while True:
        print(confirm_menu)
        choice = (input("[Y/n]?: ").strip()).lower()
        if choice not in choice_of_yes and choice not in choice_of_no:
            continue
        if choice in choice_of_no:
            return False
        elif choice in choice_of_yes:
            print("Change has been done!")
            return True

def input_deadline():
    year = 2026
    month = int(input("Enter a month: ").strip())
    day = int(input("Enter a day: ").strip())
    if month not in range(1,13):
        raise ValueError()
    else:
        if day in (1,3,5,7,8,10,12):
            if day not in range(1,32):
                raise ValueError()
            else:
                if day not in range(1,31):
                    raise ValueError()
    deadline = f"{year}-{month}-{day}"
    return datetime.strptime(deadline,"%Y-%m-%d")

def handle_deadline(app: TodoApp):
    while True:
        try:
            index = input_index()
            new_deadline = input_deadline()
            app.edit_deadline(index, new_deadline)
        except (IndexError, ValueError) as e:
                print(e)
        else:
            break
            
