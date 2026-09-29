from pydantic import BaseModel

class EstimateRequest(BaseModel):
    window_id: int
    fabric_id: int
    save: bool = False
    note: str = ""
    header_tape: bool = False
    joint_loss: float | None = None
