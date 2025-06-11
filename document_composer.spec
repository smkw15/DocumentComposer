# -*- mode: python ; coding: utf-8 -*-

# NOTE: いちいちbuildやdistが残っているか気にするのは面倒なので開始時に全部消す
import shutil

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.yml', '.'),
        ('logging.yml', '.'),
        ('README.md', '.'),
        ('LICENSE.txt', '.'),
        ('resources/icon64.ico', './resources'),
        ('resources/icon64.png', './resources'),
    ],
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
    icon='resources/icon64.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='document_composer',
)

# NOTE: 構成ファイルやリソースファイルなどがバイナリの階層に作られるので無理やり移動させる
shutil.move('./dist/document_composer/_internal/config.yml', './dist/document_composer')
shutil.move('./dist/document_composer/_internal/logging.yml', './dist/document_composer')
shutil.move('./dist/document_composer/_internal/README.md', './dist/document_composer')
shutil.move('./dist/document_composer/_internal/LICENSE.txt', './dist/document_composer')
shutil.move('./dist/document_composer/_internal/resources', './dist/document_composer')

# 簡単に配布できるようにzip化する
shutil.make_archive('document_composer', format='zip', root_dir='./dist/document_composer')
shutil.move('./document_composer.zip', './dist/document_composer')  # distファイルに移動
