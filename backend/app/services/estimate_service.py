from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters, header_tape_meters
from app.repositories import fabrics, history, settings_repo, windows

def run_estimate(window_id: int, fabric_id: int, save: bool, note: str,
                 header_tape: bool = False, joint_loss: float | None = None):
    w = windows.get_window(window_id)
    f = fabrics.get_fabric(fabric_id)
    if not w or not f:
        raise HTTPException(404, "not found")
    if w.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty window")
    settings = settings_repo.get_all()
    fullness = float(w.get("fullness") or settings.get("default_fullness", 2.0))
    calc = fabric_meters(w["width"], w["height"], fullness, f["hem_top"], f["hem_bottom"], f["fabric_width"])
    calc["header_tape"] = bool(header_tape)
    if header_tape:
        loss = joint_loss if joint_loss is not None else float(settings.get("header_tape_joint_loss") or 0.0)
        loss = float(loss)
        if loss < 0:
            raise HTTPException(422, "joint loss must be >= 0")
        calc["header_tape_joint_loss"] = loss
        calc["header_tape_meters"] = header_tape_meters(calc["finished_width"], loss)
    run_id = history.insert_run(window_id, fabric_id, calc, note) if save else None
    return {"window": w, "fabric": f, "run_id": run_id, **calc}
