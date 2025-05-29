"""汎用便利モジュール。"""
from libs.constants import (NewlineCode, NewlineChar)


def get_newline_type(newline_char: NewlineChar) -> NewlineCode:
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
