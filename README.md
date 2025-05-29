# ConvTxtToDocx

ConvTxtToDocxは、txtファイルをdocxファイルに変換するPythonスクリプトです。

## 開発環境

- Windows 11
- Python 3.10.6
- venv
- pip
- VSCode
- PEP8

## 環境構築方法

仮想環境:

```sh
# 仮想環境構築
python -m venv env

# 仮想環境起動/
./env/Scripts/activate

# pip更新
python.exe -m pip install --upgrade pip

# Python依存パッケージのインストール(初回のみ)
pip install -r requirements.txt

# 仮想環境終了(仮想環境内で)
deactivate
```

ディレクトリ構造:

```txt
📁./
├─📁.github  👈GitHub設定情報
├─📁docs
│　├─📁dest  👈出力先ディレクトリ(実行時自動作成)
│　└─📁src  👈入力元ディレクトリ
├─📁env
│　├─📁Scripts
│　│　├─📄activate.bat  👈仮想環境起動バッチ
│　│　└─📄deactivate.bat  👈仮想環境終了バッチ
│　└─📄*.*  👈その他仮想環境設定ファイル
├─📁lib  👈Pythonスクリプト一式
├─🐍main.py 👈Pythonスクリプトのエントリーポイント
├─📄.flake8.py 👈flake8設定ファイル
├─⚖️LICENSE.txt 👈ライセンス情報ファイル
└─📄requirements.txt 👈依存ライブラリ
```

## 動作仕様

- ConvTxtToDocxは、入力元ディレクトリに存在するtxtファイルを再帰的に検索し、読み込みます。
- 読み込まれた文字列は、1行=1段落として出力先ディレクトリに1つのdocxファイルとして出力されます。
- ファイルとファイル間には、境界を示すファイルセパレータが挿入されます。

## 使用方法

仮想環境を起動させ、Pythonスクリプトを実行します。

```sh
python main.py 
  [--src <src_dir_path>]
  [--dest <dest_dir_path>]
  [--file <dest_file_name>]
  [--config <config_file_path>]
```

Pythonスクリプトには、必要に応じてコマンドライン引数を渡すことができます。ユーザはこれらの引数を利用してConvTxtToDocxの入出力を制御することができます。

| 引数 | ショートハンド | 初期値 | 説明 |
| -- | -- | -- | -- |
| `--src` | `-s` | `./docs/src` | 入力元ディレクトリまでのパス。 |
| `--dest` | `-d` | `./docs/dest` | 出力先ディレクトリまでのパス。 |
| `--file` | `-f` | `__all_in_one.docx__` | 出力ファイル名。 |
| `--config` | `-c` | `./config.yaml` | 設定ファイルまでのパス。 |

設定ファイルには、ConvTxtToDocxの動作を制御する各種設定情報が定義されています。ユーザはこのファイル定義された以下の設定値を編集することで、ConvTxtToDocxの動作を自由にカスタマイズすることができます。

| 設定値名 | 初期値 | 内容 |
| -- | -- | -- |
| `file_separator` | `['', "＊", '']` | ファイルセパレータ。1つの配列要素が1行の文字列に相当する。|
| `paragraph_style_name` | `Body Text` | 段落のスタイル。python-docxの仕様に基づく。|
| `paragraph_pt_before` | `0` | 段落間スペースのサイズ。段落前。|
| `paragraph_pt_after` | `0` | 段落間スペースのサイズ。段落後。|
| `page_width_mm` | `210.0` | ページサイズの横幅。mm単位。|
| `page_height_mm` | `297.0` | ページサイズの縦幅。mm単位。|
| `left_margin_mm` | `19.0` | ページの余白の左。mm単位。|
| `top_margin_mm` | `19.0` | ページの余白の右。mm単位。|
| `right_margin_mm` | `19.0` | ページの余白の上。mm単位。|
| `bottom_margin_mm` | `19.0` | ページの余白の下。mm単位。|
| `header_distance_mm` | `19.0` | ヘッダーの幅。mm単位。|
| `footer_distance_mm` | `19.0` | フッターの幅。mm単位。|
| `encoding` | `utf-8` | 文字エンコーディング方式。|
| `newline_code` | `CRLF` | 改行コード。`LF`、`CRLF`、`LF`のどれか。|

改行コードの仕様は、一般的に多く見られる仕様に準じています。

| 改行コード | 改行文字 | 対応OS |
| -- | -- | -- |
| `LF` | `\n` | Unix/Linux、Mac OS X以降 |
| `CRLF` | `\r\n` | Windows |
| `CR` | `\r` | Mac OS 9以前 |

Pythonスクリプトが終了すると、出力先ディレクトリに出力ファイルが生成されています。
