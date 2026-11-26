# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import copy_metadata

datas = [('C:\\Users\\7calculus\\Documents\\5TH SEM RUAS\\graph\\new honeypie\\honeypie\\app.py', '.'), ('ui', 'ui'), ('src', 'src'), ('benchmarks', 'benchmarks'), ('data', 'data'), ('results', 'results'), ('.streamlit', '.streamlit')]
binaries = []
hiddenimports = ['__future__.annotations', 'streamlit', 'ui.data', 'ui.tabs_algos.annealing', 'ui.tabs_algos.comparison', 'ui.tabs_algos.exhaustive', 'ui.tabs_algos.greedy', 'ui.tabs_core.centrality', 'ui.tabs_core.overview', 'ui.tabs_core.paths', 'ui.tabs_core.topology', 'ui.tabs_extra.precinct6', 'ui.tabs_extra.results', 'ui.tabs_extra.runner', 'ui.theme']
datas += copy_metadata('streamlit')
tmp_ret = collect_all('streamlit')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:\\Users\\7CALCU~1\\AppData\\Local\\Temp\\tmp_kwvqnwm.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='MyApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MyApp',
)
