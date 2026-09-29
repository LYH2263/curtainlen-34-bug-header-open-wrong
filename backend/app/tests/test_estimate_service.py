import pytest
from fastapi import HTTPException
from app.services import estimate_service
from app.engines.curtain_math import fabric_meters
from app.repositories import history, settings_repo


def test_header_tape_off_matches_legacy_main_curtain():
    # 关闭帘头带：主帘 panels / meters 必须等于改造前同窗同布
    legacy = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    r = estimate_service.run_estimate(1, 1, save=False, note="")
    assert r["panels"] == legacy["panels"]
    assert r["meters"] == legacy["meters"]
    assert r["header_tape"] is False
    assert "header_tape_meters" not in r


def test_preview_and_save_with_header_tape():
    # 预览：带长 = 成品宽 6.0 + 损耗 0.3，向上取厘米后 6.3，与主帘 meters 分列
    pv = estimate_service.run_estimate(1, 1, save=False, note="", header_tape=True, joint_loss=0.3)
    assert pv["run_id"] is None
    assert pv["header_tape_meters"] == 6.3
    assert pv["header_tape_joint_loss"] == 0.3
    assert pv["meters"] == 14.25  # 主帘布米不受影响

    # 保存：固化开关、损耗、带长与布米
    sv = estimate_service.run_estimate(1, 1, save=True, note="", header_tape=True, joint_loss=0.3)
    rid = sv["run_id"]
    assert rid is not None
    frozen = history.get_run(rid)["result"]
    assert frozen["header_tape"] is True
    assert frozen["header_tape_joint_loss"] == 0.3
    assert frozen["header_tape_meters"] == 6.3
    assert frozen["meters"] == 14.25


def test_negative_loss_fails_order_without_history_row():
    before = len(history.list_runs(1000))
    with pytest.raises(HTTPException) as ei:
        estimate_service.run_estimate(1, 1, save=True, note="", header_tape=True, joint_loss=-0.01)
    assert ei.value.status_code == 422
    after = len(history.list_runs(1000))
    assert after == before


def test_default_loss_used_when_omitted():
    settings_repo.set_value("header_tape_joint_loss", "0.2")
    r = estimate_service.run_estimate(1, 1, save=False, note="", header_tape=True)
    assert r["header_tape_joint_loss"] == 0.2
    assert r["header_tape_meters"] == 6.2


def test_old_run_keeps_frozen_length_after_default_changes():
    # 按编号打开仍是当初带长：默认损耗事后修改不能改写旧编号
    settings_repo.set_value("header_tape_joint_loss", "0.2")
    sv = estimate_service.run_estimate(1, 1, save=True, note="", header_tape=True)
    rid = sv["run_id"]
    assert sv["header_tape_meters"] == 6.2

    settings_repo.set_value("header_tape_joint_loss", "1.0")
    frozen = history.get_run(rid)["result"]
    assert frozen["header_tape_joint_loss"] == 0.2
    assert frozen["header_tape_meters"] == 6.2
