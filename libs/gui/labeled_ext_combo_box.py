"""ラベル付きファイル拡張子選択用モジュール。"""
import tkinter as tk
from typing import Any
from libs.gui.basic.dc_frame import DCFrame
from libs.gui.basic.dc_label import DCLabel
from libs.gui.basic.dc_combo_box import DCComboBox
from libs.gui.basic.dc_font import DCFont
from libs.constants import Extension

# 選択肢
OPTIONS: list[Extension] = [
    "txt",
    "docx"
]


class LabeledExtComboBox(DCFrame):
    """ラベル付きファイル拡張子選択用コンボボックス。"""

    def __init__(
        self,
        master: Any,
        label_text: str,
        value: Extension = None,
        label_width: int = 0,
        label_height: int = 28,
        font: DCFont = None
    ):
        """コンストラクタ。

        Args:
            master (Any): マスター。
            label_text (str): ラベルに表示するテキスト。
            value (Extension): 初期値。
            label_width (int): ラベルの幅。
            label_height (int): ラベルの高さ。
            font (DcFont): フォント。
        """
        # フレーム設定
        super().__init__(master)
        # ラベル
        self.label = DCLabel(
            self,
            label_text,
            width=label_width,
            height=label_height,
            font=font)
        self.label.pack(side=tk.LEFT)
        # コンボボックス
        self.combo = DCComboBox(
            self,
            values=OPTIONS,
            state="readonly",
            width=100)
        self.combo.set(value)
        self.combo.pack(side=tk.LEFT)

    def get_value(self) -> Extension:
        """選択されている値を取得する。

        Returns:
            Extension: 選択されている値。
        """
        return self.combo.get()
