"""定数モジュール。"""

# ディレクトリ名・ファイル名
SRC_DIR_PATH = ".\\docs\\src"
DEST_DIR_PATH = ".\\docs\\dest"
DEST_FILE_NAME = "__all_in_one__.docx"

# 文字列結合規則
FILE_SEPARATOR = ['', "＊", '']  # default:['', "＊", '']

# ドキュメントのスタイル
PARAGRAPH_STYLE_NAME = 'Body Text'  # default:'Body Text'
# 行間の幅
PARAGRAPH_PT_BEFORE = 0  # default:0
PARAGRAPH_PT_AFTER = 0  # default:0
# ページサイズ
PAGE_WIDTH_MM = 210  # default:210
PAGE_HEIGHT_MM = 297  # default:297
# ページ余白
LEFT_MARGIN_MM = 19.0  # default:25.4
TOP_MARGIN_MM = 19.0  # default:25.4
RIGHT_MARGIN_MM = 19.0  # default:25.4
BOTTOM_MARGIN_MM = 19.0  # default:25.4
# ヘッダー/フッターの幅
HEADER_DISTANCE_MM = 19.0  # default:12.7
FOOTER_DISTANCE_MM = 19.0  # default:12.7

# 一般規則
ENCODIG = "utf-8"
NEWLINE = "\r\n"
