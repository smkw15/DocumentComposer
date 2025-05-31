"""Composerインターフェースモジュール。"""
import pathlib
from abc import ABCMeta, abstractmethod
from libs.constants import Extension
from libs.config import Config


class Composable(metaclass=ABCMeta):
    """Composerインターフェース。"""

    @classmethod
    @abstractmethod
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
    @abstractmethod
    def get_extension(cls) -> Extension:
        """拡張子を取得する。

        Returns:
            Extension: 拡張子。
        """
        pass

    @abstractmethod
    def get_file_path(self) -> pathlib.Path:
        """ファイルのパスを取得する。

        Returns:
            pathlib.Path: ファイルのパス。
        """
        pass

    @abstractmethod
    def get_lines(self) -> list[str]:
        """ファイルコンテンツを取得する。

        Returns:
            list[str]: ファイルコンテンツ。行のリスト。
        """
        pass

    @abstractmethod
    def append_lines(self, lines: list[str]):
        """ファイルコンテンツを追加する。

        Args:
            lines (list[str]): ファイルコンテンツ。行のリスト。
        """
        pass

    @abstractmethod
    def read_file(self):
        """ファイルを読み込む。"""
        pass

    @abstractmethod
    def write_file(self):
        """ファイルを書き込み。"""
        pass
