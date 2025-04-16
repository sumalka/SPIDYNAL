[Setup]
AppName=SPIDYNAL SYSTEM™
AppVersion=1.3.0.6
DefaultDirName={pf}\SPIDYNAL
DefaultGroupName=SPIDYNAL
UninstallDisplayIcon={app}\SPIDYNAL.exe
OutputBaseFilename=SPIDYNAL-Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "G:\GitHubRep\SPIDYNAL\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\SPIDYNAL"; Filename: "{app}\SPIDYNAL.exe"
Name: "{commondesktop}\SPIDYNAL"; Filename: "{app}\SPIDYNAL.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"
