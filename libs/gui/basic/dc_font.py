"""DocumentComposer向けフォントモジュール。"""
import customtkinter as ctk
from libs.gui.constants import (
    FONT_FAMILY,
    FONT_SIZE_STD
)
from libs.gui.basic.dc_widget import DCWidget


class DCFont(ctk.CTkFont, DCWidget):
    """独自フォントラッパークラス。"""

    def __init__(
        self,
        family: str = FONT_FAMILY,
        size: int = FONT_SIZE_STD,
        **kwargs
    ):
        """コンストラクタ。"""
        super().__init__(family=family, size=size, **kwargs)
