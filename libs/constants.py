"""定数モジュール。"""
from typing import Literal

# 改行コード/改行文字
NewlineCode = Literal["LF", "CRLF", "CR"]
NewlineChar = Literal["\n", "\r\n", "\r"]

# 対応ファイル形式(拡張子)
Extension = Literal["txt", "docx"]

# ユーザインターフェース
UI = Literal["gui", "cui"]

# コマンドライン引数初期値
SRC_ROOT_DIR_PATH: str = "./docs/src"
DEST_ROOT_DIR_PATH: str = "./docs/dest"
CONFIG_FILE_PATH: str = "./config.yml"
SRC_FILE_EXT: Extension = "txt"
DEST_FILE_EXT: Extension = "txt"
VERBOSE = False

# 構成情報初期値
IGNORANTS: list[str] = []
DEST_ROOT_FILE_NICKNAME = "__all_in_one__"
FILE_SEPARATOR: list[str] = ['', "＊", '']
PARAGRAPH_STYLE_NAME: str = 'Body Text'
PARAGRAPH_PT_BEFORE: float = 0.0
PARAGRAPH_PT_AFTER: float = 0.0
PAGE_WIDTH_MM: float = 210
PAGE_HEIGHT_MM: float = 297
LEFT_MARGIN_MM: float = 19.0
TOP_MARGIN_MM: float = 19.0
RIGHT_MARGIN_MM: float = 19.0
BOTTOM_MARGIN_MM: float = 19.0
HEADER_DISTANCE_MM: float = 19.0
FOOTER_DISTANCE_MM: float = 19.0
ENCODING: str = "utf-8"
NEWLINE_CODE: str = "LF"

# GUIデータ保存先
SCREEN_FILE_PATH: str = "./.user.yml"

# ロギング構成ファイル
LoggerName = Literal["system", "gui"]
LOGGING_CONFIG_FILE_PATH: str = "./logging.yml"
LOGGING_DIR: str = "./.logs"
