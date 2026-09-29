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

def _dims(row) -> dict:
    return {
        "width": row["window_width"] if "window_width" in row.keys() else None,
        "height": row["window_height"] if "window_height" in row.keys() else None,
        "fullness": row["window_fullness"] if "window_fullness" in row.keys() else None,
        "fabric_width": row["fabric_width"] if "fabric_width" in row.keys() else None,
        "hem_top": row["hem_top"] if "hem_top" in row.keys() else None,
        "hem_bottom": row["hem_bottom"] if "hem_bottom" in row.keys() else None,
    }


def _row_to_dict(row):
    d = dict(row)
    # 原样返回写入快照；帘头带带长/损耗/主帘米不做任何读取期改写。
    d["result"] = json.loads(d.pop("result_json"))
    return d


def get_run(run_id):
    c = connect()
    try:
        row = c.execute(
            """SELECT r.*, w.name window_name, f.name fabric_name,
                   w.width window_width, w.height window_height, w.fullness window_fullness,
                   f.fabric_width fabric_width, f.hem_top hem_top, f.hem_bottom hem_bottom
            FROM calc_runs r
            LEFT JOIN windows w ON w.id=r.window_id LEFT JOIN fabrics f ON f.id=r.fabric_id
            WHERE r.id=?""", (run_id,)).fetchone()
        if not row:
            return None
        return _row_to_dict(row)
    finally:
        c.close()

def list_runs(limit=50):
    c = connect()
    try:
        rows = c.execute(
            """SELECT r.*, w.name window_name, f.name fabric_name,
                   w.width window_width, w.height window_height, w.fullness window_fullness,
                   f.fabric_width fabric_width, f.hem_top hem_top, f.hem_bottom hem_bottom
            FROM calc_runs r
            LEFT JOIN windows w ON w.id=r.window_id LEFT JOIN fabrics f ON f.id=r.fabric_id
            ORDER BY r.id DESC LIMIT ?""", (limit,)).fetchall()
        return [_row_to_dict(row) for row in rows]
    finally:
        c.close()
