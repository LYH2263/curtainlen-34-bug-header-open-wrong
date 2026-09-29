import math

def ceil_units(v: float) -> int:
    return int(math.ceil(float(v) - 1e-9))

def ceil_cm(v: float) -> float:
    return math.ceil(float(v) * 100 - 1e-9) / 100
