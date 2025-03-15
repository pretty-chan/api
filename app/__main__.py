import uvicorn
from app.env_validator import settings

if __name__ == "__main__":
    server_arguments = {"host": "0.0.0.0", "port": settings.SERVER_PORT}
    if settings.APP_ENV == "production":
        from app.main import server

        server_arguments.update({"app": server})

    else:
        server_arguments.update({"app": "app.main:server", "reload": True})

    uvicorn.run(**server_arguments, reload=True)
