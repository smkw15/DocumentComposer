"""txtファイル結合モジュール。"""
import glob
import os
import shutil
from functools import reduce
from docx import Document
from docx.shared import Pt, Mm
from libs.constants import (
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

    def conv_txt_to_docx_verbosely(
        self,
        src_root_dir_path: str,
        dest_root_dir_path: str,
        dest_root_file_name: str,
        can_reset: bool
    ) -> list[str]:
        """txtファイルを階層ごとに結合してdocxファイルとして出力する。

        Args:
            src_root_dir_path (str): 入力元ルートディレクトリ。入力元の最も上層のディレクトリ。
            dest_root_dir_path (str): 出力先ルートディレクトリ。出力先の最も上層のディレクトリ。
            dest_root_file_name (str): 出力ルートファイル。すべての階層のtxtファイルの内容を含む。
            can_reset (bool): リセットフラグ。出力先ディレクトリの削除可否。
        """
        # リセットフラグが立っている時のみ既存の出力先をリセット
        if can_reset and os.path.exists(dest_root_dir_path):
            shutil.rmtree(dest_root_dir_path)
            print("# Remove:", dest_root_dir_path)

        # 与えればパス文字列は絶対パスにしておく
        src_root_dir_path = os.path.abspath(src_root_dir_path)
        dest_root_dir_path = os.path.abspath(dest_root_dir_path)

        # 対象入力ディレクトリを検索
        src_dir_pathes = self._find_dir(src_root_dir_path, self.config.ignorants)

        # 入力ディレクトリごとに処理
        for src_dir_path in src_dir_pathes:
            # 出力先ディレクトリを導出
            dest_dir_path = src_dir_path.replace(src_root_dir_path, dest_root_dir_path)
            # 出力ファイル名を導出
            dest_file_name = dest_root_file_name  \
                if src_dir_path == src_root_dir_path \
                else os.path.basename(dest_dir_path) + ".docx"
            # 変換実行
            self.conv_txt_to_docx(src_dir_path, dest_dir_path, dest_file_name, False)

    def conv_txt_to_docx(
        self,
        src_dir_path: str,
        dest_dir_path: str,
        dest_file_name: str,
        can_reset: bool
    ) -> str:
        """txtファイルを結合してdocxファイルとして出力する。

        Args:
            src_dir_path (str): 入力元ディレクリまでのパス。
            dest_dir_path (str): 出力先ディレクリまでのパス。
            dest_file_name (str): 出力ファイルのファイル名。
            can_reset (bool): リセットフラグ。出力先ディレクトリの削除可否。

        Returns:
            str: 出力ファイルまでのパス。
        """
        # リセットフラグが立っている時のみ既存の出力先をリセット
        if can_reset and os.path.exists(dest_dir_path):
            shutil.rmtree(dest_dir_path)
            print("# Remove:", dest_dir_path)

        # 対象ファイルを検索
        src_file_pathes = self._find_txt_file(src_dir_path, self.config.ignorants)
        print("# Loaded:", "\n" + "\n".join(src_file_pathes))

        # 対象ファイルの内容を集積
        lines: list[str] = reduce(
            lambda lst, src_file_path: lst + self.config.file_separator + self._read_txt_file(src_file_path),
            src_file_pathes,
            list[str]()
        )
        lines = lines[len(self.config.file_separator):]  # 最初に余計なファイルセパレータが混じるので消す

        # docxに書き込み
        dest_file_path = self._write_docx_file(dest_dir_path, dest_file_name, lines)
        print("# Created:", dest_file_path)
        return dest_file_path

    def _find_txt_file(self, dir_path: str, ignorants: list[str]) -> list[str]:
        """txtファイル検索。

        Args:
            dir_path (str): 検索対象ディレクトリまでのパス。
            ignorants (list[str]): 無視リスト。弾くファイルまでのパス。

        Returns:
            list[str]: txtファイルのパス文字列。
        """
        file_pathes: list[str] = glob.glob(os.path.join(dir_path, "**", "*.txt"), recursive=True)
        file_pathes = self._fileter_pathes(file_pathes, ignorants)
        return sorted(file_pathes, key=lambda p: p.split(os.sep))

    def _find_dir(self, dir_path: str, ignorants: list[str]) -> list[str]:
        """ディレクトリ検索。

        Args:
            dir_path (str): 検索対象ディレクトリまでのパス。
            ignorants (list[str]): 無視リスト。弾くディレクトリまでのパス。

        Returns:
            list[str]: ディレクトリのパス文字列。
        """
        dir_pathes: list[str] = glob.glob(os.path.join(dir_path, "**"), recursive=True)
        dir_pathes = [dir_path for dir_path in dir_pathes if os.path.isdir(dir_path)]
        dir_pathes = self._fileter_pathes(dir_pathes, ignorants)
        return sorted(dir_pathes, key=lambda p: p.split(os.sep))

    def _fileter_pathes(self, pathes: list[str], ignorants: list[str]) -> list[str]:
        """パスをフィルタリングする。

        Args:
            pathes (list[str]): 検査対象のパスのリスト。
            ignorants (list[str]): 無視リスト。弾くファイルまでのパス。

        Returns:
            list[str]: フィルタリングした後のパスのリスト。
        """
        # パス文字列は絶対パスに正規化してから検査
        pathes = [os.path.abspath(p) for p in pathes]
        ignorants = [os.path.abspath(w) for w in ignorants]
        return [p for p in pathes if p not in ignorants]

    def _read_txt_file(self, file_path: str) -> list[str]:
        """txtファイル読み込み。

        Args:
            file_path (str): txtファイルまでのパス。

        Returns:
            list[str]: txtファイルの全行。
        """
        encoding = self.config.encoding
        newline = self.config.newline_char
        with open(file_path, mode="r", encoding=encoding, newline=newline) as f:
            return f.read() \
                .strip(self.config.newline_char) \
                .split(self.config.newline_char)  # ファイルの先頭と末尾にある改行はトリム

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
        if not os.path.exists(dir_path):
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
        if os.path.exists(dest_file_path):
            os.remove(dest_file_path)
        doc.save(dest_file_path)
        return dest_file_path
