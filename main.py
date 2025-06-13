"""メインモジュール。"""
import sys
import argparse
import dataclasses
import yaml
import logging
import logging.config
import pathlib
from libs.composer import exec_composer
from libs.constants import (
    SRC_ROOT_DIR_PATH,
    DEST_ROOT_DIR_PATH,
    CONFIG_FILE_PATH,
    SRC_FILE_EXT,
    DEST_FILE_EXT,
    Extension,
    UI,
    LOGGING_CONFIG_FILE_PATH,
    LOGGING_DIR
)
from libs.gui.root_screen import exec_composer_with_gui


class LoggingLoader(yaml.SafeLoader):
    """ロギング構成ファイル用の独自YAMLローダー。"""
    pass


def initialize_logging():
    """ロギングの初期化を行う。"""
    # ファイルハンドラー用の出力先を用意
    logging_dir_path = pathlib.Path(LOGGING_DIR)
    if not logging_dir_path.exists():
        logging_dir_path.mkdir()
    # ロギング構成ファイルから読みだしてロガー作成
    with open(LOGGING_CONFIG_FILE_PATH) as f:
        d = yaml.load(f, Loader=LoggingLoader)
    logging.config.dictConfig(d)


@dataclasses.dataclass
class ArgParams:
    """コマンドライン引数データモデル。

    Attribute:
        src_file_dir (str): 入力元ディレクトリまでのパス。
        dest_file_dir (str): 出力先ディレクトリまでのパス。
        config_file_path (str): 構成ファイルまでのパス。
        src_file_ext (Extension): 入力ファイルのファイル形式。
        dest_file_ext (Extension): 出力ファイルのファイル形式。
        verbose (bool): 冗長出力を行うか。
        ui (UI): UIに何を使用するか。
    """
    src_dir_path: str
    dest_dir_path: str
    config_file_path: str
    src_file_ext: Extension
    dest_file_ext: Extension
    verbose: bool
    ui: UI


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
    parser.add_argument("--verbose", "-v", help="冗長出力を行うか。", action="store_true")
    # 実行ファイルから呼び出された時はデフォルトUIをGUIにする
    if getattr(sys, "frozen", False):
        parser.add_argument("--ui", "-u", help="UIに何を使用するか。", default="gui", type=str)
    else:
        parser.add_argument("--ui", "-u", help="UIに何を使用するか。", default="cui", type=str)
    args = parser.parse_args()
    return ArgParams(
        src_dir_path=args.src,
        dest_dir_path=args.dest,
        config_file_path=args.config,
        src_file_ext=args.x,
        dest_file_ext=args.y,
        verbose=args.verbose,
        ui=args.ui)


def main():
    """メイン処理"""
    # ロギング初期化
    initialize_logging()
    # 引数解析
    args = parse_args()
    # GUIかコンポーザーを実行
    if args.ui == "gui":
        exec_composer_with_gui()
    else:
        exec_composer(
            args.src_dir_path,
            args.dest_dir_path,
            args.config_file_path,
            args.src_file_ext,
            args.dest_file_ext,
            args.verbose,
            "system")


if __name__ == "__main__":
    main()
