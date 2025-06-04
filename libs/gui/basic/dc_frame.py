"""DocumentComposer向けフレームモジュール。"""
import customtkinter as ctk
from typing import Any


class DCFrame(ctk.CTkFrame):
    """独自フレームラッパークラス。"""

    def __init__(self, master: Any, **kwargs):
        """コンストラクタ"""
        super().__init__(
            master,
            fg_color="transparent",
            **kwargs)
