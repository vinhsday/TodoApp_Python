from task import Task
from todo_app import TodoApp
from handlers import *
menu = ''
with open("menu.txt") as f:
    menu = f.read()

if __name__ == "__main__":
    app = TodoApp()
    try:
        app.load("data.csv")
    except FileNotFoundError:
        pass

    while True:
        print(menu)
        try:
            choice = int(input("Choose the utility: ").strip())
            if choice < 0 or choice > 7:
                raise ValueError()
        except ValueError:
            print("There's no chosen utility. Please choose again")
            continue

        if choice == 1:
            handle_show(app)
        elif choice == 2:
            handle_add(app)
        elif choice == 3:
            handle_edit(app)
        elif choice == 4:
            handle_complete(app)
        elif choice == 5:
            handle_detele(app)
        elif choice == 6:
            app.save("data.csv")
        elif choice == 7:
            app.load("data.csv")
        elif choice == 0:
            app.save("data.csv")
            print("You exited the app ! See you later !")
            break
        


        
