# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ["src/document_composer/main.py"],
    pathex=[],
    binaries=[],
    datas=collect_data_files("document_composer"),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='document_composer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/document_composer/resources/icon64.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='document_composer_exe',
)

# 簡単に配布できるようにライセンス情報ファイルやREADMEと合わせてzip化する
import shutil 
shutil.copy("./LICENSE.txt", "./dist/document_composer_exe/LICENSE.txt")
shutil.copy("./README.md", "./dist/document_composer_exe/README.md")
shutil.make_archive('document_composer_exe', format='zip', root_dir='./dist/document_composer_exe')
shutil.move('./document_composer_exe.zip', './dist')  # distディレクトリ配下に移動
