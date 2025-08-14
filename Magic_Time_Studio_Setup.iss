; Magic Time Studio - Inno Setup Installer Script
; Geoptimaliseerd voor Windows 10/11
; Versie: 3.0

#define MyAppName "Magic Time Studio"
#define MyAppVersion "3.0"
#define MyAppPublisher "Magic Time Studio"
#define MyAppURL "https://github.com/magic-time-studio"
#define MyAppExeName "Magic_Time_Studio.exe"
#define MyAppIcon "assets\Magic_Time_Studio.ico"

[Setup]
; Basis instellingen
AppId={{8F4A8B2C-9E3D-4F1A-B5C7-8D9E0F1A2B3C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={drive:{src}}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir=installer
OutputBaseFilename=Magic_Time_Studio_Setup_v{#MyAppVersion}
SetupIconFile={#MyAppIcon}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
; Verwijder problematische wizard afbeeldingen
; WizardImageFile=assets\Magic_Time_Studio_wit.png
; WizardSmallImageFile=assets\Magic_Time_Studio_wit.png
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Optimalisaties
DiskSpanning=no
DiskSliceSize=max
UseSetupLdr=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
UninstallRestartComputer=no
CloseApplications=no
RestartApplications=no
AllowUNCPath=no
UsePreviousAppDir=yes
UsePreviousGroup=yes
UsePreviousSetupType=yes
UsePreviousTasks=yes
UsePreviousLanguage=yes

; Taal instellingen
LanguageDetectionMethod=locale
ShowLanguageDialog=no

[Languages]
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "startupicon"; Description: "{cm:AutoStartProgram,{#MyAppName}}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Types]
Name: "full"; Description: "{cm:FullInstallation}"
Name: "minimal"; Description: "{cm:MinimalInstallation}"
Name: "custom"; Description: "{cm:CustomInstallation}"; Flags: iscustom

[Components]
Name: "main"; Description: "{cm:MainProgramFiles}"; Types: full minimal custom; Flags: fixed
Name: "whisper"; Description: "Whisper AI Models"; Types: full custom; Flags: disablenouninstallwarning
Name: "docs"; Description: "Documentation"; Types: full custom; Flags: disablenouninstallwarning

[Files]
; Hoofdapplicatie
Source: "dist\Magic_Time_Studio\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: main

; Assets en resources (alleen als ze bestaan)
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: main; Check: DirExists('assets')

; Whisper modellen (optioneel)
Source: "magic_time_studio\models\*"; DestDir: "{app}\models"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: whisper; Check: DirExists('magic_time_studio\models')

; Documentatie
Source: "magic_time_studio\docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: docs; Check: DirExists('magic_time_studio\docs')

; Desktop shortcut
Source: "{#MyAppIcon}"; DestDir: "{app}"; Flags: ignoreversion; Check: FileExists('{#MyAppIcon}')

[Icons]
; Start Menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIcon}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"; IconFilename: "{app}\{#MyAppIcon}"

; Desktop shortcut
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIcon}"; Tasks: desktopicon

; Quick Launch shortcut
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIcon}"; Tasks: quicklaunchicon

; Startup shortcut
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIcon}"; Tasks: startupicon

[Registry]
; Registry registratie is uitgeschakeld
; Alle registry sleutels zijn verwijderd om geen wijzigingen in het Windows register te maken

[Run]
; Start applicatie na installatie (optioneel)
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// Functie om te controleren of PATH update nodig is
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'PATH', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;

// Functie om te controleren of .NET Framework beschikbaar is
function IsDotNetDetected(): boolean;
var
  success: boolean;
  install: cardinal;
  release: cardinal;
  key: string;
begin
  success := false;
  key := 'SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full\';
  
  if RegQueryDWordValue(HKLM, key, 'Install', install) then begin
    if RegQueryDWordValue(HKLM, key, 'Release', release) then begin
      success := (install = 1) and (release >= 378389);
    end;
  end;
  
  Result := success;
end;

// Functie om te controleren of Visual C++ Redistributable beschikbaar is
function IsVCRedistInstalled(): boolean;
var
  success: boolean;
  install: cardinal;
  key: string;
begin
  success := false;
  key := 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64\';
  
  if RegQueryDWordValue(HKLM, key, 'Installed', install) then begin
    success := (install = 1);
  end;
  
  Result := success;
end;

// Functie om te controleren of alle vereisten zijn voldaan
function InitializeSetup(): boolean;
begin
  Result := true;
  
  // Controleer .NET Framework
  if not IsDotNetDetected() then begin
    MsgBox('.NET Framework 4.5 of hoger is vereist voor Magic Time Studio.' + #13#10 + 
           'Download en installeer .NET Framework voordat je doorgaat.', mbInformation, MB_OK);
    Result := false;
    exit;
  end;
  
  // Controleer Visual C++ Redistributable
  if not IsVCRedistInstalled() then begin
    MsgBox('Microsoft Visual C++ 2015-2022 Redistributable is vereist voor Magic Time Studio.' + #13#10 + 
           'Download en installeer de Redistributable voordat je doorgaat.', mbInformation, MB_OK);
    Result := false;
    exit;
  end;
end;

// Functie om te controleren of de gekozen schijf toegankelijk is
function NextButtonClick(CurPageID: Integer): Boolean;
var
  Dir, Drive: string;
begin
  Result := True;
  
  if CurPageID = wpSelectDir then begin
    Dir := WizardForm.DirEdit.Text;
    
    // Controleer alleen of de schijf toegankelijk is, niet of de map bestaat
    Drive := ExtractFileDrive(Dir);
    if (Drive <> '') and not DirExists(Drive) then begin
      MsgBox('De gekozen schijf is niet toegankelijk.' + #13#10 + 
             'Controleer of de schijf beschikbaar is en probeer opnieuw.', mbError, MB_OK);
      Result := False;
      exit;
    end;
    
    // Controleer of we schrijfrechten hebben op de gekozen locatie
    try
      if not ForceDirectories(Dir) then begin
        MsgBox('Kan geen toegang krijgen tot de gekozen locatie.' + #13#10 + 
               'Controleer of je voldoende rechten hebt.', mbError, MB_OK);
        Result := False;
        exit;
      end;
    except
      MsgBox('Kan geen toegang krijgen tot de gekozen locatie.' + #13#10 + 
             'Controleer of je voldoende rechten hebt.', mbError, MB_OK);
      Result := False;
      exit;
    end;
  end;
end;

[UninstallDelete]
; Verwijder configuratie bestanden bij uninstall
Type: files; Name: "{app}\*.env"
Type: files; Name: "{app}\*.json"
Type: files; Name: "{app}\*.log"
Type: dirifempty; Name: "{app}\logs"
Type: dirifempty; Name: "{app}\temp"
Type: dirifempty; Name: "{app}"

[CustomMessages]
dutch.MainProgramFiles=Hoofdprogramma bestanden
dutch.FullInstallation=Volledige installatie
dutch.MinimalInstallation=Minimale installatie
dutch.CustomInstallation=Aangepaste installatie
dutch.CreateDesktopIcon=Bureaublad icoon aanmaken
dutch.CreateQuickLaunchIcon=Snelle start icoon aanmaken
dutch.AutoStartProgram=Automatisch starten van {0}
dutch.AdditionalIcons=Extra iconen
dutch.LaunchProgram=Start {0}
