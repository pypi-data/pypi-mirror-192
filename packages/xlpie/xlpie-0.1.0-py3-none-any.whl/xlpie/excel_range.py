from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import xlpie.excel_ws as xlws


class ExcelRange:
    def __init__(self, ws: xlws.ExcelWS, range_str: str):
        self._ws = ws
        self._range = ws._xl_range(range_str)

    @property
    def value(self):
        return self._range.Value

    @value.setter
    def value(self, value):
        self._range.Value = value
