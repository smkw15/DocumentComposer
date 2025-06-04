"""ラベル付きディレクトリ入力用モジュール。"""
import tkinter as tk
import tkinter.filedialog
import pathlib
from typing import Any
from libs.gui.basic.dc_frame import DCFrame
from libs.gui.basic.dc_label import DCLabel
from libs.gui.basic.dc_entry import DCEntry
from libs.gui.basic.dc_button import DCButton
from libs.gui.basic.dc_font import DCFont
from libs.gui.constants import (
    BUTTON_REFFER_TEXT
)


class LabeledDirEntry(DCFrame):
    """ラベル付きディレクトリ入力用エントリー。"""

    def __init__(
        self,
        master: Any,
        label_text: str,
        initial_path: str,
        label_width: int = 0,
        label_height: int = 28,
        font: DCFont = None
    ):
        """コンストラクタ。

        Args:
            master (Any): マスター。
            label_text (str): ラベルに表示するテキスト。
            initial_path (str): パス指定する時の初期位置。
            label_width (int): ラベルの幅。
            label_height (int): ラベルの高さ。
            font (DcFont): フォント。
        """
        # フレーム設定
        super().__init__(master)
        self.initial_path = initial_path
        # ラベル
        self.label = DCLabel(
            self,
            label_text,
            width=label_width,
            height=label_height,
            font=font)
        self.label.pack(side=tk.LEFT)
        # エントリー
        self.entry = DCEntry(self, width=700)
        self.entry.set_value(initial_path)
        self.entry.pack(side=tk.LEFT)
        # ボタン
        self.button = DCButton(
            self,
            text=BUTTON_REFFER_TEXT,
            command=self._on_click_button,
            width=60)
        self.button.pack(side=tk.LEFT, padx=5)

    def get_value(self) -> str:
        """入力値を取得する。

        Returns:
            str: 入力値。
        """
        return self.entry.get()

    def _on_click_button(self):
        path = tkinter.filedialog.askdirectory(
            mustexist=True,
            initialdir=pathlib.Path(self.initial_path).resolve())
        if path is not None and path != "":
            self.entry.set_value(path)
