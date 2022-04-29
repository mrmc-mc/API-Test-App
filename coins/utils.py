import re
from decimal import Decimal


def SplitPairs(pairs):
    sell = re.search(r'^(\w+)(IRT|USDT)$', pairs.upper())
    buy = re.search(r'^(IRT|USDT)(\w+)$', pairs.upper())
    if sell or buy:
        m = sell or buy
        return m.group(1), m.group(2)
    else:
        return False


def float2decimal(number: float, place: int) -> float:
    slices = str(Decimal(number)).split(".")
    slices.append("0")
    f2d_num = float(slices[0] + "." + slices[1][:place])
    return f2d_num
