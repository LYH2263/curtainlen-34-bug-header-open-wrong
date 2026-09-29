"""端到端 HTTP 契约：写入 -> 列表摘要 / 详情回看 -> 默认损耗改大 -> 旧编号钉住。"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories import history

client = TestClient(app)


def test_write_then_list_and_detail_agree():
    r = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": True,
        "header_tape": True, "joint_loss": 0.3,
    })
    assert r.status_code == 200
    written = r.json()
    rid = written["run_id"]
    assert written["header_tape_meters"] == 6.3
    assert written["meters"] == 14.25

    # 详情进入该编号
    d = client.get(f"/api/runs/{rid}")
    assert d.status_code == 200
    detail = d.json()
    assert detail["result"]["header_tape"] is True
    assert detail["result"]["header_tape_meters"] == 6.3
    assert detail["result"]["header_tape_joint_loss"] == 0.3
    assert detail["result"]["meters"] == 14.25

    # 列表摘要进入该编号：同一组带长与主帘米
    lst = client.get("/api/runs").json()["items"]
    row = next(x for x in lst if x["id"] == rid)
    assert row["result"]["header_tape"] is True
    assert row["result"]["header_tape_meters"] == detail["result"]["header_tape_meters"] == 6.3
    assert row["result"]["header_tape_joint_loss"] == detail["result"]["header_tape_joint_loss"] == 0.3
    assert row["result"]["meters"] == detail["result"]["meters"] == 14.25


def test_old_run_pinned_after_default_loss_raised():
    r = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": True,
        "header_tape": True,  # 用当时默认损耗 0（每测例重建库）
    })
    rid = r.json()["run_id"]
    assert r.json()["header_tape_meters"] == 6.0

    # 褶量方案页改大默认损耗
    s = client.post("/api/settings", json={"key": "header_tape_joint_loss", "value": "1.0"})
    assert s.status_code == 200

    detail = client.get(f"/api/runs/{rid}").json()["result"]
    assert detail["header_tape"] is True
    assert detail["header_tape_joint_loss"] == 0.0
    assert detail["header_tape_meters"] == 6.0
    assert detail["meters"] == 14.25

    row = next(x for x in client.get("/api/runs").json()["items"] if x["id"] == rid)
    assert row["result"]["header_tape_meters"] == 6.0
    assert row["result"]["meters"] == 14.25


def test_negative_loss_rejected_without_row():
    before = len(client.get("/api/runs").json()["items"])
    r = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": True,
        "header_tape": True, "joint_loss": -0.01,
    })
    assert r.status_code == 422
    after = len(client.get("/api/runs").json()["items"])
    assert after == before


def test_bench_same_params_dry_rerun_matches_reopen():
    sv = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": True,
        "header_tape": True, "joint_loss": 0.3,
    }).json()
    rid = sv["run_id"]

    dry = client.get("/api/estimate?window_id=1&fabric_id=1&save=false&header_tape=true&joint_loss=0.3").json()
    reopened = client.get(f"/api/runs/{rid}").json()["result"]
    assert dry["header_tape_meters"] == reopened["header_tape_meters"] == 6.3
    assert dry["meters"] == reopened["meters"] == 14.25
