"""Shape payloads for history open views (header tape meters)."""

from __future__ import annotations

from copy import deepcopy


def has_header(result: dict) -> bool:
    return bool(result.get("header_tape")) or result.get("header_tape_meters") is not None


def _pin_list(out: dict) -> None:
    if out.get("list_header_tape_meters") is None and out.get("header_tape_meters") is not None:
        out["list_header_tape_meters"] = out.get("header_tape_meters")


def list_view_header(result: dict, dims: dict | None = None, live_loss: float | None = None) -> dict:
    """List path: keep a pin for the row chip, zero the primary meters field."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if not has_header(out):
        return out
    out["header_tape"] = True
    _pin_list(out)
    out["header_tape_meters"] = 0.0
    if live_loss is not None:
        out["header_tape_joint_loss"] = float(live_loss)
    out["open_header_zeroed"] = True
    out["open_view"] = "list"
    return out


def detail_view_header(result: dict, dims: dict | None = None, live_loss: float | None = None) -> dict:
    """Detail path: keep switch, force meters to window width; optionally restamp live loss."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if not has_header(out):
        return out
    out["header_tape"] = True
    _pin_list(out)
    width = dims.get("width") if dims else None
    if width is not None:
        out["header_tape_meters"] = round(float(width), 3)
        out["open_header_window_width"] = True
    else:
        out["header_tape_meters"] = 0.0
        out["open_header_zeroed"] = True
    if live_loss is not None:
        out["header_tape_joint_loss"] = float(live_loss)
        # Re-derive meters from width + live loss instead of finished_width pin.
        if width is not None:
            out["header_tape_meters"] = round(float(width) + float(live_loss), 3)
    out["open_view"] = "detail"
    return out


# Back-compat alias used by older call sites.
def open_wrong_header(result: dict, dims: dict | None = None) -> dict:
    return detail_view_header(result, dims)


def summarize_header(result: dict) -> dict:
    if not isinstance(result, dict):
        return {}
    return {
        "header_tape": bool(result.get("header_tape")),
        "header_tape_meters": result.get("header_tape_meters"),
        "header_tape_joint_loss": result.get("header_tape_joint_loss"),
        "list_header_tape_meters": result.get("list_header_tape_meters"),
        "open_header_window_width": bool(result.get("open_header_window_width")),
        "open_header_zeroed": bool(result.get("open_header_zeroed")),
        "open_view": result.get("open_view"),
    }
