"""設定情報モジュール。"""
import dataclasses
import yaml
from libs.constants import (
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
    NEWLINE_CODE,
    CONFIG_FILE_PATH,
    NewlineCode,
    NewlineChar
)
from libs.util import (
    get_newline_char
)


class ConfigLoader(yaml.SafeLoader):
    """設定ファイル用の独自YAMLローダー"""
    pass


@dataclasses.dataclass
class Config:
    """設定情報データモデル。

    Attribute:
        file_separator (list[str]): ファイル単位の区切り行リスト。
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
        newline_code (str): 改行コード。
    """
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
    newline_code: NewlineCode

    @property
    def newline_char(self) -> NewlineChar:
        """改行コードを改行文字として取得。

        Returns:
            NewlineChar: 改行文字。
        """
        return get_newline_char(self.newline_code)

    @classmethod
    def from_yml(cls, config_file_path: str = CONFIG_FILE_PATH) -> 'Config':
        """YAMLファイルからインスタンスを生成する。

        Args:
            config_file_path (str): 設定ファイルまでのパス。

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
        file_separator = d["file_separator"] if "file_separator" in d else FILE_SEPARATOR
        paragraph_style_name = d["paragraph_style_name"] if "paragraph_style_name" in d else PARAGRAPH_STYLE_NAME
        paragraph_pt_before = d["paragraph_pt_before"] if "paragraph_pt_before" in d else PARAGRAPH_PT_BEFORE
        paragraph_pt_after = d["paragraph_pt_after"] if "paragraph_pt_after" in d else PARAGRAPH_PT_AFTER
        page_width_mm = d["page_width_mm"] if "page_width_mm" in d else PAGE_WIDTH_MM
        page_height_mm = d["page_height_mm"] if "page_height_mm" in d else PAGE_HEIGHT_MM
        left_margin_mm = d["left_margin_mm"] if "left_margin_mm" in d else LEFT_MARGIN_MM
        top_margin_mm = d["top_margin_mm"] if "top_margin_mm" in d else TOP_MARGIN_MM
        right_margin_mm = d["right_margin_mm"] if "right_margin_mm" in d else RIGHT_MARGIN_MM
        bottom_margin_mm = d["bottom_margin_mm"] if "bottom_margin_mm" in d else BOTTOM_MARGIN_MM
        header_distance_mm = d["header_distance_mm"] if "header_distance_mm" in d else HEADER_DISTANCE_MM
        footer_distance_mm = d["footer_distance_mm"] if "footer_distance_mm" in d else FOOTER_DISTANCE_MM
        encoding = d["encoding"] if "encoding" in d else ENCODING
        newline_code = d["newline_code"] if "newline_code" in d else NEWLINE_CODE
        return cls(
            file_separator=file_separator,
            paragraph_style_name=paragraph_style_name,
            paragraph_pt_before=paragraph_pt_before,
            paragraph_pt_after=paragraph_pt_after,
            page_width_mm=page_width_mm,
            page_height_mm=page_height_mm,
            left_margin_mm=left_margin_mm,
            top_margin_mm=top_margin_mm,
            right_margin_mm=right_margin_mm,
            bottom_margin_mm=bottom_margin_mm,
            header_distance_mm=header_distance_mm,
            footer_distance_mm=footer_distance_mm,
            encoding=encoding,
            newline_code=newline_code
        )

    def __repr__(self):
        """インスタンスの文字列表現を返却する。

        Returns:
            str: 各パラメータの文字列表現。
        """
        return f"file_separator={self.file_separator}," \
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
            + f"newline_code={self.newline_code}"
