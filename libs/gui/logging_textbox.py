"""ロギング表示テキストボックスモジュール。"""
import logging
from typing import Any
from libs.gui.basic.dc_textbox import DCTextbox


class GuiHandler(logging.Handler):
    """ロギングのGUI出力用ハンドラー。"""

    def __init__(self, textboxes: list['LoggingTextbox'] = []):
        """コンストラクタ。"""
        super().__init__()
        self.textboxes = textboxes

    def append_textbox(self, textbox: 'LoggingTextbox'):
        """テキストボックスを追加する。"""
        self.textboxes.append(textbox)

    def emit(self, record):
        """ロギング処理。"""
        record_formated = self.format(record)
        for textbox in self.textboxes:
            textbox.insert_value(record_formated)


class LoggingTextbox(DCTextbox):
    """ロギング表示テキストボックス。"""
    def __init__(self, master: Any, **kwargs):
        """コンストラクタ。"""
        super().__init__(master, readonly=True, height=2160, wrap="none", **kwargs)  # NOTE: 高さを無限に設定できないのでさしあたって4Kサイズにしておく
        logger = logging.getLogger("gui")
        for handler in logger.handlers:
            if isinstance(handler, GuiHandler):
                handler.append_textbox(self)
