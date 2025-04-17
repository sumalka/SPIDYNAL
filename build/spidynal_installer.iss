[Setup]
AppName=SPIDYNAL SYSTEM
AppVersion=1.3.0.7
DefaultDirName={pf}\SPIDYNAL
DefaultGroupName=SPIDYNAL
UninstallDisplayIcon={app}\SPIDYNAL.exe
OutputBaseFilename=SPIDYNAL-Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "G:\SPIDYNAL\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional Options:"
Name: "startmenuicon"; Description: "Pin to Start Menu"; GroupDescription: "Additional Options:"


[Icons]
Name: "{group}\SPIDYNAL"; Filename: "{app}\SPIDYNAL.exe"
Name: "{commondesktop}\SPIDYNAL"; Filename: "{app}\SPIDYNAL.exe"; Tasks: desktopicon
Name: "{userprograms}\SPIDYNAL"; Filename: "{app}\SPIDYNAL.exe"; Tasks: startmenuicon

[Run]
Filename: "{app}\SPIDYNAL.exe"; Description: "Launch SPIDYNAL SYSTEM"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\build\spidy\mound\assets\middle.mp3"
