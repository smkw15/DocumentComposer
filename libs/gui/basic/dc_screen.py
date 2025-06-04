"""DocumentComposer向けスクリーンモジュール。"""
import customtkinter as ctk


class DCScreen(ctk.CTk):
    """独自スクリーンのラッパークラス。"""

    def __init__(self, title: str = "", size: str = "", **kwargs):
        """コンストラクタ

        Args:
            title (str): タイトル。
            size (str): サイズ。`幅x高さ`で表記する。
        """
        super().__init__(
            fg_color="#ffffff",
            **kwargs)
        self.title(title)
        self.geometry(size)
