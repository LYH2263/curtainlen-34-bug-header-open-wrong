from fastapi import APIRouter, HTTPException
from app.repositories import history as repo
from app.services.header_open import summarize_header

router = APIRouter()


@router.get("/runs")
def runs(limit: int = 50):
    items = repo.list_runs(limit)
    for it in items:
        # 列表摘要直接取自写入快照，与详情同一组带长与主帘米。
        it["header_summary"] = summarize_header(it.get("result") or {})
    return {"items": items}


@router.get("/runs/{run_id}")
def run(run_id: int):
    r = repo.get_run(run_id)
    if not r:
        raise HTTPException(404, "not found")
    r["header_summary"] = summarize_header(r.get("result") or {})
    return r
