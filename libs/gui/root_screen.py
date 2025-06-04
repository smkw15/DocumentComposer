"""ルートスクリーンモジュール。"""
import tkinter as tk
import dataclasses
import yaml
import pathlib
from typing import Type
from libs.gui.constants import (
    ROOT_SCREEN_TITLE,
    ROOT_SCREEN_SIZE,
    LABEL_SRC_DIR_TEXT,
    LABEL_SRC_EXT_TEXT,
    LABEL_DEST_DIR_TEXT,
    LABEL_DEST_EXT_TEXT,
    LABEL_CONFIG_TEXT,
    LABEL_VERBOSE_TEXT,
    BUTTON_COMPOSE_TEXT,
    ICON_PATH
)
from libs.gui.basic.dc_button import DCButton
from libs.gui.basic.dc_screen import DCScreen
from libs.gui.basic.dc_frame import DCFrame
from libs.gui.labeled_dir_entry import LabeledDirEntry
from libs.gui.labeled_ext_combo_box import LabeledExtComboBox
from libs.gui.labeled_file_entry import LabeledFileEntry
from libs.gui.labeled_check_box import LabeledCheckBox
from libs.constants import (
    Extension,
    SCREEN_FILE_PATH,
    ENCODING,
    NEWLINE_CODE,
    SRC_ROOT_DIR_PATH,
    DEST_ROOT_DIR_PATH,
    CONFIG_FILE_PATH,
    SRC_FILE_EXT,
    DEST_FILE_EXT,
    VERBOSE,
)
from libs.util import get_newline_char
from libs.composer import (
    Composer,
    get_composable_type,
    T
)


class ScreenLoader(yaml.SafeLoader):
    """スクリーンファイル用の独自YAMLローダー。"""
    pass


class ScreenDumper(yaml.SafeDumper):
    """スクリーンファイル用の独自YAMLダンパー。"""
    pass


@dataclasses.dataclass
class RootScreenModel:
    """ルートウィンドウのデータモデル。

    Attributes:
        src_dir_path (str): 入力元ディレクトリまでのパス。
        src_file_ext (Extension): 入力ファイルの拡張子。
        dest_dir_path (str): 出力先ディレクトリまでのパス。
        dest_file_ext (Extension): 出力ファイルの拡張子。
        config_file_path (str): 構成ファイルまでのパス。
        verbose (bool): 冗長出力を行うか。
    """
    src_dir_path: str
    src_file_ext: Extension
    dest_dir_path: str
    dest_file_ext: Extension
    config_file_path: str
    verbose: bool

    @classmethod
    def from_yml(cls, model_file_path: str = SCREEN_FILE_PATH) -> 'RootScreenModel':
        """YAMLファイルからインスタンスを生成する。

        Args:
            model_file_path (str): スクリーンモデルファイルまでのパス。

        Returns:
            RootScreenModel: インスタンス。
        """
        if pathlib.Path(model_file_path).exists():
            with open(model_file_path, mode="r", encoding=ENCODING, newline=get_newline_char(NEWLINE_CODE)) as f:
                d = yaml.load(f, Loader=ScreenLoader)
                if d is None:
                    d = {}
        else:
            d = {}
        return cls(
            src_dir_path=d["src_dir_path"] if "src_dir_path" in d else SRC_ROOT_DIR_PATH,
            src_file_ext=d["src_file_ext"] if "src_file_ext" in d else SRC_FILE_EXT,
            dest_dir_path=d["dest_dir_path"] if "dest_dir_path" in d else DEST_ROOT_DIR_PATH,
            dest_file_ext=d["dest_file_ext"] if "dest_file_ext" in d else DEST_FILE_EXT,
            config_file_path=d["config_file_path"] if "config_file_path" in d else CONFIG_FILE_PATH,
            verbose=d["verbose"] if "verbose" in d else VERBOSE)

    def dump_yml(self, model_file_path: str = SCREEN_FILE_PATH):
        """YAMLファイルにインスタンスをダンプする。

        Args:
            model_file_path (str): スクリーンモデルファイルまでのパス。
        """
        with open(model_file_path, mode="w", encoding=ENCODING, newline=get_newline_char(NEWLINE_CODE)) as f:
            yaml.dump(self.to_dict(), f, Dumper=ScreenDumper, sort_keys=False)

    def to_dict(self) -> dict:
        """インスタンスを辞書に変換する。

        Returns:
            dict: 辞書。
        """
        return {
            "src_dir_path": self.src_dir_path,
            "src_file_ext": self.src_file_ext,
            "dest_dir_path": self.dest_dir_path,
            "dest_file_ext": self.dest_file_ext,
            "config_file_path": self.config_file_path,
            "verbose": self.verbose
        }


class RootScreen(DCScreen):
    """ルートウィンドウ"""

    def __init__(self, model: RootScreenModel):
        """初期化。

        表示物のインスタンスを生成する。

        Args:
            model (RootScreenModel): 入力値を格納して内外とやりとりするデータモデル。
        """
        # ウィンドウ設定
        super().__init__(
            title=ROOT_SCREEN_TITLE,
            size=ROOT_SCREEN_SIZE)
        self.model = model
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        # ボディフレーム
        self.frame_body = DCFrame(self)
        self.frame_body.pack(anchor=tk.CENTER, pady=10)
        # 入力元ディレクトリ入力欄
        self.entry_src_dir = LabeledDirEntry(
            master=self.frame_body,
            label_text=LABEL_SRC_DIR_TEXT,
            initial_path=model.src_dir_path,
            label_width=120)
        self.entry_src_dir.pack(side=tk.TOP, pady=5)
        # 入力ファイル形式選択欄
        self.combo_src_ext = LabeledExtComboBox(
            master=self.frame_body,
            label_text=LABEL_SRC_EXT_TEXT,
            value=model.src_file_ext,
            label_width=120)
        self.combo_src_ext.pack(side=tk.TOP, anchor=tk.W, pady=5)
        # 出力先ディレクトリ入力欄
        self.entry_dest_dir = LabeledDirEntry(
            master=self.frame_body,
            label_text=LABEL_DEST_DIR_TEXT,
            initial_path=model.dest_dir_path,
            label_width=120)
        self.entry_dest_dir.pack(side=tk.TOP, pady=5)
        # 出力ファイル形式選択欄
        self.combo_dest_ext = LabeledExtComboBox(
            master=self.frame_body,
            label_text=LABEL_DEST_EXT_TEXT,
            value=model.dest_file_ext,
            label_width=120)
        self.combo_dest_ext.pack(side=tk.TOP, anchor=tk.W, pady=5)
        # 構成ファイル選択欄
        self.entry_config_file = LabeledFileEntry(
            master=self.frame_body,
            label_text=LABEL_CONFIG_TEXT,
            initial_path=model.config_file_path,
            file_types=[("構成ファイル", "*.yml;*.yaml")],
            label_width=120)
        self.entry_config_file.pack(side=tk.TOP, anchor=tk.W, pady=5)
        # 冗長出力チェックボックス
        self.check_verbose = LabeledCheckBox(
            master=self.frame_body,
            label_text=LABEL_VERBOSE_TEXT,
            value=model.verbose,
            label_width=120)
        self.check_verbose.pack(side=tk.TOP, anchor=tk.W, pady=5)
        # コンポーズボタン
        self.button_compose = DCButton(
            self.frame_body,
            text=BUTTON_COMPOSE_TEXT,
            command=self._on_click_button_submit,
            width=120)
        self.button_compose.pack(side=tk.TOP, anchor=tk.W, pady=5)

    def _on_click_button_submit(self):
        # ユーザ設定値をモデルに抽出
        self.model.src_dir_path = self.entry_src_dir.get_value()
        self.model.src_file_ext = self.combo_src_ext.get_value()
        self.model.dest_dir_path = self.entry_dest_dir.get_value()
        self.model.dest_file_ext = self.combo_dest_ext.get_value()
        self.model.config_file_path = self.entry_config_file.get_value()
        self.model.verbose = self.check_verbose.get_value()
        # コンポーズ実行
        src_type: Type[T] = get_composable_type(self.model.src_file_ext)
        dest_type: Type[T] = get_composable_type(self.model.dest_file_ext)
        composer = Composer.from_yml(self.model.config_file_path)
        if self.model.verbose:
            composer.compose_verbosely(
                pathlib.Path(self.model.src_dir_path),
                pathlib.Path(self.model.dest_dir_path),
                True,
                src_type,
                dest_type)
        else:
            dest_file_name = composer.config.dest_root_file_nickname + "." + dest_type.get_extension()
            composer.compose(
                pathlib.Path(self.model.src_dir_path),
                pathlib.Path(self.model.dest_dir_path) / pathlib.Path(dest_file_name),
                True,
                src_type,
                dest_type)

    def _on_closing(self):
        self.model.dump_yml()  # モデルをファイルに保存
        self.destroy()  # 閉じる処理を明示的に呼ばないと閉じない


def show_root_screen():
    """ルートウィンドウを表示する。"""
    model = RootScreenModel.from_yml()
    root = RootScreen(model)
    photo = tk.PhotoImage(file=ICON_PATH)  # FIXME: アイコンが表示されない
    root.iconphoto(False, photo)
    root.mainloop()
    # TODO: スクリーンのサイズに合わせて入力欄が伸びるようように調整
    # TODO: 実行ボタンの大きさを少し短く
    # TODO: ログ表示領域を表示
    # TODO: 処理完了時にスナックバーでも出す
    # TODO: ツールチップを出す
    # TODO: GUIについてREADMEの記載
    # TODO: customtkinterについてライセンス情報の更新
