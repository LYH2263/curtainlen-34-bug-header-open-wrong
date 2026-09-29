from fastapi import APIRouter, HTTPException
from app.repositories import history as repo, settings_repo
from app.services.header_open import detail_view_header, list_view_header, summarize_header

router = APIRouter()


@router.get("/runs")
def runs(limit: int = 50):
    items = repo.list_runs(limit)
    live = float((settings_repo.get_all() or {}).get("header_tape_joint_loss") or 0)
    for it in items:
        # Second pass keeps list chip pin while primary meters stay zeroed.
        it["result"] = list_view_header(it.get("result") or {}, None, live)
        it["header_summary"] = summarize_header(it["result"])
    return {"items": items}


@router.get("/runs/{run_id}")
def run(run_id: int):
    r = repo.get_run(run_id)
    if not r:
        raise HTTPException(404, "not found")
    live = float((settings_repo.get_all() or {}).get("header_tape_joint_loss") or 0)
    dims = {
        "width": r.get("window_width"),
        "height": r.get("window_height"),
        "fullness": r.get("window_fullness"),
        "fabric_width": r.get("fabric_width"),
        "hem_top": r.get("hem_top"),
        "hem_bottom": r.get("hem_bottom"),
    }
    r["result"] = detail_view_header(r.get("result") or {}, dims, live)
    r["header_summary"] = summarize_header(r["result"])
    return r
