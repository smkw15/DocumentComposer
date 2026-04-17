"""DocumentComposer向けコンボボックスモジュール。"""
import customtkinter as ctk
from document_composer.gui.basic.dc_widget import DCWidget


class DCComboBox(ctk.CTkComboBox, DCWidget):
    """独自コンボボックスラッパークラス。"""
    pass
