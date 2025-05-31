# DocumentComposer

DocumentComposerは、複数の文書ファイルを読み込み、内容を結合し、1つの文書ファイルとして出力するPythonモジュールです。

## 開発環境

- Windows 11
- Python 3.10.6
- venv
- pip
- VSCode
- PEP8

## 環境構築方法

■仮想環境:

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

■ディレクトリ構造:

```txt
📁./
├─📁.github  👈GitHub設定ディレクトリ
├─📁docs
│　├─📁dest  👈出力先ディレクトリ(実行時自動作成)
│　└─📁src  👈入力元ディレクトリ
├─📁env
│　├─📁Scripts
│　│　├─📄activate.bat  👈仮想環境起動バッチ
│　│　└─📄deactivate.bat  👈仮想環境終了バッチ
│　└─📄*.*  👈その他の仮想環境設定ファイル
├─📁lib  👈DocumentComposerのPythonライブラリ
├─🐍main.py  👈DocumentComposerのメインモジュール(エントリーポイント)
├─📄.flake8  👈flake8設定ファイル
├─📄config.yml  👈DocumentComposerの構成ファイル
├─⚖️LICENSE.txt  👈ライセンス情報ファイル
└─📄requirements.txt  👈依存ライブラリ設定ファイル
```

## 動作仕様

- DocumentComposerは、入力元ディレクトリに存在する特定の拡張子を持つ文書ファイル(入力ファイル)を再帰的に検索します。
- 続いて、それらのファイルパスにフィルタリングを施した後、階層ごとに名前順ソートを施し、その順にファイルの内容を読み込みます。
- 読み込まれた内容は、1行=1段落として結合します。1つのファイルの内容と内容の間には、ファイルの境界を示すファイルセパレータが挿入されます。
- 最後に、DocumentComposerは、その結合した内容を特定の拡張子を持つ1つの文書ファイル(出力ファイル)として出力します。
- ユーザは、コマンドライン引数、または、構成ファイルからこれらの動作を制御する設定値を入力することができます。

## 使用方法

仮想環境を起動させ、DocumentComposerのメインモジュールを実行します。

```sh
python main.py 
  [--src <src_dir_path>]
  [--dest <dest_dir_path>]
  [--config <config_file_path>]
  [-x <src_file_kind>]
  [-y <dest_file_kind>]
  [--verbose]
```

メインモジュールには、必要に応じてコマンドライン引数を渡すことができます。ユーザはこれらの引数を利用してDocumentComposerの入出力を制御することができます。

| 引数 | 初期値 | 説明 |
| -- | -- | -- |
| `--src`または`-s` | `./docs/src` | 入力元ディレクトリまでのパス。 |
| `--dest`または`-d` | `./docs/dest` | 出力先ディレクトリまでのパス。 |
| `--config`または`-c` | `./config.yaml` | 構成ファイルまでのパス。 |
| `-x` | `txt` | 入力ファイルの形式を示す文字列。`txt`か`docx`。 |
| `-y` | `docx` | 出力ファイルの形式を示す文字列。`txt`か`docx`。 |
| `--verbose`または`-v` | `False` | 冗長出力を行うか。 |

### 冗長出力オプション

冗長出力とは、txtファイルの結合をディレクトリごとに行う出力方式です。この方式では、出力先ディレクトリに入力元ディレクトリと同様な階層構造が作成され、その中にディレクトリ名をファイル名とした出力ファイルが出力されます。冗長出力を行う場合でも、すべての階層の入力ファイルを含む出力ファイルが出力されます。

■通常の出力:
```txt
📁docs/src
├─📁A
│　├─📄A1
│　└─📄A2
└─📁B
　　├─📄B1
　　└─📄B2

👇処理結果

📁docs/dest
└─📄__all_in_one__  👈A1 + A2 + B1 + B2
```

■冗長出力:
```txt
📁docs/src
├─📁A
│　├─📄A1
│　└─📄A2
└─📁B
 　├─📄B1
 　└─📄B2

👇

📁docs/src
├─📁A
│　└─📄A　👈A1 + A2
├─📁B
│　└─📄B　👈B1 + B2
└─📄__all_in_doc__  👈A1 + A2 + B1 + B2
```

### 構成ファイル

構成ファイルには、DocumentComposerの動作を制御する各種設定値が定義されています。ユーザはこのファイル定義された以下の設定値を編集することで、DocumentComposerの動作を自由にカスタマイズすることができます。

| 設定値名 | 初期値 | 内容 |
| -- | -- | -- |
| `ignorants` | `[]` | 無視リスト。入力対象外にするファイル・ディレクトリまでのパス。相対パスでも絶対パスでもよい。 |
| `dest_root_file_nickname` | `__all_in_one__` | 最上層の出力ファイル(出力ルートファイル)のファイル名。拡張子を記載しない。 |
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
| `newline_code` | `LF` | 改行コード。`LF`、`CRLF`、`LF`のどれか。|

改行コードの仕様は、一般的に多く見られる仕様に準じています。

| 改行コード | 改行文字 | 対応OS |
| -- | -- | -- |
| `LF` | `\n` | Unix/Linux、Mac OS X以降 |
| `CRLF` | `\r\n` | Windows |
| `CR` | `\r` | Mac OS 9以前 |

メインモジュールが終了すると、出力先ディレクトリに出力ファイルが生成されています。
