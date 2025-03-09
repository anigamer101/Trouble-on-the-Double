; -- Trouble on the Double Installer Script --

[Setup]
AppName=Trouble on the Double
AppVersion=1.0
DefaultDirName={autopf}\Trouble on the Double
DefaultGroupName=Trouble on the Double
OutputDir=output
OutputBaseFilename=TroubleOnTheDoubleInstaller
Compression=lzma
SolidCompression=yes
SetupIconFile="assets\imgs\logo\LOGO.ico"
UninstallDisplayIcon={app}\assets\imgs\logo

[Files]
; Main executable from PyInstaller output
Source: "Trouble on the Double.exe"; DestDir: "{app}"; Flags: ignoreversion

; Game assets folder (optional if you used --onefile and bundled assets in exe)
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; License and readme files
Source: "er\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\readme.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Desktop shortcut
Name: "{commondesktop}\Trouble on the Double"; Filename: "{app}\Trouble on the Double.exe"; IconFilename: "{app}\assets\imgs\Logo\LOGO.ico"

; Start menu shortcut
Name: "{group}\Trouble on the Double"; Filename: "{app}\Trouble on the Double.exe"; IconFilename: "{app}\assets\imgs\Logo\LOGO.ico"

[Run]
; Launch game after install
Filename: "{app}\Trouble on the Double.exe"; Description: "Play Trouble on the Double"; Flags: nowait postinstall skipifsilent
