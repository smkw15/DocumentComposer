"""Docxデータモデルモジュール。"""
import dataclasses
import pathlib
from docx import Document
from docx.shared import Pt, Mm
from libs.composable.base import Composable
from libs.constants import Extension
from libs.config import Config


@dataclasses.dataclass
class Docx(Composable):
    """docxファイルを表すデータモデル。

    Attributes:
        file_path (pathlib.Path): ファイルのパス。
        lines (Optional[list[str]]): ファイルコンテンツ。行のリスト。
    """
    file_path: pathlib.Path
    lines: list[str]
    config: Config

    @classmethod
    def new_file(cls, file_path: pathlib.Path, config: Config) -> 'Composable':
        """新しい空のインスタンスを生成する。

        Args:
            file_path (pathlib.Path): ファイルのパス。
            config (Config): 設定情報。

        Returns:
            Composable: インスタンス。
        """
        docx = Docx(file_path, [], config)
        return docx

    @classmethod
    def get_extension(cls) -> Extension:
        """拡張子を取得する。

        Returns:
            Extension: 拡張子。
        """
        return ".docx"

    def get_file_path(self) -> pathlib.Path:
        """ファイルのパスを取得する。

        Returns:
            pathlib.Path: ファイルのパス。
        """
        return self.file_path

    def get_lines(self) -> list[str]:
        """ファイルコンテンツを取得する。

        Returns:
            list[str]: ファイルコンテンツ。行のリスト。
        """
        return self.lines

    def append_lines(self, lines: list[str]):
        """ファイルコンテンツを追加する。

        Args:
            lines (list[str]): ファイルコンテンツ。行のリスト。
        """
        self.lines.extend(lines)

    def read_file(self):
        """ファイルを読み込む。"""
        pass

    def write_file(self):
        """ファイルを書き込み。"""
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
        for line in self.get_lines():
            paragraph = doc.add_paragraph(line, style=self.config.paragraph_style_name)
            paragraph.paragraph_format.space_before = Pt(self.config.paragraph_pt_before)
            paragraph.paragraph_format.space_after = Pt(self.config.paragraph_pt_after)
        doc.save(str(self.file_path))
