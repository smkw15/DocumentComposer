"""定数モジュール。"""
from typing import Literal

# 改行コード/改行文字
NewlineCode = Literal["LF", "CRLF", "CR"]
NewlineChar = Literal["\n", "\r\n", "\r"]

# 対応ファイル種別・対応ファイル拡張子
FileKind = Literal["txt", "docx"]
Extension = Literal[".txt", ".docx"]

# コマンドライン引数初期値
SRC_ROOT_DIR_PATH: str = "./docs/src"
DEST_ROOT_DIR_PATH: str = "./docs/dest"
CONFIG_FILE_PATH: str = "./config.yml"
SRC_EXTENSION: FileKind = "txt"
DEST_EXTENSION: FileKind = "docx"
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
