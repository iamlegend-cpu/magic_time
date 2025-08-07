; Magic Time Studio Installer Script
; Gebruik Inno Setup Compiler om dit script te compileren

[Setup]
; Basis informatie
AppName=Magic Time Studio
AppVersion=1.0.0
AppPublisher=Magic Time Studio
AppPublisherURL=https://github.com/magic-time-studio
AppSupportURL=https://github.com/magic-time-studio/support
AppUpdatesURL=https://github.com/magic-time-studio/updates
DefaultDirName={autopf}\Magic Time Studio
DefaultGroupName=Magic Time Studio
AllowNoIcons=yes
OutputDir=installer_output
OutputBaseFilename=Magic_Time_Studio_Setup
SetupIconFile=assets\Magic_Time_Studio_wit.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; Vereisten
PrivilegesRequired=lowest
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Taal instellingen
LanguageDetectionMethod=locale
ShowLanguageDialog=no

[Languages]
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Hoofdapplicatie
Source: "dist\Magic_Time_Studio\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Assets (als ze niet al in de dist map zitten)
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; FFmpeg (als het niet al in de dist map zit)
Source: "assets\ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion

; Iconen
Source: "assets\Magic_Time_Studio.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\Magic_Time_Studio_wit.ico"; DestDir: "{app}"; Flags: ignoreversion

; Documentatie
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Magic Time Studio"; Filename: "{app}\Magic_Time_Studio.exe"; IconFilename: "{app}\Magic_Time_Studio_wit.ico"
Name: "{group}\{cm:UninstallProgram,Magic Time Studio}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Magic Time Studio"; Filename: "{app}\Magic_Time_Studio.exe"; IconFilename: "{app}\Magic_Time_Studio_wit.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Magic Time Studio"; Filename: "{app}\Magic_Time_Studio.exe"; IconFilename: "{app}\Magic_Time_Studio_wit.ico"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\Magic_Time_Studio.exe"; Description: "{cm:LaunchProgram,Magic Time Studio}"; Flags: nowait postinstall skipifsilent

[Registry]
; Registreer bestandsextensies voor Magic Time Studio
Root: HKCU; Subkey: "Software\Classes\.mp4"; ValueType: string; ValueName: ""; ValueData: "MagicTimeStudio.Video"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\.avi"; ValueType: string; ValueName: ""; ValueData: "MagicTimeStudio.Video"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\.mkv"; ValueType: string; ValueName: ""; ValueData: "MagicTimeStudio.Video"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\.mov"; ValueType: string; ValueName: ""; ValueData: "MagicTimeStudio.Video"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\.wmv"; ValueType: string; ValueName: ""; ValueData: "MagicTimeStudio.Video"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\.flv"; ValueType: string; ValueName: ""; ValueData: "MagicTimeStudio.Video"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\.webm"; ValueType: string; ValueName: ""; ValueData: "MagicTimeStudio.Video"; Flags: uninsdeletevalue

; Registreer MagicTimeStudio.Video protocol
Root: HKCU; Subkey: "Software\Classes\MagicTimeStudio.Video"; ValueType: string; ValueName: ""; ValueData: "Magic Time Studio Video File"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\MagicTimeStudio.Video\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Magic_Time_Studio_wit.ico"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\MagicTimeStudio.Video\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Magic_Time_Studio.exe"" ""%1"""; Flags: uninsdeletekey

[Code]
// Custom code voor extra functionaliteit
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Post-installatie acties kunnen hier worden toegevoegd
  end;
end;

[UninstallDelete]
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"
Type: dirifempty; Name: "{app}"

[CustomMessages]
; Nederlandse berichten
dutch.LaunchProgram=Magic Time Studio starten
dutch.CreateDesktopIcon=Desktop icoon aanmaken
dutch.CreateQuickLaunchIcon=Quick Launch icoon aanmaken
dutch.AdditionalIcons=Extra iconen:
dutch.UninstallProgram=Magic Time Studio verwijderen 