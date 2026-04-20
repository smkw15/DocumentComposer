"""ラベル付きディレクトリ入力用モジュール。"""
import tkinter as tk
import tkinter.filedialog
import pathlib

from typing import Any

from document_composer.gui.basic.dc_frame import DCFrame
from document_composer.gui.basic.dc_label import DCLabel
from document_composer.gui.basic.dc_entry import DCEntry
from document_composer.gui.basic.dc_button import DCButton
from document_composer.gui.basic.dc_font import DCFont
from document_composer.gui.constants import (
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
        font: DCFont | None = None
    ):
        """コンストラクタ。

        Args:
            master (Any): マスター。
            label_text (str): ラベルに表示するテキスト。
            initial_path (str): パス指定する時の初期位置。
            label_width (int): ラベルの幅。
            label_height (int): ラベルの高さ。
            font (DcFont | None): フォント。
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
        self.entry = DCEntry(self, width=120)
        self.entry.set_value(initial_path)
        self.entry.pack(side=tk.LEFT, expand=True, fill="x")
        # ボタン
        self.button = DCButton(
            self,
            text=BUTTON_REFFER_TEXT,
            command=self._on_click_button,
            width=60)
        self.button.pack(side=tk.LEFT, padx=5)

    def get_value(self) -> str | Any:
        """入力値を取得する。

        Returns:
            str: 入力値。
        """
        return self.entry.get()

    def _on_click_button(self) -> None:
        path = tkinter.filedialog.askdirectory(
            mustexist=True,
            initialdir=pathlib.Path(self.initial_path).resolve())
        if path is not None and path != "":
            self.entry.set_value(path)
