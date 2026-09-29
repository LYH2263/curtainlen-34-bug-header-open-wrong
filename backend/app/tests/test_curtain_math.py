from app.engines.curtain_math import fabric_meters, header_tape_meters
import pytest

def test_living_room():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    assert r["panels"] == 5
    assert r["cut_height"] == 2.85
    assert r["meters"] == 14.25

def test_single_panel_narrow():
    r = fabric_meters(1.0, 2.0, 1.5, 0.0, 0.0, 2.8)
    assert r["panels"] == 1
    assert r["meters"] == 2.0

def test_header_tape_length_is_finished_width_plus_loss():
    # 成品宽 6.0 + 接头损耗 0.3
    assert header_tape_meters(6.0, 0.3) == 6.3

def test_header_tape_ceils_to_centimeter():
    # 2.2 * 2 = 4.4 成品宽，+0.001 -> 4.401，向上取厘米为 4.41
    assert header_tape_meters(4.401) == 4.41
    assert header_tape_meters(4.4) == 4.4

def test_header_tape_negative_loss_rejected():
    with pytest.raises(ValueError):
        header_tape_meters(6.0, -0.01)
