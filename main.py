"""メインモジュール。"""
import glob
import os
import shutil
from functools import reduce
from docx import Document
from docx.shared import Pt, Mm
from constants import (
    SRC_DIR_PATH,
    DEST_DIR_PATH,
    DEST_FILE_NAME,
    FILE_SEPARATOR,
    PARAGRAPH_STYLE_NAME,
    PARAGRAPH_PT_BEFORE,
    PARAGRAPH_PT_AFTER,
    PAGE_WIDTH_MM,
    PAGE_HEIGHT_MM,
    LEFT_MARGIN_MM,
    TOP_MARGIN_MM,
    RIGHT_MARGIN_MM,
    BOTTOM_MARGIN_MM,
    HEADER_DISTANCE_MM,
    FOOTER_DISTANCE_MM,
    NEWLINE,
    ENCODING,
)


def _find_txt_file(dir_path: str) -> list[str]:
    """txtファイル検索。

    Args:
        dir_path (str): 入力元ディレクトリまでのパス。

    Returns:
        list[str]: txtファイルのパス文字列。
    """
    file_pathes: list[str] = glob.glob(os.path.join(dir_path, "**", "*.txt"), recursive=True)
    return sorted(file_pathes, key=os.path.basename)


def _read_txt_file(file_path: str) -> list[str]:
    """txtファイル読み込み。

    Args:
        file_path (str): txtファイルまでのパス。

    Returns:
        list[str]: txtファイルの全行。
    """
    with open(file_path, mode="r", encoding=ENCODING, newline=NEWLINE) as f:
        return f.read().strip(NEWLINE).split(NEWLINE)  # ファイルの先頭と末尾にある改行はトリム


def _write_docx_file(dir_path: str, file_name: str, lines: list[str]) -> str:
    """docxファイル書き込み。

    Args:
        dir_path (str): 出力先ディレクトリまでのパス。
        file_name (str): 出力ファイルのファイル名。
        lines (list[str]): 出力する行。

    Returns:
        str: 出力ファイルまでのパス。
    """
    # 出力先の準備
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # 既に存在していたら削除
    os.mkdir(dir_path)
    # ドキュメント用意
    doc = Document()
    section = doc.sections[0]
    section.page_width = Mm(PAGE_WIDTH_MM)
    section.page_height = Mm(PAGE_HEIGHT_MM)
    section.left_margin = Mm(LEFT_MARGIN_MM)
    section.top_margin = Mm(TOP_MARGIN_MM)
    section.right_margin = Mm(RIGHT_MARGIN_MM)
    section.bottom_margin = Mm(BOTTOM_MARGIN_MM)
    section.header_distance = Mm(HEADER_DISTANCE_MM)
    section.footer_distance = Mm(FOOTER_DISTANCE_MM)
    # ドキュメントに段落を追加
    for line in lines:
        paragraph = doc.add_paragraph(line, style=PARAGRAPH_STYLE_NAME)
        paragraph.paragraph_format.space_before = Pt(PARAGRAPH_PT_BEFORE)
        paragraph.paragraph_format.space_after = Pt(PARAGRAPH_PT_AFTER)
    # ドキュメント書き込み
    dest_file_path = os.path.join(dir_path, file_name)
    doc.save(dest_file_path)
    return dest_file_path


def main():
    """メイン処理"""
    # 対象ファイルの検索
    src_file_pathes = _find_txt_file(SRC_DIR_PATH)
    print("# loaded:", "\n" + "\n".join(src_file_pathes))
    # 対象ファイルの内容を集積
    lines: list[str] = reduce(lambda lst, src_file_path: lst + FILE_SEPARATOR + _read_txt_file(src_file_path), src_file_pathes, list[str]())
    lines = lines[len(FILE_SEPARATOR):]  # 最初に余計なファイルセパレータが混じるので消す
    # docxに書き込み
    dest_file_path = _write_docx_file(DEST_DIR_PATH, DEST_FILE_NAME, lines)
    print("# created:", dest_file_path)


if __name__ == "__main__":
    main()
