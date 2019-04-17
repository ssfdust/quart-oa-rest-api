from typing import Any
from pprint import pformat

def logfmt(data: Any) -> str:
    return "\n{}".format(pformat(data))
