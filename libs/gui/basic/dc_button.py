"""DocumentComposer向けボタンモジュール。"""
import customtkinter as ctk
from typing import Any, Union, Optional, Tuple, Callable
from libs.gui.constants import (
    BUTTON_FG_COLOR,
    BUTTON_HOVER_COLOR,
)
from libs.gui.basic.dc_font import DCFont


class DCButton(ctk.CTkButton):
    """独自ボタンラッパークラス。"""

    def __init__(
        self,
        master: Any,
        text: str,
        command: Callable[[], Any],
        fg_color: Optional[Union[str, Tuple[str, str]]] = BUTTON_FG_COLOR,
        hover_color: Optional[Union[str, Tuple[str, str]]] = BUTTON_HOVER_COLOR,
        font: Optional[Union[tuple, DCFont]] = None,
        **kwargs
    ):
        """コンストラクタ。"""
        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color,
            font=DCFont(weight="bold") if font is None else font,
            **kwargs)
