# Run with: pyinstaller packaging\OpenClassPad.spec
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all("sympy")
a = Analysis(["run.py"], pathex=[], binaries=binaries, datas=datas,
             hiddenimports=hiddenimports, hookspath=[], hooksconfig={},
             runtime_hooks=[], excludes=[])
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name="OpenClassPad",
          debug=False, bootloader_ignore_signals=False, strip=False, upx=True,
          console=False, icon=None)
