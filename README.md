# conv-txt-to-docx

conv-txt-to-docxは、txtファイルをdocxファイルに変換するPythonスクリプトです。

## 環境

- Python 3.10.6
- VSCode

```sh
# 仮想環境起動
.\env\Scripts\activate

# Pythonライブラリのインストール(初回のみ)
pip install -r requirements.txt

# 実行(仮想環境内で)
python main.py

# 仮想環境終了(仮想環境内で)
deactivate
```

- ディレクトリ構造

```txt
./
├─docs
│　├─dest … 出力先ディレクトリ(実行時自動作成)
│　└─src … 入力元ディレクトリ(原稿)
├─env
│　├─Scripts
│　│　├─activate.bat … 仮想環境起動バッチ
│　│　└─deactivate.bat … 仮想環境終了バッチ
│　└─その他仮想環境設定ファイル
├─main.py … Pythonコードエントリーポイント
└─requirements.txt … Pythonライブラリ
```

## 動作仕様

- `conv-txt-to-doc`は、入力元ディレクトリに存在するtxtファイルを再帰的に検索し、読み込みます。
- 読み込まれた文字列は、1行=1段落として出力先ディレクトリに1つのdocxファイルとして出力されます。

## 使い方

1. 入力元ディレクトリ`docs/src`配下にtxtファイルを配置する。
2. 以下を実行。

```sh
# 実行(仮想環境内で)
python main.py
```

3. 出力先ディレクトリ`docs/dest`配下にdocxファイルが作成されます。既定のファイル名は`__all_in_one__.docx`です。
