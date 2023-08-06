from __future__ import annotations

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    import xlpie.excel_wb as xlwb


class ExcelWS:
    def __init__(self, ws_name: Union[str, int], wb: xlwb.ExcelWB):
        self._wb = wb
        self._ws = wb._open_ws(ws_name)

    def _xl_range(self, range_str: str):
        return self._ws.Range(range_str)

    def xl_range(self, range_str: str):
        import xlpie.excel_range as xlrange

        return xlrange.ExcelRange(self, range_str)

    @property
    def name(self) -> str:
        return self._ws.Name

    @property
    def index(self) -> int:
        return self._ws.Index

    def insert_row(self, row: int):
        self._ws.Rows(row).Insert()

    def __rich__(self):
        name = f"[bold purple]{self.name}[/bold purple]"
        index = f"[bold]{self.index}[/bold]"
        wb = f"[bold blue]{self._wb.name}[/bold blue]"
        return f"{name} at index {index} in {wb}"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
