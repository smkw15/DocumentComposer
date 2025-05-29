"""メインモジュール。"""
import argparse
import dataclasses
from libs.converter import Converter
from libs.constants import (
    SRC_DIR_PATH,
    DEST_DIR_PATH,
    DEST_FILE_NAME,
    CONFIG_FILE_PATH
)


@dataclasses.dataclass
class ArgParams:
    """コマンドライン引数データモデル。

    Attribute:
        src_file_dir (str): 入力元ディレクトリまでのパス。
        dest_file_dir (str): 出力先ディレクトリまでのパス。
        dest_file_name (str): 出力ファイル名。
        config_file_path (str): 設定ファイルまでのパス。
    """
    src_dir_path: str
    dest_dir_path: str
    dest_file_name: str
    config_file_path: str


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
    parser.add_argument("--src", "-s", help="入力元ディレクリまでのパス。", default=SRC_DIR_PATH, type=str)
    parser.add_argument("--dest", "-d", help="出力先ディレクトリまでのパス。", default=DEST_DIR_PATH, type=str)
    parser.add_argument("--file", "-f", help="出力ファイル名。", default=DEST_FILE_NAME, type=str)
    parser.add_argument("--config", "-c", help="設定ファイルまでのパス。", default=CONFIG_FILE_PATH, type=str)
    args = parser.parse_args()
    return ArgParams(
        src_dir_path=args.src,
        dest_dir_path=args.dest,
        dest_file_name=args.file,
        config_file_path=args.config
    )


def main():
    """メイン処理"""
    # 引数解析
    args = parse_args()

    # 変換
    converter = Converter.from_yml(args.config_file_path)
    converter.conv_txt_to_docx(
        args.src_dir_path,
        args.dest_dir_path,
        args.dest_file_name
    )


if __name__ == "__main__":
    main()
