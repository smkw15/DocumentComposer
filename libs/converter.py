"""txtファイル結合モジュール。"""
import glob
import os
import shutil
import pathlib
from functools import reduce
from docx import Document
from docx.shared import Pt, Mm
from libs.constants import (
    SRC_DIR_PATH,
    DEST_DIR_PATH,
    DEST_FILE_NAME,
    CONFIG_FILE_PATH
)
from libs.config import Config


class Converter:
    """文書ファイル形式変換器。"""

    def __init__(self, config: Config):
        """コンストラクタ。

        Args:
            config (Config): 設定情報。
        """
        self.config: Config = config

    @classmethod
    def from_dict(cls, d: dict) -> 'Converter':
        """辞書からインスタンスを生成する。

        Args:
            d (dict): 辞書。

        Returns:
            Converter: インスタンス。
        """
        return cls(Config.from_dict(d))

    @classmethod
    def from_yml(cls, config_file_path: str = CONFIG_FILE_PATH) -> 'Converter':
        """YAMLファイルからインスタンスを生成する。

        Args:
            config_file_path (str): 設定ファイルまでのパス。

        Return:
            Converter: インスタンス。
        """
        return cls(Config.from_yml(config_file_path))

    def conv_txt_to_docx(
        self,
        src_dir_path: str = SRC_DIR_PATH,
        dest_dir_path: str = DEST_DIR_PATH,
        dest_file_name: str = DEST_FILE_NAME
    ) -> str:
        """txtファイルをdocxファイルに結合する。

        Args:
            src_dir_path (str): 入力元ディレクリまでのパス。
            dest_dir_path (str): 出力先ディレクリまでのパス。
            dest_file_name (str): 出力ファイルのファイル名。

        Returns:
            str: 出力ファイルまでのパス。
        """
        # 対象ファイルの検索
        src_file_pathes = self._find_txt_file(src_dir_path, self.config.whitelst)
        print("# loaded:", "\n" + "\n".join(src_file_pathes))
        # 対象ファイルの内容を集積
        lines: list[str] = reduce(
            lambda lst, src_file_path: lst + self.config.file_separator + self._read_txt_file(src_file_path),
            src_file_pathes,
            list[str]()
        )
        lines = lines[len(self.config.file_separator):]  # 最初に余計なファイルセパレータが混じるので消す
        # docxに書き込み
        dest_file_path = self._write_docx_file(dest_dir_path, dest_file_name, lines)
        print("# created:", dest_file_path)
        return dest_file_path

    def _find_txt_file(self, dir_path: str, whitelst: list[str]) -> list[str]:
        """txtファイル検索。

        Args:
            dir_path (str): 検索対象ディレクトリまでのパス。
            whitelst (list[str]): ホワイトリスト。弾くファイルまでのパス。

        Returns:
            list[str]: txtファイルのパス文字列。
        """
        file_pathes: list[str] = glob.glob(os.path.join(dir_path, "**", "*.txt"), recursive=True)
        file_pathes = self._fileter_files(file_pathes, whitelst)
        return sorted(file_pathes, key=os.path.basename)

    def _fileter_files(self, file_pathes: list[str], whitelst: list[str]) -> list[str]:
        """ファイルをフィルタリングする。

        Args:
            file_pathes (list[str]): 検査対象のファイルまでのパス。
            whitelst (list[str]): ホワイトリスト。弾くファイルまでのパス。

        Returns:
            list[str]: フィルタリングした後のファイルのリスト。
        """
        # パス文字列は絶対パスに正規化してから検査
        file_pathes = [str(pathlib.Path(p).resolve()) for p in file_pathes]
        whitelst = [str(pathlib.Path(w).resolve()) for w in whitelst]
        return [p for p in file_pathes if p not in whitelst]

    def _read_txt_file(self, file_path: str) -> list[str]:
        """txtファイル読み込み。

        Args:
            file_path (str): txtファイルまでのパス。

        Returns:
            list[str]: txtファイルの全行。
        """
        with open(file_path, mode="r", encoding=self.config.encoding, newline=self.config.newline_char) as f:
            return f.read().strip(self.config.newline_char).split(self.config.newline_char)  # ファイルの先頭と末尾にある改行はトリム

    def _write_docx_file(self, dir_path: str, file_name: str, lines: list[str]) -> str:
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
        section.page_width = Mm(self.config.page_width_mm)
        section.page_height = Mm(self.config.page_height_mm)
        section.left_margin = Mm(self.config.left_margin_mm)
        section.top_margin = Mm(self.config.top_margin_mm)
        section.right_margin = Mm(self.config.right_margin_mm)
        section.bottom_margin = Mm(self.config.bottom_margin_mm)
        section.header_distance = Mm(self.config.header_distance_mm)
        section.footer_distance = Mm(self.config.footer_distance_mm)
        # ドキュメントに段落を追加
        for line in lines:
            paragraph = doc.add_paragraph(line, style=self.config.paragraph_style_name)
            paragraph.paragraph_format.space_before = Pt(self.config.paragraph_pt_before)
            paragraph.paragraph_format.space_after = Pt(self.config.paragraph_pt_after)
        # ドキュメント書き込み
        dest_file_path = os.path.join(dir_path, file_name)
        doc.save(dest_file_path)
        return dest_file_path
