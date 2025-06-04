"""コンポーザーモジュール。"""
import os
import pathlib
import shutil
from typing import Type, TypeVar
from libs.composable.base import Composable
from libs.composable.docx import Docx
from libs.composable.txt import Txt
from libs.config import Config
from libs.constants import (
    CONFIG_FILE_PATH,
    Extension
)

S = TypeVar("S", bound=Composable)
D = TypeVar("D", bound=Composable)


class Composer:
    """コンポーザー。"""

    def __init__(self, config: Config):
        """コンストラクタ。

        Args:
            config (Config): 構成情報。
        """
        self.config: Config = config

    @classmethod
    def from_dict(cls, d: dict) -> 'Composer':
        """辞書からインスタンスを生成する。

        Args:
            d (dict): 辞書。

        Returns:
            Converter: インスタンス。
        """
        return cls(Config.from_dict(d))

    @classmethod
    def from_yml(cls, config_file_path: str = CONFIG_FILE_PATH) -> 'Composer':
        """YAMLファイルからインスタンスを生成する。

        Args:
            config_file_path (str): 構成ファイルまでのパス。

        Return:
            Converter: インスタンス。
        """
        return cls(Config.from_yml(config_file_path))

    def compose_verbosely(
        self,
        src_root_dir_path: pathlib.Path,
        dest_root_dir_path: pathlib.Path,
        can_reset: bool,
        src_type: Type[S],
        dest_type: Type[D]
    ) -> list[Composable]:
        """コンポーズの冗長実行を行う。

        Args:
            src_root_dir_path (pathlib.Path): 入力元ルートディレクトリ。入力元の最も上層のディレクトリ。
            dest_root_dir_path (pathlib.Path): 出力先ルートディレクトリ。出力先の最も上層のディレクトリ。
            can_reset (bool): リセットフラグ。出力先ディレクトリの削除可否。
            src_type (Type[S]): 入力ファイルのファイル形式を示す型引数。
            dest_type (Type[D]): 出力ファイルのファイル形式を示す型引数。
        """
        ret = []
        # 出力先ディレクトリをセット
        self._reset_dest_dir(dest_root_dir_path, can_reset)
        # 入力元ディレクトリをすべて検索
        src_dir_pathes = self._find_pathes(src_root_dir_path, "**", self.config.ignorants)
        src_dir_pathes = [p for p in src_dir_pathes if p.is_dir()]
        for src_dir_path in src_dir_pathes:
            # 出力先ディレクトリのパスを導出
            dest_dir_path = pathlib.Path(str(src_dir_path.resolve()).replace(
                str(src_root_dir_path.resolve()),
                str(dest_root_dir_path.resolve())))
            # 出力ファイルのパスを導出
            if src_dir_path.resolve() == src_root_dir_path.resolve():
                dest_file_name = self.config.dest_root_file_nickname + "." + dest_type.get_extension()
                dest_file_path = dest_dir_path / dest_file_name
            else:
                dest_file_name = dest_dir_path.name + "." + dest_type.get_extension()
                dest_file_path = dest_dir_path / pathlib.Path(dest_file_name)
            # コンポーズ実行
            tpl = self.compose(src_dir_path, dest_file_path, False, src_type, dest_type)
            ret.append(tpl)
        return ret

    def compose(
        self,
        src_dir_path: pathlib.Path,
        dest_file_path: pathlib.Path,
        can_reset: bool,
        src_type: Type[S],
        dest_type: Type[D]
    ) -> tuple[list[Composable], Composable]:
        """コンポーズを実行する。

        Args:
            src_dir_path (pathlib.Path): 入力元ディレクリのパス。
            dest_file_path (pathlib.Path): 出力ファイルのパス。
            can_reset (bool): リセットフラグ。出力先ディレクトリの削除可否。
            src_type (Type[S]): 入力ファイルのファイル形式を示す型引数。
            dest_type (Type[D]): 出力ファイルのファイル形式を示す型引数。

        Returns:
            tuple[list[Composable], Composable]: 入力ファイルと出力ファイル。
        """
        # 出力先ディレクトリをリセット
        self._reset_dest_dir(dest_file_path.parent, can_reset)
        # ファイル検索
        src_file_pathes = self._find_pathes(src_dir_path, "*." + src_type.get_extension(), self.config.ignorants)
        # 読み込み
        src_files = self._read_files(src_file_pathes, src_type)
        # 集積
        dest_file = dest_type.new_file(dest_file_path, self.config)
        self._accumulate_lines(src_files, dest_file)
        # 書き込み
        dest_file.write_file()
        print("# Created:", str(dest_file_path))
        return (src_files, dest_file)

    def _find_pathes(
        self,
        dir_path: pathlib.Path,
        condition: str,
        ignorants: list[pathlib.Path]
    ) -> list[pathlib.Path]:
        ignorants_str = [ig.resolve() for ig in ignorants]  # 無視リストは絶対パスの文字列にする
        filted_pathes = [p for p in dir_path.rglob(condition) if p.resolve() not in ignorants_str]
        sorted_pathes = sorted(filted_pathes, key=lambda p: str(p.resolve()).split(os.sep))
        return sorted_pathes

    def _read_files(
        self,
        src_file_pathes: list[pathlib.Path],
        src_type: Type[S]
    ) -> list[Composable]:
        ret = []
        for src_file_path in src_file_pathes:
            src_file = src_type.new_file(src_file_path, self.config)
            src_file.read_file()
            ret.append(src_file)
            print("# Loaded:", str(src_file_path))
        return ret

    def _accumulate_lines(
        self,
        src_files: list[Composable],
        dest_files: Composable
    ) -> Composable:
        for i, src_file in enumerate(src_files):
            dest_files.append_lines(src_file.get_lines())
            if i != len(src_files) - 1:
                dest_files.append_lines(self.config.file_separator)
        return dest_files

    def _reset_dest_dir(self, dest_dir_path: pathlib.Path, can_reset: bool):
        if can_reset and dest_dir_path.exists():
            shutil.rmtree(str(dest_dir_path))
            print("# Removed:", str(dest_dir_path))
        if not dest_dir_path.exists():
            dest_dir_path.mkdir()
            print("# Created:", str(dest_dir_path))


T = TypeVar("T", bound=Composable)


def get_composable_type(ext: Extension) -> Type[T]:
    """ファイル種別からComposableの型情報を取得する。

    Args:
        ext (Extension): ファイル種別。

    Returns:
        Type[T]: Composableの型情報。
    """
    match(ext):
        case "txt":
            return Txt
        case "docx":
            return Docx
        case _:
            return Txt
