"""DocumentComposer向けチェックボックスモジュール。"""
import tkinter as tk
import customtkinter as ctk
from typing import Any, Optional, Union
from libs.gui.basic.dc_font import DCFont


class DCCheckBox(ctk.CTkCheckBox):
    """独自チェックボックスラッパークラス。"""

    def __init__(
        self,
        master: Any,
        text: str = "",
        font: Optional[Union[tuple, DCFont]] = None,
        **kwargs
    ):
        """独自チェックボックスラッパークラス。"""
        self.checked = tk.BooleanVar()
        super().__init__(
            master,
            text=text,
            font=DCFont() if font is None else font,
            variable=self.checked,
            **kwargs)
