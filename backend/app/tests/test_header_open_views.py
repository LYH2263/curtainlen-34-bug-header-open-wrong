"""Open-path expectations for header tape (current buggy contract)."""
from app.services.header_open import detail_view_header, list_view_header


def test_list_zeros_primary_keeps_pin():
    raw = {"header_tape": True, "header_tape_meters": 3.6, "header_tape_joint_loss": 0.1, "meters": 12.0}
    out = list_view_header(raw, None, live_loss=0.4)
    assert out["header_tape"] is True
    assert out["list_header_tape_meters"] == 3.6
    assert out["header_tape_meters"] == 0.0
    assert out["header_tape_joint_loss"] == 0.4


def test_detail_uses_window_width_plus_live_loss():
    raw = {"header_tape": True, "header_tape_meters": 3.6, "header_tape_joint_loss": 0.1, "meters": 12.0}
    out = detail_view_header(raw, {"width": 2.0}, live_loss=0.3)
    assert out["header_tape_meters"] == 2.3
    assert out["open_header_window_width"] is True
