"""独自ウィジット共通基盤モジュール。"""
import customtkinter as ctk
from libs.gui.constants import AppearanceMode
from abc import ABC


class DCWidget(ABC):
    """独自ウィジット共通基盤クラス。"""
    _appearance_mode: AppearanceMode = "system"

    @classmethod
    def set_appearance_mode(cls, appearance_mode: AppearanceMode):
        """アピアランスモード(テーマ)を切り替える。

        Args:
            appearance_mode (AppearanceMode): アピアランスモード。
        """
        cls._appearance_mode = appearance_mode
        ctk.set_appearance_mode(appearance_mode)
