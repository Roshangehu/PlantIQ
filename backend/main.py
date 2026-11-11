from fastapi import FastAPI

from backend.api.routes.chat import router as chat_router


app = FastAPI(
    title="PlantIQ API",
    description="AI-powered Industrial Maintenance Assistant",
    version="1.0.0"
)


# Connect chat routes
app.include_router(
    chat_router,
    prefix="/api"
)


@app.get("/")
def home():

    return {
        "message": "Welcome to PlantIQ API",
        "status": "running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }