from contextlib import asynccontextmanager
import subprocess

from fastapi import FastAPI

from app.routers import tasks, users
from app._logger import logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Apply migrations when application starts.
    """
    try:
        result = subprocess.run(
            ["uv", "run", "alembic", "upgrade", "head"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            logger.info("Migrations applied successfully")
            logger.info(result.stdout)
        else:
            logger.error("Error applying migrations: %s", {result.stderr})
            logger.error("Trying to apply migrations through Python API...")

            raise Exception("Failed to apply migrations")
    except Exception as e:
        logger.error("Error initializing database: %s", {e})

    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Task management system",
        description="API for managing personal tasks with user authentication",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(users.router)
    app.include_router(tasks.router)

    return app


app = create_app()


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint with basic API info.
    """
    return {"message": "Task management API", "documentation": "/docs"}
