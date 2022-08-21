from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.security.api_key import APIKeyBase
from pydantic import BaseModel

from middleware.security import get_api_key
from services.toolslib.tools import create_record_from_repo

router = APIRouter(
    prefix="/tools",
    tags=["tools"],
    responses={404: {"description": "Not found"}},
)


class NewRepo(BaseModel):
    full_name: str


@router.post("/new")
async def tools_webhook(repo: NewRepo, background_tasks: BackgroundTasks, api_key: APIKeyBase = Depends(get_api_key)):
    background_tasks.add_task(create_record_from_repo, repo.full_name)
    return {"message": "Repo has been created"}
