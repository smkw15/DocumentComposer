"""メインモジュール。"""
import argparse
import dataclasses
import pathlib
from libs.composer import Composer
from libs.constants import (
    SRC_ROOT_DIR_PATH,
    DEST_ROOT_DIR_PATH,
    DEST_ROOT_FILE_NAME,
    CONFIG_FILE_PATH
)
from libs.composable.txt import Txt
from libs.composable.docx import Docx


@dataclasses.dataclass
class ArgParams:
    """コマンドライン引数データモデル。

    Attribute:
        src_file_dir (str): 入力元ディレクトリまでのパス。
        dest_file_dir (str): 出力先ディレクトリまでのパス。
        dest_file_name (str): 出力ファイル名。
        config_file_path (str): 設定ファイルまでのパス。
        verbose (bool): 冗長出力を行うか。
    """
    src_dir_path: str
    dest_dir_path: str
    dest_file_name: str
    config_file_path: str
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
    parser.add_argument("--file", "-f", help="出力ファイル名。", default=DEST_ROOT_FILE_NAME, type=str)
    parser.add_argument("--config", "-c", help="設定ファイルまでのパス。", default=CONFIG_FILE_PATH, type=str)
    parser.add_argument("--verbose", "-v", help="冗長出力フラグ。ディレクトリごとに結合したファイルも出力する。", action="store_true")
    args = parser.parse_args()
    return ArgParams(
        src_dir_path=args.src,
        dest_dir_path=args.dest,
        dest_file_name=args.file,
        config_file_path=args.config,
        verbose=args.verbose
    )


def main():
    """メイン処理"""
    # 引数解析
    args = parse_args()
    # 変換器生成
    composer = Composer.from_yml(args.config_file_path)
    if args.verbose:
        composer.compose_verbosely(
            pathlib.Path(args.src_dir_path),
            pathlib.Path(args.dest_dir_path),
            pathlib.Path(args.dest_file_name),
            True,
            Txt,
            Docx
        )
    else:
        composer.compose(
            pathlib.Path(args.src_dir_path),
            pathlib.Path(args.dest_dir_path) / pathlib.Path(args.dest_file_name),
            True,
            Txt,
            Docx
        )


if __name__ == "__main__":
    main()
