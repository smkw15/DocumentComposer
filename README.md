# conv-txt-to-docx

conv-txt-to-docxは、txtファイルをdocxファイルに変換するPythonスクリプトです。

## 開発環境

- 開発環境: Windows
- Python 3.10.6
- VSCode

## 環境構築方法

- 仮想環境:

```sh
# 仮想環境構築
python -m venv env

# 仮想環境起動
.\env\Scripts\activate

# Python依存パッケージのインストール(初回のみ)
pip install -r requirements.txt

# 仮想環境終了(仮想環境内で)
deactivate
```

- ディレクトリ構造:

```txt
./
├─docs
│　├─dest 👈出力先ディレクトリ(実行時自動作成)
│　└─src 👈入力元ディレクトリ
├─env
│　├─Scripts
│　│　├─activate.bat 👈仮想環境起動バッチ
│　│　└─deactivate.bat 👈仮想環境終了バッチ
│　└─... 👈その他仮想環境設定ファイル
├─*.py 👈Pythonソースコード
└─requirements.txt 👈依存ライブラリ
```

## 動作仕様

- conv-txt-to-docxは、入力元ディレクトリに存在するtxtファイルを再帰的に検索し、読み込みます。
- 読み込まれた文字列は、1行=1段落として出力先ディレクトリに1つのdocxファイルとして出力されます。
- 複数のtxtファイルの文字列を1つのdocxファイルに書き込む場合、ファイルの境界を示すファイルセパレータが挿入されます。

## 使用方法

1. 入力元ディレクトリ *docs/src* 配下にtxtファイルを配置する。
2. 以下を実行。

```sh
# 実行(仮想環境内で)
python main.py
```

3. 出力先ディレクトリ *docs/dest* 配下にdocxファイルが作成されます。既定のファイル名は`__all_in_one__.docx`です。

## 開発者向けの設定

- conv-txt-to-docxの動作を制御する各種設定値は、 *constants.py* に定義されており、ユーザはこのファイルの各種設定値を変更することで、conv-txt-to-docxの動作仕様を自由にカスタマイズすることができます。

| 定数名 | 説明 |
| -- | -- | 
| `SRC_DIR` | 入力元ディレクトリの配置場所。|
| `DEST_DIR` | 出力先ディレクトリの配置場所。|
| `DEST_DIR` | 出力先ディレクトリの配置場所。|
| `DEST_FILE_NAME` | 出力されるファイルのファイル名。|
| `FILE_SEPARATOR` | ファイルセパレータ。1つの配列要素が1行の文字列に相当する。|
| `PARAGRAPH_STYLE_NAME` | 段落のスタイル。python-docxの仕様に基づく。|
| `PARAGRAPH_PT_BEFORE` | 段落間スペースのサイズ。段落前。|
| `PARAGRAPH_PT_AFTER` | 段落間スペースのサイズ。段落後。|
| `PAGE_WIDTH_MM` | ページサイズの横幅。mm単位。|
| `PAGE_HEIGHT_MM` | ページサイズの縦幅。mm単位。|
| `LEFT_MARGIN_MM` | ページの余白の左。mm単位。|
| `TOP_MARGIN_MM` | ページの余白の右。mm単位。|
| `RIGHT_MARGIN_MM` | ページの余白の上。mm単位。|
| `BOTTOM_MARGIN_MM` | ページの余白の下。mm単位。|
| `HEADER_DISTANCE_MM` | ヘッダーの幅。mm単位。|
| `FOOTER_DISTANCE_MM` | フッターの幅。mm単位。|
| `ENCODING` | 文字エンコーディング方式。|
| `NEWLINE` | 改行コード。|
