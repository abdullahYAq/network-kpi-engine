from fastapi import APIRouter
from src.config.db_config import db_config
from src.db.technology_repository import get_technology_list
router = APIRouter(
    prefix="/api/v1/technologies",
    tags=["Technologies"]
)


@router.get(
    "/",
    summary="Get all technologies"
)
def get_all_technologies():
    return get_technology_list(db_config)