"""DocumentComposer向けボタンモジュール。"""
import customtkinter as ctk
from typing import Any, Union, Optional, Callable
from libs.gui.basic.dc_font import DCFont
from libs.gui.basic.dc_widget import DCWidget


class DCButton(ctk.CTkButton, DCWidget):
    """独自ボタンラッパークラス。"""

    def __init__(
        self,
        master: Any,
        text: str,
        command: Callable[[], Any],
        font: Optional[Union[tuple, DCFont]] = None,
        **kwargs
    ):
        """コンストラクタ。"""
        super().__init__(
            master,
            text=text,
            command=command,
            bg_color="transparent",
            font=DCFont(weight="bold") if font is None else font,
            **kwargs)
