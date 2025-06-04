"""メインモジュール。"""
import argparse
import dataclasses
import pathlib
from typing import Type
from libs.composer import (
    Composer,
    get_composable_type,
    T
)
from libs.constants import (
    SRC_ROOT_DIR_PATH,
    DEST_ROOT_DIR_PATH,
    CONFIG_FILE_PATH,
    SRC_FILE_EXT,
    DEST_FILE_EXT,
    VERBOSE,
    GUI,
    Extension
)
from libs.gui.root_screen import show_root_screen


@dataclasses.dataclass
class ArgParams:
    """コマンドライン引数データモデル。

    Attribute:
        src_file_dir (str): 入力元ディレクトリまでのパス。
        dest_file_dir (str): 出力先ディレクトリまでのパス。
        config_file_path (str): 構成ファイルまでのパス。
        src_file_kind (Extension): 入力ファイルのファイル形式。
        dest_file_kind (Extension): 出力ファイルのファイル形式。
        verbose (bool): 冗長出力を行うか。
        gui (bool): GUIを使用するか。
    """
    src_dir_path: str
    dest_dir_path: str
    config_file_path: str
    src_file_kind: Extension
    dest_file_kind: Extension
    verbose: bool
    gui: bool


def parse_args() -> ArgParams:
    """引数解析。

    コマンドライン引数を解析し、以下の情報を抽出する。
    - 入力元ディレクリまでのパス
    - 出力先ディレクトリまでのパス
    - 出力ファイル名
    - 構成ファイルまでのパス

    Return:
        Args: 引数解析結果。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", "-s", help="入力元ディレクリまでのパス。", default=SRC_ROOT_DIR_PATH, type=str)
    parser.add_argument("--dest", "-d", help="出力先ディレクトリまでのパス。", default=DEST_ROOT_DIR_PATH, type=str)
    parser.add_argument("--config", "-c", help="構成ファイルまでのパス。", default=CONFIG_FILE_PATH, type=str)
    parser.add_argument("-x", help="入力ファイルのファイル形式。", default=SRC_FILE_EXT, type=str)
    parser.add_argument("-y", help="出力ファイルのファイル形式。", default=DEST_FILE_EXT, type=str)
    parser.add_argument("--verbose", "-v", help="冗長出力を行うか。", action="store_false" if VERBOSE else "store_true")
    parser.add_argument("--gui", "-g", help="GUIを使用するか。", action="store_false" if GUI else "store_true")
    args = parser.parse_args()
    return ArgParams(
        src_dir_path=args.src,
        dest_dir_path=args.dest,
        config_file_path=args.config,
        src_file_kind=args.x,
        dest_file_kind=args.y,
        verbose=args.verbose,
        gui=args.gui)


def main():
    """メイン処理"""
    # 引数解析
    args = parse_args()
    # GUIで実行する場合は、GUIを呼び出して終了
    if args.gui:
        show_root_screen()
        return
    # 入出力対象の型を取得
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
        dest_file_name = composer.config.dest_root_file_nickname + "." + dest_type.get_extension()
        composer.compose(
            pathlib.Path(args.src_dir_path),
            pathlib.Path(args.dest_dir_path) / pathlib.Path(dest_file_name),
            True,
            src_type,
            dest_type)


if __name__ == "__main__":
    main()
