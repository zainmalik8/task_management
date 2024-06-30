from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.logger import logger
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.schemas.task import CreateTask, ResponseTask, UpdateTask, AssignTask
from app.utils import BadRequestException

router = APIRouter(tags=["Tasks/SubTask"], prefix="/project")


@router.post("/{project_id}/task", response_model=ResponseTask, status_code=201)
def create_task(data: CreateTask, project_id: UUID, db: Session = Depends(get_db)):
    try:
        if data.parent_id and (not db.query(Task).get(data.parent_id)):
            raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Parent ID.")
        if data.assignee_id and (not db.query(User).get(data.assignee_id)):
            raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Assignee ID.")
        if project := db.query(Project).get(project_id):
            db_task = Task(**data.model_dump(exclude_defaults=True), project_id=project.id)
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            return db_task
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Project ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.get("/{project_id}/task", response_model=list[ResponseTask], status_code=200)
def list_project_tasks(project_id: UUID, db: Session = Depends(get_db)):
    try:
        if project := db.query(Project).get(project_id):
            return db.query(Task).filter(Task.project_id == project.id).all()
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Project ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.get("/task/{task_id}", response_model=ResponseTask, status_code=200)
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    try:
        if db_task := db.query(Task).get(task_id):
            return db_task
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Task ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.put("/task/{task_id}", response_model=ResponseTask, status_code=200)
def update_task(data: UpdateTask, task_id: UUID, db: Session = Depends(get_db)):
    try:
        data_to_validate = {"assignee_id": "db.query(User).get(value)", "project_id": "db.query(Project).get(value)",
                            "parent_id": "db.query(Task).get(value)"}
        serialized_data = data.model_dump(exclude_defaults=True)
        if db_task := db.query(Task).get(task_id):
            for attribute, value in serialized_data.items():
                if query := data_to_validate.get(attribute):
                    if obj := eval(query):
                        if isinstance(obj, Task) and db_task.id == obj.id:
                            raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND,
                                                      detail=f"Invalid {attribute}")
                        setattr(db_task, attribute, value)
                    else:
                        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid {attribute}")
                else:
                    setattr(db_task, attribute, value)
            db.commit()
            db.refresh(db_task)
            return db_task
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Task ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.delete("/task/{task_id}", status_code=204)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    try:
        if db_task := db.query(Task).get(task_id):
            db.delete(db_task)
            db.commit()
            return
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Task ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.put("/task/{task_id}/assign", response_model=ResponseTask, status_code=200)
def assign_task(data: AssignTask, task_id: UUID, db: Session = Depends(get_db)):
    try:
        if db_task := db.query(Task).get(task_id):
            if user := db.query(User).get(data.assignee_id):
                db_task.assignee_id = user.id
                db.commit()
                db.refresh(db_task)
                return db_task
            raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Assignee ID.")
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Task ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException
