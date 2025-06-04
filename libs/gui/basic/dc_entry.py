"""DocumentComposer向けエントリーモジュール。"""
import customtkinter as ctk


class DCEntry(ctk.CTkEntry):
    """独自エントリーラッパークラス。"""
    pass

    def set_value(self, value: str):
        """値のセット。

        Args:
            value (str): 値。
        """
        self.delete(0, ctk.END)
        self.insert(0, value)
