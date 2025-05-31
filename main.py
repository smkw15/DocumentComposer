"""メインモジュール。"""
import argparse
import dataclasses
import pathlib
from typing import Type, TypeVar
from libs.composer import Composer
from libs.constants import (
    SRC_ROOT_DIR_PATH,
    DEST_ROOT_DIR_PATH,
    CONFIG_FILE_PATH,
    FileKind
)
from libs.composable.txt import Txt
from libs.composable.docx import Docx
from libs.composable.base import Composable


@dataclasses.dataclass
class ArgParams:
    """コマンドライン引数データモデル。

    Attribute:
        src_file_dir (str): 入力元ディレクトリまでのパス。
        dest_file_dir (str): 出力先ディレクトリまでのパス。
        config_file_path (str): 設定ファイルまでのパス。
        src_file_kind (FileKind): 入力ファイルのファイル形式。
        dest_file_kind (FileKind): 出力ファイルのファイル形式。
        verbose (bool): 冗長出力を行うか。
    """
    src_dir_path: str
    dest_dir_path: str
    config_file_path: str
    src_file_kind: FileKind
    dest_file_kind: FileKind
    verbose: bool


def parse_args() -> ArgParams:
    """引数解析。

    コマンドライン引数を解析し、以下の情報を抽出する。
    - 入力元ディレクリまでのパス
    - 出力先ディレクトリまでのパス
    - 出力ファイル名
    - 設定ファイルまでのパス

    Return:
        Args: 引数解析結果。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", "-s", help="入力元ディレクリまでのパス。", default=SRC_ROOT_DIR_PATH, type=str)
    parser.add_argument("--dest", "-d", help="出力先ディレクトリまでのパス。", default=DEST_ROOT_DIR_PATH, type=str)
    parser.add_argument("--config", "-c", help="設定ファイルまでのパス。", default=CONFIG_FILE_PATH, type=str)
    parser.add_argument("-x", help="入力ファイルのファイル形式。", default="txt", type=str)
    parser.add_argument("-y", help="出力ファイルのファイル形式。", default="docx", type=str)
    parser.add_argument("--verbose", "-v", help="冗長出力フラグ。ディレクトリごとに結合したファイルも出力する。", action="store_true")
    args = parser.parse_args()
    return ArgParams(
        src_dir_path=args.src,
        dest_dir_path=args.dest,
        config_file_path=args.config,
        src_file_kind=args.x,
        dest_file_kind=args.y,
        verbose=args.verbose
    )


T = TypeVar("S", bound=Composable)


def get_composable_type(fileKind: FileKind) -> Type[T]:
    """ファイル種別からComposableの型情報を取得する。

    Args:
        fileKind (FileKind): ファイル種別。

    Returns:
        Type[T]: Composableの型情報。
    """
    match(fileKind):
        case "txt":
            return Txt
        case "docx":
            return Docx
        case _:
            return Txt


def main():
    """メイン処理"""
    # 引数解析
    args = parse_args()
    src_type: Type[T] = get_composable_type(args.src_file_kind)
    dest_type: Type[T] = get_composable_type(args.dest_file_kind)
    # 変換器生成
    composer = Composer.from_yml(args.config_file_path)
    if args.verbose:
        composer.compose_verbosely(
            pathlib.Path(args.src_dir_path),
            pathlib.Path(args.dest_dir_path),
            True,
            src_type,
            dest_type)
    else:
        dest_file_name = composer.config.dest_root_file_nickname + dest_type.get_extension()
        composer.compose(
            pathlib.Path(args.src_dir_path),
            pathlib.Path(args.dest_dir_path) / pathlib.Path(dest_file_name),
            True,
            src_type,
            dest_type)


if __name__ == "__main__":
    main()
