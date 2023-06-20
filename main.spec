# myapp.spec

# 设置入口点（main script）和名称
# 如果你的主脚本文件名不是main.py，请将下面的main.py替换为你的实际文件名
entry_point='main.py'
name='HDMAN_DTC'

# 添加图标文件
icon='myapp.ico'

# 配置打包选项
a = Analysis([entry_point],
             pathex=['.'],
             binaries=[],
             datas=[(icon, '.')],
             hiddenimports=[],
             hookspath=['.\\hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=None)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=name,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon=icon)