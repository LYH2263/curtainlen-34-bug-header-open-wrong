"""History open views for header tape meters.

历史回看必须钉住写入时的快照：无论列表摘要还是详情，帘头带开关、
带长、接头损耗都以 calc_runs.result_json 中固化的值为准，读取路径
不得清零、不得退化成窗宽、不得用实时默认损耗重算。
"""

from __future__ import annotations

from copy import deepcopy


def has_header(result: dict) -> bool:
    return bool(result.get("header_tape")) or result.get("header_tape_meters") is not None


def _pinned(result: dict) -> dict:
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if not has_header(out):
        return out
    # 开关可显示为开启；带长/损耗/主帘米一律保持写入快照，不做任何改写。
    out["header_tape"] = True
    return out


def list_view_header(result: dict, dims: dict | None = None, live_loss: float | None = None) -> dict:
    """List path: return the frozen snapshot as written."""
    return _pinned(result)


def detail_view_header(result: dict, dims: dict | None = None, live_loss: float | None = None) -> dict:
    """Detail path: return the frozen snapshot as written."""
    return _pinned(result)


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
    }
