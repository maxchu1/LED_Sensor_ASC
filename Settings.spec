# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None
BASE_DIR = os.getcwd()
SITE_PACKAGES_DIR = 'C:\\Users\\max_chu\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages'
ICON_DIR = '..\\Icon\\Icons'
IMG_DIR = '..\\Icon\\IMG'
EXE_NAME  = 'LED_Sensor_ASC'
ICON_NAME = 'LED.ico'
LOGO_NAME = 'accton_logo.png'

a = Analysis(['Main.py','Main_GUI.py','comPort.py','readThread.py',
			 ],
             pathex=[BASE_DIR,
			         SITE_PACKAGES_DIR,
			         os.path.join(SITE_PACKAGES_DIR, 'PySide6\\plugins\\platforms'),
			         os.path.join(SITE_PACKAGES_DIR, 'shiboken6'),
					 ],
             binaries=[],
             datas=[(os.path.join(ICON_DIR, ICON_NAME), '.'), (os.path.join(IMG_DIR, LOGO_NAME), '.'),
					],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
			 win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False,
			 )
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher,
	     )
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=EXE_NAME,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False ,
		  icon=os.path.join(ICON_DIR, ICON_NAME),
		  )
