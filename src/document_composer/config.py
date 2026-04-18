"""構成情報モジュール。"""
import dataclasses
import yaml
import pathlib
from document_composer.constants import (
    IGNORANTS,
    DEST_ROOT_FILE_NICKNAME,
    FILE_SEPARATOR,
    PARAGRAPH_STYLE_NAME,
    PARAGRAPH_PT_BEFORE,
    PARAGRAPH_PT_AFTER,
    PAGE_WIDTH_MM,
    PAGE_HEIGHT_MM,
    LEFT_MARGIN_MM,
    TOP_MARGIN_MM,
    RIGHT_MARGIN_MM,
    BOTTOM_MARGIN_MM,
    HEADER_DISTANCE_MM,
    FOOTER_DISTANCE_MM,
    ENCODING,
    NEWLINE_CODE_SRC,
    NEWLINE_CODE_DEST,
    CONFIG_FILE_PATH,
    NewlineCode,
    NewlineChar
)
from document_composer.util import (
    get_newline_char
)


class ConfigLoader(yaml.SafeLoader):
    """構成ファイル用の独自YAMLローダー。"""
    pass


@dataclasses.dataclass
class Config:
    """構成情報データモデル。

    Attribute:
        ignorants (list[pathlib.Path]): イグノアリスト。
        dest_root_file_nickname (str): 出力ルートファイルのファイル名(拡張子なし)。
        file_separator (list[str]): ファイル単位のセパレーターのリスト。
        paragraph_style_name (str): 段落のスタイル名。
        paragraph_pt_before (float): 段落前のスペース。
        paragraph_pt_after (float): 段落後のスペース。
        page_width_mm (float): ページの横幅。ミリ単位。
        page_height_mm (float): パージの縦幅。ミリ単位。
        left_margin_mm (float): ページの左端の余白。ミリ単位。
        top_margin_mm (float): ページの上端の余白。ミリ単位。
        right_margin_mm (float): ページの右端の余白。ミリ単位。
        bottom_margin_mm (float): ページの下端の余白。ミリ単位。
        header_distance_mm (float): ヘッダーの幅。ミリ単位。
        footer_distance_mm (float): フッターの幅。ミリ単位。
        encoding (str): 文字エンコーディング方式。
        newline_code_src (NewlineCode): 入力ファイル改行コード。
        newline_code_dest (NewlineCode): 出力ファイル改行コード。
    """
    ignorants: list[pathlib.Path]
    dest_root_file_nickname: str
    file_separator: list[str]
    paragraph_style_name: str
    paragraph_pt_before: float
    paragraph_pt_after: float
    page_width_mm: float
    page_height_mm: float
    left_margin_mm: float
    top_margin_mm: float
    right_margin_mm: float
    bottom_margin_mm: float
    header_distance_mm: float
    footer_distance_mm: float
    encoding: str
    newline_code_src: NewlineCode
    newline_code_dest: NewlineCode

    @property
    def ignorants_as_str(self) -> pathlib.Path:
        """イグノアリストを絶対パスの文字列として取得する。

        Returns:
            list[str]: イグノアリスト。
        """
        return [ig.resolve() for ig in self.ignorants]

    @property
    def newline_char_src(self) -> NewlineChar:
        """入力ファイルの改行コードを改行文字として取得。

        Returns:
            NewlineChar: 改行文字。
        """
        return get_newline_char(self.newline_code_src)

    @property
    def newline_char_dest(self) -> NewlineChar:
        """出力ファイルの改行コードを改行文字として取得。

        Returns:
            NewlineChar: 改行文字。
        """
        return get_newline_char(self.newline_code_dest)

    @classmethod
    def from_yml(cls, config_file_path: str = CONFIG_FILE_PATH) -> 'Config':
        """YAMLファイルからインスタンスを生成する。

        Args:
            config_file_path (str): 構成ファイルまでのパス。

        Return:
            Config: インスタンス。
        """
        with open(config_file_path, mode="r", encoding=ENCODING) as f:
            d = yaml.load(f, Loader=ConfigLoader)
        if d is None:
            d = {}
        return cls.from_dict(d)

    @classmethod
    def from_dict(cls, d: dict) -> 'Config':
        """辞書からインスタンスを生成する。

        Args:
            d (dict): 辞書。

        Returns:
            Config: インスタンス。
        """
        return cls(
            ignorants=[pathlib.Path(ig) for ig in d.get("ignorants", IGNORANTS)],  # イグノアリストは絶対パスに正規化して格納する
            dest_root_file_nickname=d.get("dest_root_file_nickname", DEST_ROOT_FILE_NICKNAME),
            file_separator=d.get("file_separator", FILE_SEPARATOR),
            paragraph_style_name=d.get("paragraph_style_name", PARAGRAPH_STYLE_NAME),
            paragraph_pt_before=d.get("paragraph_pt_before", PARAGRAPH_PT_BEFORE),
            paragraph_pt_after=d.get("paragraph_pt_after", PARAGRAPH_PT_AFTER),
            page_width_mm=d.get("page_width_mm", PAGE_WIDTH_MM),
            page_height_mm=d.get("page_height_mm", PAGE_HEIGHT_MM),
            left_margin_mm=d.get("left_margin_mm", LEFT_MARGIN_MM),
            top_margin_mm=d.get("top_margin_mm", TOP_MARGIN_MM),
            right_margin_mm=d.get("right_margin_mm", RIGHT_MARGIN_MM),
            bottom_margin_mm=d.get("bottom_margin_mm", BOTTOM_MARGIN_MM),
            header_distance_mm=d.get("header_distance_mm", HEADER_DISTANCE_MM),
            footer_distance_mm=d.get("footer_distance_mm", FOOTER_DISTANCE_MM),
            encoding=d.get("encoding", ENCODING),
            newline_code_src=d.get("newline_code_src", NEWLINE_CODE_SRC),
            newline_code_dest=d.get("newline_code_dest", NEWLINE_CODE_DEST),
        )

    def __repr__(self):
        """インスタンスの文字列表現を返却する。

        Returns:
            str: 各パラメータの文字列表現。
        """
        return f"ignorants={self.ignorants_as_str}" \
            + f"file_separator={self.file_separator}," \
            + f"paragraph_style_name={self.paragraph_style_name}, " \
            + f"paragraph_pt_before={self.paragraph_pt_before}, " \
            + f"paragraph_pt_after={self.paragraph_pt_after}, " \
            + f"page_width_mm={self.page_width_mm}, " \
            + f"page_height_mm={self.page_height_mm}, " \
            + f"left_margin_mm={self.left_margin_mm}, " \
            + f"top_margin_mm={self.top_margin_mm}, " \
            + f"right_margin_mm={self.right_margin_mm}, " \
            + f"bottom_margin_mm={self.bottom_margin_mm}, " \
            + f"header_distance_mm={self.header_distance_mm}, " \
            + f"footer_distance_mm={self.footer_distance_mm}, " \
            + f"encodingf={self.encoding}, " \
            + f"newline_code_src={self.newline_code_src}" \
            + f"newline_code_dest={self.newline_code_dest}"
