"""DocumentComposer向けフォントモジュール。"""
import customtkinter as ctk
from libs.gui.constants import (
    FONT_FAMILY,
    FONT_SIZE_STD
)


class DCFont(ctk.CTkFont):
    """独自フォントラッパークラス。"""

    def __init__(
        self,
        family: str = FONT_FAMILY,
        size: int = FONT_SIZE_STD,
        **kwargs
    ):
        """コンストラクタ。

        Args:
            family (str): フォントファミリー。
            size (int): フォントサイズ。
        """
        super().__init__(
            family=family,
            size=size,
            **kwargs)
