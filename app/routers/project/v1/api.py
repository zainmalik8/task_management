from uuid import UUID

from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.logger import logger
from app.models.user import User
from app.models.project import Project
from app.schemas.project import CreateProject, ResponseProject, AssignProject, UserProjectsResponse
from app.utils import BadRequestException

router = APIRouter(tags=["Project Management"])


@router.post("/admin/project", response_model=ResponseProject, status_code=201)
def create_project(project: CreateProject, db: Session = Depends(get_db)):
    try:
        db_project = Project(**project.model_dump())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception as error:
        logger.exception(error)
        raise BadRequestException


@router.get("/admin/project", response_model=list[ResponseProject], status_code=200)
def get_projects(db: Session = Depends(get_db)):
    try:
        return db.query(Project).all()
    except Exception as error:
        logger.exception(error)
        raise BadRequestException


@router.get("/project", response_model=list[UserProjectsResponse], status_code=200)
def get_assigned_projects(request: Request, db: Session = Depends(get_db)):
    try:
        return db.query(User).get(request.state.user_id).projects
    except Exception as error:
        logger.exception(error)
        raise BadRequestException


@router.get("/project/{project_id}", response_model=ResponseProject, status_code=200)
def get_assigned_projects(project_id: UUID, db: Session = Depends(get_db)):
    try:
        if project := db.query(Project).get(project_id):
            return project
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Project ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.put("/admin/project/{project_id}", response_model=ResponseProject, status_code=200)
def update_project(data: CreateProject, project_id: UUID, db: Session = Depends(get_db)):
    try:
        serialized_data = data.model_dump()
        if db_project := db.query(Project).filter(Project.id == project_id).first():
            [setattr(db_project, attribute, value) for attribute, value in serialized_data.items()]
            db.add(db_project)
            db.commit()
            db.refresh(db_project)
            return db_project
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Project ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.delete("/project/{project_id}", status_code=204)
def delete_project(project_id: UUID, db: Session = Depends(get_db)):
    try:
        if db_project := db.query(Project).filter(Project.id == project_id).first():
            db.delete(db_project)
            db.commit()
            return
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Project ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.put("/admin/project/{project_id}/assign", response_model=ResponseProject, status_code=200)
def assign_project(project_id: UUID, data: AssignProject, db: Session = Depends(get_db)):
    try:
        print("debugegr")
        if db_project := db.query(Project).filter(Project.id == project_id).first():
            if user := db.query(User).get(data.user_id):
                db_project.users.append(user)
                db.add(db_project)
                db.commit()
                db.refresh(db_project)
                return db_project
            raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid User ID.")
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Project ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException
