from fastapi import FastAPI
from .router import router
app = FastAPI(
    title="Network KPI Engine",
    version="0.1.0"
)

app.include_router(router)