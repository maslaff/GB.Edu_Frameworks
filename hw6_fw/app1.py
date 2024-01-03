"""
Создать API для управления списком задач.
Каждая задача должна содержать поля "название",
"описание" и "статус" (выполнена/не выполнена).
API должен позволять выполнять CRUD операции с
задачами.

Напишите API для управления списком задач. Для этого создайте модель Task
со следующими полями:
○ id: int (первичный ключ)
○ title: str (название задачи)
○ description: str (описание задачи)
○ done: bool (статус выполнения задачи)

API должно поддерживать следующие операции:
○ Получение списка всех задач: GET /tasks/
○ Получение информации о конкретной задаче: GET /tasks/{task_id}/
○ Создание новой задачи: POST /tasks/
○ Обновление информации о задаче: PUT /tasks/{task_id}/
○ Удаление задачи: DELETE /tasks/{task_id}/
Для валидации данных используйте параметры Field модели Task.
Для работы с базой данных используйте SQLAlchemy и модуль databases.
"""
from typing import List
from fastapi import FastAPI
from hw6_fw.data_models import Task, TaskIn
from hw6_fw.db_models import database, tasks_table

app = FastAPI()


# @app.get("/fake_tasks/{count}")
# async def create_task(count: int):
#     for i in range(count):
#         query = tasks_table.insert().values(
#             title=f"title{i}", description=f"task{i} - Data", done=False
#         )
#         await database.execute(query)
#     return {"message": f"{count} fake users create"}


@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskIn):
    query = tasks_table.insert().values(**task.dict())
    new_id = await database.execute(query)
    return {**task.dict(), "id": new_id}


@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    # query = tasks_table.select()
    return await database.fetch_all(tasks_table.select())


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    return await database.fetch_one(
        tasks_table.select().where(tasks_table.c.id == task_id)
    )


@app.put("/tasks/edit/{task_id}", response_model=Task)
async def edit_task(task_id: int, mod_task: TaskIn):
    query = (
        tasks_table.update()
        .where(tasks_table.c.id == task_id)
        .values(**mod_task.dict())
    )
    await database.execute(query)
    return {**mod_task.dict(), "id": task_id}


@app.delete("/tasks/remove/{task_id}")
async def remove_task(task_id: int):
    query = tasks_table.delete().where(tasks_table.c.id == task_id)
    await database.execute(query)
    return {"message": "User deleted"}
