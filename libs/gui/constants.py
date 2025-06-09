"""GUI関係の定数モジュール。"""
from typing import Literal

AppearanceMode = Literal["system", "light", "dark"]

FONT_FAMILY = "meiryo"
FONT_SIZE_STD = 11

ICON_PATH_ICO = "./resources/icon64.ico"
ICON_PATH_PNG = "./resources/icon64.png"

ROOT_SCREEN_TITLE = "Document Composer"
ROOT_SCREEN_WIDTH = 640
ROOT_SCREEN_HEIGHT = 360
ROOT_SCREEN_MIN_WIDTH = 400
ROOT_SCREEN_MIN_HEIGHT = 300
LABEL_SRC_DIR_TEXT = "入力元ディレクトリ:"
LABEL_SRC_EXT_TEXT = "入力ファイル形式:"
LABEL_DEST_DIR_TEXT = "出力先ディレクトリ:"
LABEL_DEST_EXT_TEXT = "出力ファイル形式:"
LABEL_CONFIG_TEXT = "構成ファイル:"
LABEL_VERBOSE_TEXT = "冗長出力:"
BUTTON_COMPOSE_TEXT = "実行"
BUTTON_REFFER_TEXT = "参照"
