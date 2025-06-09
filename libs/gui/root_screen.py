"""ルートスクリーンモジュール。"""
import tkinter as tk
import dataclasses
import yaml
import pathlib
import platform
from libs.gui.constants import (
    ROOT_SCREEN_TITLE,
    ROOT_SCREEN_WIDTH,
    ROOT_SCREEN_HEIGHT,
    ROOT_SCREEN_MIN_WIDTH,
    ROOT_SCREEN_MIN_HEIGHT,
    LABEL_SRC_DIR_TEXT,
    LABEL_SRC_EXT_TEXT,
    LABEL_DEST_DIR_TEXT,
    LABEL_DEST_EXT_TEXT,
    LABEL_CONFIG_TEXT,
    LABEL_VERBOSE_TEXT,
    BUTTON_COMPOSE_TEXT,
    ICON_PATH_ICO,
    ICON_PATH_PNG
)
from libs.gui.basic.dc_widget import DCWidget
from libs.gui.basic.dc_button import DCButton
from libs.gui.basic.dc_screen import DCScreen
from libs.gui.basic.dc_frame import DCFrame
from libs.gui.labeled_dir_entry import LabeledDirEntry
from libs.gui.labeled_ext_combo_box import LabeledExtComboBox
from libs.gui.labeled_file_entry import LabeledFileEntry
from libs.gui.labeled_check_box import LabeledCheckBox
from libs.gui.logging_textbox import LoggingTextbox
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
from libs.composer import exec_composer


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
        super().__init__(title=ROOT_SCREEN_TITLE, size=f"{ROOT_SCREEN_WIDTH}x{ROOT_SCREEN_HEIGHT}")
        self.minsize(ROOT_SCREEN_MIN_WIDTH, ROOT_SCREEN_MIN_HEIGHT)
        self.model = model
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        if platform.system() == "Windows":
            self.iconbitmap(ICON_PATH_ICO)
        else:
            self.icon_photo_image = tk.PhotoImage(file=ICON_PATH_PNG)
            self.wm_iconphoto(False, self.icon_photo_image)
        # ボディ領域フレーム
        self.frame_body = DCFrame(self)
        self.frame_body.pack(side=tk.TOP, anchor=tk.N, padx=10, pady=10, expand=True, fill="x")
        # 入力元ディレクトリ入力欄
        self.entry_src_dir = LabeledDirEntry(
            master=self.frame_body,
            label_text=LABEL_SRC_DIR_TEXT,
            initial_path=model.src_dir_path,
            label_width=120)
        self.entry_src_dir.pack(side=tk.TOP, anchor=tk.W, pady=5, expand=True, fill="x")
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
        self.entry_dest_dir.pack(side=tk.TOP, anchor=tk.W, pady=5, expand=True, fill="x")
        # 出力ファイル形式選択欄
        self.combo_dest_ext = LabeledExtComboBox(
            master=self.frame_body,
            label_text=LABEL_DEST_EXT_TEXT,
            value=model.dest_file_ext,
            label_width=120)
        self.combo_dest_ext.pack(side=tk.TOP, anchor=tk.W, pady=5)
        # 構成ファイル入力欄
        self.entry_config_file = LabeledFileEntry(
            master=self.frame_body,
            label_text=LABEL_CONFIG_TEXT,
            initial_path=model.config_file_path,
            file_types=[("構成ファイル", "*.yml"), ("構成ファイル", "*.yaml")],
            label_width=120)
        self.entry_config_file.pack(side=tk.TOP, anchor=tk.W, pady=5, expand=True, fill="x")
        # 冗長出力チェックボックス
        self.check_verbose = LabeledCheckBox(
            master=self.frame_body,
            label_text=LABEL_VERBOSE_TEXT,
            value=model.verbose,
            label_width=120)
        self.check_verbose.pack(side=tk.TOP, anchor=tk.W, pady=5)
        # サブミット領域フレーム
        self.frame_submit = DCFrame(self.frame_body)
        self.frame_submit.pack(side=tk.TOP, anchor=tk.W, pady=5, expand=True, fill="both")
        # コンポーズボタン
        self.button_compose = DCButton(
            master=self.frame_submit,
            text=BUTTON_COMPOSE_TEXT,
            command=self._on_click_button_submit,
            width=120)
        self.button_compose.pack(side=tk.LEFT, anchor=tk.N)
        # ログ表示領域
        self.textbox_logging = LoggingTextbox(master=self.frame_submit)
        self.textbox_logging.pack(side=tk.LEFT, anchor=tk.N, padx=5, expand=True, fill="both")

    def _on_click_button_submit(self):
        # ユーザ設定値をモデルに抽出
        self.model.src_dir_path = self.entry_src_dir.get_value()
        self.model.src_file_ext = self.combo_src_ext.get_value()
        self.model.dest_dir_path = self.entry_dest_dir.get_value()
        self.model.dest_file_ext = self.combo_dest_ext.get_value()
        self.model.config_file_path = self.entry_config_file.get_value()
        self.model.verbose = self.check_verbose.get_value()
        exec_composer(
            self.model.src_dir_path,
            self.model.dest_dir_path,
            self.model.config_file_path,
            self.model.src_file_ext,
            self.model.dest_file_ext,
            self.model.verbose,
            "gui")

    def _on_closing(self):
        self.model.dump_yml()  # モデルをファイルに保存
        self.destroy()  # 閉じる処理を明示的に呼ばないと閉じない


def exec_composer_with_gui():
    """ルートウィンドウを表示する。"""
    model = RootScreenModel.from_yml()
    root = RootScreen(model)
    DCWidget.set_appearance_mode("dark")
    root.mainloop()
