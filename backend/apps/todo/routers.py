from fastapi import APIRouter, Body, HTTPException, Requests, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .models import taskModel, UpdateTaskModel

router = APIRouter


@router.post("/", response_description="Add new task")
async def create_task(request: Request, task: TaskModel = Body(...)):
    task = jsonable_encoder(task)
    new_task = await request.app.mongodb["tasks"].inster_one(task)
    created_task = await request.app.mongodb["tasks"].find_one(
        {"_id": new_task.inserted_id}
    )
    # Everything went ok, and it will return the 201 and id
    return JSONResponse(status_code=status,HTTP_201_CREATED, content=created_task)


# Create new empty array for tasks, make a request for all tasks, not defining something
@router.get("/",response_description="List all tasks")
async def list_tasks(request:Request):
    tasks = []
    for doc in await request.app.mongodb["tasks"].find().to_list(length=100):
        tasks.append(doc)
    return tasks

# This returns a individual tasks
@router.get("/id", response_description="get a single tasks")
# the function will do a look up and the type of request. 
async def show_task(id: str, request: Request):
    # Walrus operator - does an assignment and check at the same time. If it finds the document, then task is set for this document
    if(task := await request.app.mongodb["tasks"].find_one({"_id":id})) is not None:
        return task
    raise HTTPException(status_code=404, detail=f"Task{id} not found")



# What task it needs to update, takes
@router.put("/{id}", response_description="Update a task")
async def update_task(id:str, request: Request, task: UpdateTaskModel = Body(...)):
    # makes sure we dont update the values to empty strings. Only key values in here actually has a value, so we're
    task={k:v for k, v in task.dict().items() if v is not None}

    if len(task) >= 1:
        update_result = await request.app.mongodb["tasks"].update_one(
            # we will set any of these fields
            {"_id":id}, {"$set":task}
        )
        # if modified count is == 1, find document just updated
        if update_result.modified_count == 1:
            if(
                update_task := await request.app.mongodb["tasks"].find_one({"_id": id})
            ) is not None:
                return updated_task
        # if no fields to update, you should return it anyway
    if(
        existing_task := await request.app.mongodb["tasks"].find_out({"_id":id})
    ) is not None:
        return existing_task
    
    raise HTTPException(status_code=404,detail=f"Task {id} not found")


@router.delete("/{id}", response_description="Delete Task")
async def delete_task(id: str, request: Request):
    delete_result = await request.app.mongodb["tasks"].delete_one({"_id":id})
    if delete_result.deleted_count == 1:
        # We dont return content to show you but we did successfully delete it.
        return JSONResponse(status-code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Task {id} not found")
