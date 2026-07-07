from fastapi import APIRouter

router = APIRouter()

@router.get("/api/v1/system")
def system_info():
    return {
        "name": "Network KPI Engine",
        "version": "0.1.0"
    }

@router.get("/api/v1/health")
def health_():
    return {
        "status": "running"
}