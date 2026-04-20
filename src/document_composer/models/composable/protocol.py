"""Composerインターフェースモジュール。"""
import pathlib

from typing import Protocol, runtime_checkable

from document_composer.constants import Extension
from document_composer.config import Config


@runtime_checkable
class Composable(Protocol):
    """Composerインターフェース。"""

    @classmethod
    def new_file(cls, file_path: pathlib.Path, config: Config) -> 'Composable':
        """新しい空のインスタンスを生成する。

        Args:
            file_path (pathlib.Path): ファイルのパス。
            config (Config): 構成情報。

        Returns:
            Composable: インスタンス。
        """
        pass

    @classmethod
    def get_extension(cls) -> Extension:
        """拡張子を取得する。

        Returns:
            Extension: 拡張子。
        """
        pass

    def get_file_path(self) -> pathlib.Path:
        """ファイルのパスを取得する。

        Returns:
            pathlib.Path: ファイルのパス。
        """
        pass

    def get_lines(self) -> list[str]:
        """ファイルコンテンツを取得する。

        Returns:
            list[str]: ファイルコンテンツ。行のリスト。
        """
        pass

    def append_lines(self, lines: list[str]) -> None:
        """ファイルコンテンツを追加する。

        Args:
            lines (list[str]): ファイルコンテンツ。行のリスト。
        """
        pass

    def read_file(self) -> None:
        """ファイルを読み込む。"""
        pass

    def write_file(self) -> None:
        """ファイルを書き込み。"""
        pass
