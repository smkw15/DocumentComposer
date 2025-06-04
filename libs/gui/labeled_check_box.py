"""ラベル付きチェックボックスモジュール。"""
import tkinter as tk
from typing import Any
from libs.gui.basic.dc_frame import DCFrame
from libs.gui.basic.dc_label import DCLabel
from libs.gui.basic.dc_check_box import DCCheckBox
from libs.gui.basic.dc_font import DCFont


class LabeledCheckBox(DCFrame):
    """ラベル付きチェックボックス。"""

    def __init__(
        self,
        master: Any,
        label_text: str,
        value: bool = False,
        label_width: int = 0,
        label_height: int = 28,
        font: DCFont = None
    ):
        """コンストラクタ。

        NOTE: tkinterのチェックボックスは、標準でテキストが箱の右側に来る。
        このテキスト位置は、カスタマイズ出来ない。
        フレームでラップして、箱の左側にテキストを置く表示を実現する。

        Args:
            master (Any): マスター。
            label_text (str): ラベルに表示するテキスト。
            value (bool): 初期値。
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
        # チェックボックス
        self.check = DCCheckBox(self)
        self.check.checked.set(value)
        self.check.pack(side=tk.LEFT)

    def get_value(self) -> bool:
        """チェックの状態を取得する。

        Returns:
            bool: チェックの状態。
        """
        return self.check.checked.get()
