from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from app import auth, models, schemas
from app.cache import cache, invalidate_cache
from app.database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
) -> models.Task:
    """
    Create a new task.
    """
    db_task = models.Task(**task.model_dump(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    invalidate_cache(f"get_tasks:{current_user.id}")
    invalidate_cache(f"top_priority_tasks:{current_user.id}")

    return db_task


@router.get("/", response_model=list[schemas.Task])
@cache(expire_time=30)
async def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
    sort_by: Literal["title", "status", "created_at", "priority"] = "created_at",
    sort_direction: Literal["asc", "desc"] = "desc",
    skip: int = 0,
    limit: int = 100,
) -> list[models.Task]:
    """
    Get all tasks with sorting options.
    """
    query = db.query(models.Task).filter(models.Task.user_id == current_user.id)

    if sort_direction == "desc":
        query = query.order_by(desc(getattr(models.Task, sort_by)))
    else:
        query = query.order_by(getattr(models.Task, sort_by))

    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.get("/top-priority", response_model=list[schemas.Task])
@cache(expire_time=30)
async def top_priority_tasks(
    n: Annotated[int, Query(gt=0)] = 5,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
) -> list[models.Task]:
    """
    Get top-N priority tasks.
    """
    tasks = (
        db.query(models.Task)
        .filter(models.Task.user_id == current_user.id)
        .order_by(desc(models.Task.priority))
        .limit(n)
        .all()
    )

    return tasks


@router.get("/search", response_model=list[schemas.Task])
async def search_tasks(
    query: Annotated[str, Query(min_length=1)],
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
) -> list[models.Task]:
    """
    Search tasks by title or description.
    """
    tasks = (
        db.query(models.Task)
        .filter(
            models.Task.user_id == current_user.id,
            or_(
                models.Task.title.contains(query),
                models.Task.description.contains(query),
            ),
        )
        .all()
    )

    return tasks


@router.get("/{task_id}", response_model=schemas.Task)
@cache(expire_time=60)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
) -> models.Task:
    """
    Get a specific task by ID.
    """
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.user_id == current_user.id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The task not found"
        )

    return task


@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
) -> models.Task:
    """
    Update a task.
    """
    db_task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.user_id == current_user.id)
        .first()
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )

    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    invalidate_cache(f"get_task:{task_id}")
    invalidate_cache(f"get_tasks:{current_user.id}")
    invalidate_cache(f"top_priority_tasks:{current_user.id}")

    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
) -> None:
    """
    Delete a task.
    """
    db_task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.user_id == current_user.id)
        .first()
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )

    db.delete(db_task)
    db.commit()

    invalidate_cache(f"get_task:{task_id}")
    invalidate_cache(f"get_tasks:{current_user.id}")
    invalidate_cache(f"top_priority_tasks:{current_user.id}")
