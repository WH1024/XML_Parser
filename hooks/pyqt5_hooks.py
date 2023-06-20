# pyqt5_hooks.py

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = collect_data_files('PyQt5')
hiddenimports = collect_submodules('PyQt5')