"""DocumentComposer向けラベルモジュール。"""
import tkinter as tk
import customtkinter as ctk
from typing import Any, Union, Optional
from libs.gui.basic.dc_font import DCFont
from libs.gui.basic.dc_widget import DCWidget


class DCLabel(ctk.CTkLabel, DCWidget):
    """独自ラベルラッパークラス。"""

    def __init__(
        self,
        master: Any,
        text: str,
        width: int = 0,
        height: int = 28,
        font: Optional[Union[tuple, ctk.CTkFont]] = None,
        anchor: str = tk.W,
        **kwargs
    ):
        """コンストラクタ。"""
        super().__init__(
            master,
            width,
            height,
            text=text,
            anchor=anchor,
            bg_color="transparent",
            font=DCFont() if font is None else font,
            **kwargs)
