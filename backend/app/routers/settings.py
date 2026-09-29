from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.repositories import settings_repo

router = APIRouter()

class SettingIn(BaseModel):
    key: str
    value: str

@router.get("/settings")
def settings(): return settings_repo.get_all()

@router.post("/settings")
def set_setting(body: SettingIn):
    if body.key == "header_tape_joint_loss":
        try:
            loss = float(body.value)
        except ValueError:
            raise HTTPException(422, "joint loss must be a number")
        if loss < 0:
            raise HTTPException(422, "joint loss must be >= 0")
        body.value = str(loss)
    settings_repo.set_value(body.key, body.value)
    return settings_repo.get_all()
