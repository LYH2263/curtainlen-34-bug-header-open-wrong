from fastapi import APIRouter, Query
from app.schemas.estimate import EstimateRequest
from app.services import estimate_service
router = APIRouter()
@router.get("/estimate")
def get_est(window_id: int = Query(...), fabric_id: int = Query(...), save: bool = False,
            header_tape: bool = False, joint_loss: float | None = None):
    return estimate_service.run_estimate(window_id, fabric_id, save, "", header_tape, joint_loss)
@router.post("/estimate")
def post_est(body: EstimateRequest):
    return estimate_service.run_estimate(body.window_id, body.fabric_id, body.save, body.note,
                                         body.header_tape, body.joint_loss)
