import xlpie.ExcelWS


class ExcelRange:
    def __init__(self, ws: xlpie.ExcelWS.ExcelWS, range_str: str):
        self._ws = ws
        self._range = ws._xl_range(range_str)

    @property
    def value(self):
        return self._range.Value

    @value.setter
    def value(self, value):
        self._range.Value = value
