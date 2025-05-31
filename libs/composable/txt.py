"""Txtデータモデルモジュール。"""
import dataclasses
import pathlib
from libs.composable.base import Composable
from libs.constants import Extension
from libs.config import Config


@dataclasses.dataclass
class Txt(Composable):
    """txtファイルを表すデータモデル。

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
            config (Config): 構成情報。

        Returns:
            Composable: インスタンス。
        """
        txt = Txt(file_path, [], config)
        return txt

    @classmethod
    def get_extension(cls) -> Extension:
        """拡張子を取得する。

        Returns:
            Extension: 拡張子。
        """
        return ".txt"

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
        with open(str(self.file_path), mode="r", encoding=self.config.encoding, newline=self.config.newline_char) as f:
            lines = f.read().strip(self.config.newline_char).split(self.config.newline_char)  # ファイルの先頭と末尾にある改行はトリム
            self.append_lines(lines)

    def write_file(self):
        """ファイルを書き込み。"""
        with open(str(self.file_path), mode="w", encoding=self.config.encoding, newline=self.config.newline_char) as f:
            f.write(self.config.newline_char.join(self.get_lines()))
