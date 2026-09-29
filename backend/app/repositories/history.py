import json
from datetime import datetime, timezone
from app.db import connect

def insert_run(window_id, fabric_id, result, note=""):
    c = connect()
    try:
        cur = c.execute(
            "INSERT INTO calc_runs(window_id,fabric_id,result_json,note,created_at) VALUES (?,?,?,?,?)",
            (window_id, fabric_id, json.dumps(result, ensure_ascii=False), note, datetime.now(timezone.utc).isoformat()),
        )
        c.commit()
        return int(cur.lastrowid)
    finally:
        c.close()

_SELECT = """SELECT r.*, w.name window_name, f.name fabric_name,
                    w.width window_width, w.height window_height, w.fullness window_fullness,
                    f.fabric_width fabric_width, f.hem_top hem_top, f.hem_bottom hem_bottom
             FROM calc_runs r
             LEFT JOIN windows w ON w.id=r.window_id
             LEFT JOIN fabrics f ON f.id=r.fabric_id"""


def _row_to_dict(row):
    d = dict(row)
    # 写入即快照：读路径原样返回，不按窗宽或当前默认损耗重算。
    d["result"] = json.loads(d.pop("result_json"))
    return d


def get_run(run_id):
    c = connect()
    try:
        row = c.execute(_SELECT + " WHERE r.id=?", (run_id,)).fetchone()
        return _row_to_dict(row) if row else None
    finally:
        c.close()

def list_runs(limit=50):
    c = connect()
    try:
        rows = c.execute(_SELECT + " ORDER BY r.id DESC LIMIT ?", (limit,)).fetchall()
        return [_row_to_dict(row) for row in rows]
    finally:
        c.close()
