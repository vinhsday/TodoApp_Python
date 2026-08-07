from models.new_task import Task
from services.todo_service import TodoService

def test_database(db):
    assert db is not None

def test_create_task(db, user):
    service = TodoService(db)
    task = service.add_task(
        title="Hello",
        user=user
    )
    assert task.id is not None
    assert task.title == "Hello"
    assert task.user_id == user.id

def test_delete_task(db,user):
    service = TodoService(db)
    task = service.add_task(
        title="Hello",
        user=user
    )

    deleted_task = service.delete_task(task.id,
                                       user=user)

    assert task.title == deleted_task.title
    assert db.query(Task).filter(Task.user_id == user.id).filter(Task.id == deleted_task.id).scalar() is None
    
    