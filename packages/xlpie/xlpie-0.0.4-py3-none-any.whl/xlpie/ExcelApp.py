import shutil
import sys
from pathlib import Path
from typing import Union

import pythoncom
from rich import print
from win32com.client import gencache


class ExcelApp:
    def __init__(self):
        self._xl_app = self._EnsureDispatchEx("Excel.Application")

    def _open_wb(self, path: Path, password: str = None, read_only: bool = True):
        print(f"Opening file [bold blue]{path.stem}[/bold blue]")
        try:
            wb = self._xl_app.Workbooks.Open(path, False, read_only, None, password)
        except Exception as error:
            print(error.excepinfo(2))
        return wb

    def _open_ws(self, ws_name: Union[str, int], wb):
        try:
            ws = wb.Worksheets(ws_name)
        except Exception as error:
            print(f"Error accessing worksheet [bold blue]{ws_name}[/bold blue]")
            print(error)
            return None
        return ws

    # https://stackoverflow.com/a/36711595
    def _EnsureDispatchEx(self, clsid, new_instance=True):
        """Create a new COM instance and ensure cache is built,
        unset read-only gencache flag"""
        if new_instance:
            clsid = pythoncom.CoCreateInstanceEx(
                clsid, None, pythoncom.CLSCTX_SERVER, None, (pythoncom.IID_IDispatch,)
            )[0]
        if gencache.is_readonly:
            # fix for "freezed" app: py2exe.org/index.cgi/UsingEnsureDispatch
            gencache.is_readonly = False
            gencache.Rebuild()
        try:
            return gencache.EnsureDispatch(clsid)
        except (KeyError, AttributeError):  # no attribute 'CLSIDToClassMap'
            # something went wrong, reset cache
            shutil.rmtree(gencache.GetGeneratePath())
            for i in [i for i in sys.modules if i.startswith("win32com.gen_py.")]:
                del sys.modules[i]
            return gencache.EnsureDispatch(clsid)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._xl_app.Quit()
