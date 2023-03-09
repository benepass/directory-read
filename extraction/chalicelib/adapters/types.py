from typing import Any, NewType

# dataclassses.dataclass does not export an interface
DataClass = NewType("DataClass", Any)
