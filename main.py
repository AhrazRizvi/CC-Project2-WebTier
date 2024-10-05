import uvicorn

def start_app():
    """
    Starts the FastAPI application using uvicorn with specified host and port settings.
    """
    uvicorn.run("app:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_app()