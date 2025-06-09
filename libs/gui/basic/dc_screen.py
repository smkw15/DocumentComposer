"""DocumentComposer向けスクリーンモジュール。"""
import customtkinter as ctk
from libs.gui.basic.dc_widget import DCWidget


class DCScreen(ctk.CTk, DCWidget):
    """独自スクリーンのラッパークラス。"""

    def __init__(self, title: str = "", size: str = "", **kwargs):
        """コンストラクタ。"""
        super().__init__(**kwargs)
        self.title(title)
        self.geometry(size)
