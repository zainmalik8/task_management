from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.logger import logger
from app.models.comment import Comment
from app.models.task import Task
from app.schemas.comment import CreateComment, ResponseComment, UpdateComment
from app.utils import BadRequestException

router = APIRouter(tags=["Comments/Replies"], prefix="/project/task")


@router.post("/{task_id}/comment", response_model=ResponseComment, status_code=201)
def create_comment_reply(task_id: UUID, data: CreateComment, db: Session = Depends(get_db)):
    try:
        if task := db.query(Task).get(task_id):
            db_comment = Comment(**data.model_dump(exclude_defaults=True), task_id=task.id)
            db.add(db_comment)
            db.commit()
            db.refresh(db_comment)
            return db_comment
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Task ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.get("/{task_id}/comment", response_model=list[ResponseComment], status_code=200)
def get_task_comments(task_id: UUID, db: Session = Depends(get_db)):
    try:
        if task := db.query(Task).get(task_id):
            return db.query(Comment).filter(task_id == task.id).all()
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Task ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.put("/comment/{comment_id}", response_model=ResponseComment, status_code=200)
def update_comment(comment_id: UUID, data: UpdateComment, db: Session = Depends(get_db)):
    try:
        if db_comment := db.query(Comment).get(comment_id):
            db_comment.content = data.content
            db.add(db_comment)
            db.commit()
            db.refresh(db_comment)
            return db_comment
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Comment ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.delete("/comment/{comment_id}", status_code=204)
def update_comment(comment_id: UUID, db: Session = Depends(get_db)):
    try:
        if db_comment := db.query(Comment).get(comment_id):
            db.delete(db_comment)
            db.commit()
            return
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Comment ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException
