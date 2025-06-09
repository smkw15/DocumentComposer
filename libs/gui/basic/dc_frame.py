"""DocumentComposer向けフレームモジュール。"""
import customtkinter as ctk
from typing import Any
from libs.gui.basic.dc_widget import DCWidget


class DCFrame(ctk.CTkFrame, DCWidget):
    """独自フレームラッパークラス。"""

    def __init__(self, master: Any, **kwargs):
        """コンストラクタ。"""
        super().__init__(
            master,
            fg_color="transparent",
            bg_color="transparent",
            **kwargs)
