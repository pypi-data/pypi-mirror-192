from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    import xlpie.excel_app as xlapp


class ExcelWB:
    def __init__(
        self,
        xl_app: xlapp.ExcelApp,
        path: Path,
        password: str = None,
        read_only: bool = True,
    ):
        self._xl_app = xl_app
        self._wb = xl_app._open_wb(path, password, read_only)

    def _open_ws(self, ws_name: Union[str, int]):
        return self._xl_app._open_ws(ws_name, self._wb)

    def open_ws(self, ws_name: str):
        import xlpie.excel_ws as xlws

        return xlws.ExcelWS(ws_name, self)

    def save(self):
        self._wb.Save()

    def close(self, save_changes: bool = False):
        self._wb.Close(save_changes)

    @property
    def name(self):
        return self._wb.Name

    @property
    def path(self):
        return self._wb.Path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        sheets = self._wb.Sheets
        for sheet in sheets:
            yield self.open_ws(sheet.Name)

    def __rich__(self):
        name = f"[bold purple]{self.name}[/bold purple]"
        path = f"[bold blue]{self.path}[/bold blue]"
        return f"{name} located at in {path}"
