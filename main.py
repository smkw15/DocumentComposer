import glob
import os
import shutil
from functools import reduce
from docx import Document
from constants import (
    SRC_DIR_PATH,
    DEST_DIR_PATH,
    DEST_FILE_NAME,
    SRC_NEWLINE,
    SRC_ENCODIG
)

def _find_txt_file(dir_path: str):
    """txtファイル検索"""
    file_pathes: list[str] = glob.glob(os.path.join(dir_path, "**", "*.txt"), recursive=True)
    return sorted(file_pathes, key=os.path.basename)

def _read_txt_file(file_path: str) -> list[str]:
    """txtファイル読み込み"""
    with open(file_path, mode="r", encoding=SRC_ENCODIG, newline=SRC_NEWLINE) as f:
        return f.readlines()

def _write_docx_file(dir_path: str, file_name: str, lines: list[str]):
    """docxファイル書き込み"""
    # 出力先の準備
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # 既に存在していたら削除
    os.mkdir(dir_path)
    # ファイル書き込み
    doc = Document()
    for line in lines:
        doc.add_paragraph(line)
    doc.save(os.path.join(dir_path, file_name))

def main():
    """メイン処理"""
    # 対象ファイルの検索
    src_file_pathes = _find_txt_file(SRC_DIR_PATH)
    # 対象ファイルの内容を集積
    lines: list[str] = reduce(lambda lst, src_file_path:  lst + _read_txt_file(src_file_path), src_file_pathes, [])
    # docxに書き込み
    _write_docx_file(DEST_DIR_PATH, DEST_FILE_NAME, lines)

if __name__ == "__main__":
    main()