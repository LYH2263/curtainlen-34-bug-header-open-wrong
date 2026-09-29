"""Open-path expectations for header tape: reads must return the frozen snapshot."""
from app.services.header_open import detail_view_header, list_view_header, summarize_header

# 成品宽 6.0（窗宽 3.0 × 褶倍 2.0）与窗宽不同；写入时带长 6.3、损耗 0.3。
RAW = {
    "header_tape": True,
    "header_tape_meters": 6.3,
    "header_tape_joint_loss": 0.3,
    "finished_width": 6.0,
    "meters": 14.25,
}


def test_list_keeps_frozen_length_and_loss():
    out = list_view_header(RAW, {"width": 3.0}, live_loss=1.0)
    assert out["header_tape"] is True
    # 不得清零、不得退化成窗宽、不得丢掉损耗只剩毛成品宽。
    assert out["header_tape_meters"] == 6.3
    assert out["header_tape_joint_loss"] == 0.3
    assert out["meters"] == 14.25


def test_detail_keeps_frozen_length_and_loss():
    out = detail_view_header(RAW, {"width": 3.0}, live_loss=1.0)
    assert out["header_tape"] is True
    # 即使实时默认损耗已改大，仍按写入快照，不得按窗宽或新损耗重算。
    assert out["header_tape_meters"] == 6.3
    assert out["header_tape_joint_loss"] == 0.3
    assert out["meters"] == 14.25


def test_list_and_detail_report_same_tape_and_meters():
    lv = list_view_header(RAW, {"width": 3.0})
    dv = detail_view_header(RAW, {"width": 3.0})
    assert lv["header_tape_meters"] == dv["header_tape_meters"] == 6.3
    assert lv["header_tape_joint_loss"] == dv["header_tape_joint_loss"] == 0.3
    assert lv["meters"] == dv["meters"] == 14.25
    assert summarize_header(dv)["header_tape_meters"] == 6.3


def test_without_header_untouched():
    raw = {"header_tape": False, "meters": 14.25}
    assert list_view_header(raw, {"width": 3.0})["meters"] == 14.25
    assert detail_view_header(raw, {"width": 3.0})["meters"] == 14.25
