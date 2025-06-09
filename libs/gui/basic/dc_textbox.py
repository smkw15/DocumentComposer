"""DocumentComposer向けテキストボックスモジュール。"""
import customtkinter as ctk
from typing import Any, Optional, Union
from libs.gui.basic.dc_font import DCFont
from libs.gui.basic.dc_widget import DCWidget


class DCTextbox(ctk.CTkTextbox, DCWidget):
    """独自テキストボックスクラス。"""

    def __init__(
        self,
        master: Any,
        font: Optional[Union[tuple, DCFont]] = None,
        readonly: bool = False,
        **kwargs
    ):
        """コンストラクタ。"""
        super().__init__(
            master,
            font=DCFont() if font is None else font,
            **kwargs)
        self.readonly = readonly
        if self.readonly:
            self.configure(state="disabled")

    def set_value(self, value: str):
        """値のセット。

        Args:
            value (str): 値。
        """
        if self.readonly:
            self.configure(state="normal")
            self.delete("1.0", ctk.END)
            self.insert(ctk.END, value)
            self.configure(state="disabled")
        else:
            self.delete("1.0", ctk.END)
            self.insert(ctk.END, value)

    def insert_value(self, value: str):
        """値の挿入。

        Args:
            value (str): 値。
        """
        _value = value + "\n"
        if self.readonly:
            self.configure(state="normal")
            self.insert(ctk.END, _value)
            self.configure(state="disabled")
        else:
            self.insert(ctk.END, _value)
