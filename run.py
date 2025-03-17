import uvicorn

from app._logger import logger

if __name__ == "__main__":
    logger.info("Starting the application...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    logger.info("Application started successfully")
