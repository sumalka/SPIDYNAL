pyinstaller --onefile --icon=spidy.ico spidy.py
pyinstaller --onefile --icon=assets/spidy.ico --distpath "C:\Users\Moham\Downloads\pyApp" spidy.py
pyinstaller --onefile --icon=assets/spidy.ico --distpath "C:\Users\Moham\Downloads\pyApp" --hidden-import colorama --hidden-import pygame spidy.py
