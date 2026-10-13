#importamos desde fastapi nuestra FastAPI
from fastapi import FastAPI

app = FastAPI(
    title="SmartCampus API",
    description="API para la gestión de aulas y reservas universitarias",
    version="1.0.0",
)

@app.get("/health")
def health():
    return {"status": "ok"}