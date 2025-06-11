# DocumentComposer

DocumentComposerは、複数の文書ファイルを読み込み、内容を結合し、1つの文書ファイルとして出力するPythonモジュールです。

## 開発環境

- Windows 11
- pyenv 3.1.1
- Python 3.10.6
- venv
- pip
- VSCode
- PEP8

## 環境構築方法

■仮想環境(Windows):

```sh
# 仮想環境構築
python3 -m venv .env

# 仮想環境起動
.\.env\Scripts\activate

# pip更新
python3 -m pip install --upgrade pip

# Python依存パッケージのインストール
pip install -r requirements.txt

# 仮想環境終了
deactivate
```

■仮想環境(Linux / Mac OS):

```sh
# 仮想環境構築
python3 -m venv .env

# 仮想環境起動
source .env/bin/activate

# pip更新
python3 -m pip install --upgrade pip

# Python依存パッケージのインストール
pip install -r requirements.txt

# 仮想環境終了
deactivate
```

■ディレクトリ構造:

```txt
📁./
├─📁.env
│　├─📁Scripts
│　│　├─📄activate.bat  👈仮想環境起動バッチ
│　│　└─📄deactivate.bat  👈仮想環境終了バッチ
│　└─📄*.*  👈その他の仮想環境設定ファイル
├─📁.github  👈GitHub設定ディレクトリ
├─📁.logs  👈ロギング出力ディレクトリ
├─📁build  👈配布物用ビルドファイルディレクトリ
├─📁dist  👈配布物用ディレクトリ
├─📁docs
│　├─📁dest  👈デフォルトの出力先ディレクトリ(実行時自動作成)
│　└─📁src  👈デフォルトの入力元ディレクトリ
├─📁libs  👈DocumentComposerのPythonライブラリ
├─📁resources  👈画像などのリースファイル
├─📄.flake8  👈flake8設定ファイル
├─📄.gitignore  👈Gitのignore設定ファイル
├─📄.user.yml  👈ユーザ入力ファイル(GUI用)
├─📄config.yml  👈DocumentComposerの構成ファイル
├─📄document_composer.spec  👈配布物作成用仕様ファイル
├─⚖️LICENSE.txt  👈ライセンス情報ファイル
├─📄logging.yml  👈ロギング構成ファイル
├─🐍main.py  👈DocumentComposerのメインモジュール(エントリーポイント)
└─📄requirements.txt  👈依存ライブラリ設定ファイル
```

## 動作仕様

- DocumentComposerは、入力元ディレクトリに存在する特定の拡張子を持つ文書ファイル(入力ファイル)を再帰的に検索します。
- 続いて、それらのファイルパスにフィルタリングを施した後、階層ごとに名前順ソートを施し、その順にファイルの内容を読み込みます。
- 読み込まれた内容は、1行=1段落として結合されます。1つのファイルの内容と内容の間には、ファイルの境界を示すファイルセパレータが挿入されます。
- 最後に、それらの結合した内容を特定の拡張子を持つ1つの文書ファイル(出力ファイル)として出力します。
- これらの一覧の動作をDocumentComposerでは、「コンポーズ」と呼びます。
- ユーザは、コマンドライン引数・構成ファイル・GUIを利用して、コンポーズの動作を決定する各種設定値を自由に設定することができます。

## 使用方法

仮想環境を起動させ、以下のコマンドでDocumentComposerのメインモジュールを実行します。メインモジュールが終了すると、出力先ディレクトリに出力ファイルが生成されます。なお、このコマンドはWindowsでもLinux/Mac OSでも同様です。

```sh
python3 main.py
  [--src <src_dir_path>]
  [--dest <dest_dir_path>]
  [--config <config_file_path>]
  [-x <src_file_kind>]
  [-y <dest_file_kind>]
  [--verbose]
```

### コマンドライン引数

メインモジュールには、必要に応じてコマンドライン引数(オプション)を渡すことができます。ユーザはこれらの引数を利用してDocumentComposerの入出力を制御することができます。

| 引数 | 初期値 | 説明 |
| -- | -- | -- |
| `--src`または`-s` | `./docs/src` | 入力元ディレクトリまでのパス。 |
| `--dest`または`-d` | `./docs/dest` | 出力先ディレクトリまでのパス。 |
| `--config`または`-c` | `./config.yaml` | 構成ファイルまでのパス。 |
| `-x` | `txt` | 入力ファイルの形式を示す文字列。`txt`か`docx`。 |
| `-y` | `txt` | 出力ファイルの形式を示す文字列。`txt`か`docx`。 |
| `--verbose`または`-v` | `False` | 冗長出力を行うか。 |
| `--gui`または`-g` | `False` | GUIを利用するか。 |

#### 構成ファイルオプション

`--config`(ショートハンド: `-c`)は、構成ファイルオプションです。構成ファイルオプションには、構成ファイルまでのパスを渡します。構成ファイルには、DocumentComposerの動作を制御する各種設定値が定義されています。ユーザはこのファイルに定義された以下の設定値を編集することで、DocumentComposerの動作を自由にカスタマイズすることができます。

| 設定値名 | 初期値 | 内容 |
| -- | -- | -- |
| `ignorants` | `[]` | 無視リスト。入力対象外にするファイル・ディレクトリまでのパス。相対パスでも絶対パスでもよい。 |
| `dest_root_file_nickname` | `__all_in_one__` | 最上層の出力ファイル(出力ルートファイル)のファイル名。拡張子を記載しない。 |
| `file_separator` | `['', "＊", '']` | ファイルセパレータ。1つの配列要素が1行の文字列に相当する。|
| `paragraph_style_name` | `Body Text` | 段落のスタイル。python-docxの仕様に基づく。|
| `paragraph_pt_before` | `0.0` | 段落間スペースのサイズ。段落前。|
| `paragraph_pt_after` | `0.0` | 段落間スペースのサイズ。段落後。|
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

#### 冗長出力オプション

`--verbose`(ショートハンド: `-v`)は、冗長出力オプションです。冗長出力オプションを渡すと、冗長出力を実行します。冗長出力とは、コンポーズを入力ディレクトリに存在する階層ごとに実行する出力方式です。この方式では、出力先ディレクトリに入力元ディレクトリと同様な階層構造が作成され、その中にディレクトリごとの出力ファイルが出力されます。出力ファイルのファイル名には、該当するフォルダのフォルダ名が用いられます。冗長出力を行う場合でも、すべての階層の入力ファイルを含む出力ファイルが出力されます。

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

👇処理結果

📁docs/src
├─📁A
│　└─📄A  👈A1 + A2
├─📁B
│　└─📄B  👈B1 + B2
└─📄__all_in_doc__  👈A1 + A2 + B1 + B2
```

#### GUIオプション

`--gui`(ショートハンド: `-g`)は、GUIオプションです。GUIオプションを渡すと、GUIを利用してDocumentComposerを実行することができます。GUIオプションを利用した場合、その他のコマンドライン引数は無視されます。GUIでは、コマンドラインで実行する場合と同様な値を設定することができ、「実行」ボタンを押下することで、DocumentComposerの処理を呼び出すことができます(ログも表示されます)。なお、GUIで入力した値は、コンポーズ実行時にユーザ入力ファイルに保存され、次回ユーザがGUIを利用した際に復元されます。

![image](./resources/gui.png)

### ロギング

DocumentComposerは、ロギング構成ファイルの定義に基づいてロギングを行います。ロギングによってログファイルが作成される場合、ログローテーションの初期設定は、以下の通りです。

| 設定値名 | 初期値 | 説明 |
| -- | -- | -- |
| `when` | `W6` | 毎週日曜日深夜 |
| `interval` | `1` | 1週間ごと |
| `backupCount` | `12` | 最大3か月分(12週間分) |
| `utc` | `False` | 現地時間で |

## 配布方法

DocumentComposerでは、[PyInstaller](https://github.com/pyinstaller/pyinstaller)を利用した実行ファイルの作成に対応しています。実行ファイルを作成するには、仮想環境を起動させ、以下のコマンドを実行します。

```sh
pyinstaller --clean document_composer.spec
```

コマンドが終了すると、配布物用ディレクトリに実行ファイルとそれに関連したファイルが作成されます。

```txt
./
├─📁build
├─📁dist
│　└─📁document_composer
│　　　├─📁_internal
│　　　│　└─📄各種バイナリ(dll, pydなど)
│　　　├─📁resources
│　　　│　├─🖼️icon64.ico
│　　　│　└─🖼️icon64.png
│　　　├─📄config.yml
│　　　├─📄logging.yml
│　　　├─📄README.md
│　　　├─📄LICENSE.txt
│　　　├─📦document_composer.zip
│　　　└─🤖document_composer.exe
├─📄document_composer.spec
└─📄main.py
```

配布するべきファイルは、`dist/document_composer`ディレクトリに存在するすべでのファイル・フォルダです。しかし、実際には、`document_composer.zip`が配布すべきものをすべて含んでいるので、このファイル1つを配布すれば済むようになっています。
