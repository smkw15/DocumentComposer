"""独自ウィジット共通基盤モジュール。"""
import customtkinter as ctk
from abc import ABC

from document_composer.gui.constants import AppearanceMode


class DCWidget(ABC):
    """独自ウィジット共通基盤クラス。"""
    _appearance_mode: AppearanceMode = "system"

    @classmethod
    def set_appearance_mode(cls, appearance_mode: AppearanceMode) -> None:
        """アピアランスモード(テーマ)を切り替える。

        Args:
            appearance_mode (AppearanceMode): アピアランスモード。
        """
        cls._appearance_mode = appearance_mode
        ctk.set_appearance_mode(appearance_mode)
