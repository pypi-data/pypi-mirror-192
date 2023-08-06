from importlib import metadata
from typing import Literal

BLANK: int = 0x2f3136
"""A colour exactly like an embed from discord"""

MAX_NUMBER: int = 82
"""How many seal images there are"""

__version__: str = metadata.version("randseal")
"""The version of the package"""