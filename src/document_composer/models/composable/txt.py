"""Txtデータモデルモジュール。"""
import dataclasses
import pathlib

from document_composer.models.composable.protocol import Composable
from document_composer.constants import Extension
from document_composer.config import Config
from document_composer.util import (
    integrate_newline_code,
    join_lines,
    split_to_lines,
    strip_empty_line
)


@dataclasses.dataclass
class Txt:
    """txtファイルを表すデータモデル。

    Attributes:
        file_path (pathlib.Path): ファイルのパス。
        lines (Optional[list[str]]): ファイルコンテンツ。行のリスト。
    """
    file_path: pathlib.Path
    lines: list[str]
    config: Config

    @classmethod
    def new_file(cls, file_path: pathlib.Path, config: Config) -> Composable:
        """新しい空のインスタンスを生成する。

        Args:
            file_path (pathlib.Path): ファイルのパス。
            config (Config): 構成情報。

        Returns:
            Txt: インスタンス。
        """
        txt = Txt(file_path, [], config)
        return txt

    @classmethod
    def get_extension(cls) -> Extension:
        """拡張子を取得する。

        Returns:
            Extension: 拡張子。
        """
        return "txt"

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

    def append_lines(self, lines: list[str]) -> None:
        """ファイルコンテンツを追加する。

        Args:
            lines (list[str]): ファイルコンテンツ。行のリスト。
        """
        self.lines.extend(lines)

    def read_file(self) -> None:
        """ファイルを読み込む。"""
        with open(str(self.file_path), mode="r", encoding=self.config.encoding) as f:
            content = f.read()
            content = integrate_newline_code(content)  # 改行コード統一
            content = strip_empty_line(content)  # 先頭と末尾の空行をトリミング
            lines = split_to_lines(content)  # システム用の改行コードで分割
            self.append_lines(lines)

    def write_file(self) -> None:
        """ファイルを書き込み。"""
        with open(str(self.file_path), mode="w", encoding=self.config.encoding, newline=self.config.newline_char_dest) as f:
            content = join_lines(self.get_lines())  # システム用の改行コードで結合
            f.write(content)
