"""汎用便利モジュール。"""
from document_composer.constants import (
    NEWLINE_CODE_SYSTEM,
    NewlineCode,
    NewlineChar
)


def get_newline_code(newline_char: NewlineChar) -> NewlineCode:
    """改行コードを取得する。

    Args:
        newline_char (NewlineChar): 改行文字。

    Return:
        NewlineCode: 改行コード。
    """
    match(newline_char):
        case "\n":
            return "LF"
        case "\r\n":
            return "CRLF"
        case "\r":
            return "CR"
        case _:
            return "CRLF"


def get_newline_char(newline_code: NewlineCode) -> NewlineChar:
    """改行文字を取得する。

    Args:
        newline_code (str): 改行コード。

    Return:
        NewlineChar: 改行文字。
    """
    match(newline_code):
        case "LF":
            return "\n"
        case "CRLF":
            return "\r\n"
        case "CR":
            return "\r"
        case _:
            return "\r\n"


def join_lines(lines: list[str], newline_code: NewlineCode = NEWLINE_CODE_SYSTEM) -> str:
    """行を結合する。

    Args:
        strings (list[str]): 結合対象の行リスト。
        newline_code (NewlineCode): 結合に用いる改行コード。

    Returns:
        str: 1行に結合した文字列。
    """
    return get_newline_char(newline_code).join(lines)


def split_to_lines(content: str, newline_code: NewlineCode = NEWLINE_CODE_SYSTEM) -> list[str]:
    """文字列を行に分割する。

    Args:
        content (str): 分割対象の文字列。
        newline_code (NewlineCode): 分割に用いる改行コード。

    Returns:
        list[str]: 文字列を分割した行リスト。
    """
    return content.split(get_newline_char(newline_code))


def strip_empty_line(content: str, newline_code: NewlineCode = NEWLINE_CODE_SYSTEM) -> str:
    """文字列の先頭と末尾の空行をストリップ(トリム)する。

    Args:
        content (str): ストリップ対象の文字列。
        newline_code (NewlineCode): 空行扱いする文字コード。

    Returns:
        str: ストリップ後の文字列。
    """
    return content.strip(get_newline_char(newline_code))


def integrate_newline_code(
    string: str,
    newline_code_integrated: NewlineCode = NEWLINE_CODE_SYSTEM
) -> str:
    """文字列に含まれる改行文字列を統一する。

    Args:
        string: サニタイズ対象の文字列。
        newline_code_integrated: 統一先の改行コード。

    Returns:
        str: 改行コード統一後の文字列。
    """
    match(newline_code_integrated):
        case "LF":
            string = string.replace("\r\n", "\n").replace("\r", "\n")
        case "CR":
            string = string.replace("\r\n", "\n").replace("\n", "\r")
        case "CRLF":
            string = string.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\r\n")
        case _:
            pass
    return string
