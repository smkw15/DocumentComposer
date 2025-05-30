"""定数モジュール。"""
from typing import Literal

# コマンドライン引数初期値
SRC_ROOT_DIR_PATH = "./docs/src"
DEST_ROOT_DIR_PATH = "./docs/dest"
DEST_ROOT_FILE_NAME = "__all_in_one__.docx"
CONFIG_FILE_PATH = "./config.yml"
VERBOSE = False

# 設定情報初期値
WHITELST = []
FILE_SEPARATOR = ['', "＊", '']
PARAGRAPH_STYLE_NAME = 'Body Text'
PARAGRAPH_PT_BEFORE = 0
PARAGRAPH_PT_AFTER = 0
PAGE_WIDTH_MM = 210
PAGE_HEIGHT_MM = 297
LEFT_MARGIN_MM = 19.0
TOP_MARGIN_MM = 19.0
RIGHT_MARGIN_MM = 19.0
BOTTOM_MARGIN_MM = 19.0
HEADER_DISTANCE_MM = 19.0
FOOTER_DISTANCE_MM = 19.0
ENCODING = "utf-8"
NEWLINE_CODE = "CRLF"

# 改行コード/改行文字
NewlineCode = Literal["LF", "CRLF", "CR"]
NewlineChar = Literal["\n", "\r\n", "\r"]
