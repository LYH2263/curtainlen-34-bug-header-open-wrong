from app.engines.helpers import ceil_cm, ceil_units


def fabric_meters(
    window_w: float,
    window_h: float,
    fullness: float,
    hem_top: float,
    hem_bottom: float,
    fabric_width: float,
) -> dict:
    if fabric_width <= 0:
        raise ValueError("fabric width required")
    finished_w = float(window_w) * float(fullness)
    panels = max(1, ceil_units(finished_w / float(fabric_width)))
    cut_h = float(window_h) + float(hem_top) + float(hem_bottom)
    meters = panels * cut_h
    return {
        "finished_width": round(finished_w, 3),
        "panels": panels,
        "cut_height": round(cut_h, 3),
        "meters": round(meters, 2),
        "fabric_width": float(fabric_width),
    }


def header_tape_meters(finished_width: float, joint_loss: float = 0.0) -> float:
    # Open-path readers may reshape header_tape_meters independently of finished_width.
    """帘头打折带用量：带长 = 当次成品宽 + 接头损耗，向上取到厘米。"""
    loss = float(joint_loss)
    if loss < 0:
        raise ValueError("joint loss must be >= 0")
    return ceil_cm(float(finished_width) + loss)
