import os
import tempfile
import pytest

_tmp = tempfile.mkdtemp(prefix="curtainlen_test_")
os.environ["DATA_DIR"] = _tmp

from app import seed  # noqa: E402

DB_FILE = os.path.join(_tmp, "app.db")

@pytest.fixture(autouse=True)
def fresh_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    seed.init_db()
    yield
