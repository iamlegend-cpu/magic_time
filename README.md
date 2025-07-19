# Magic Time Studio

Magic Time Studio is een krachtige, gebruiksvriendelijke desktopapplicatie voor automatische transcriptie, vertaling en verwerking van video- en audiobestanden. De applicatie is geoptimaliseerd voor Windows en bevat een moderne, toegankelijke interface met veel aandacht voor gebruiksgemak.

---

## ⚡ Belangrijkste Features

- **Batchverwerking** van video’s en audio
- **Automatische transcriptie** met Whisper (OpenAI)
- **Vertaling** met DeepL en Google Translate
- **Slim logvenster** met sticky auto-scroll, kleurcodering en live monitoring
- **MoviePy-integratie** voor videobewerking
- **Donkere modus** (optioneel)
- **Snelle toegang tot outputmap**
- **Instellingen worden onthouden**
- **Robuuste foutafhandeling** en duidelijke meldingen

---

## 🚀 Installatie

1. **Clone of download** deze repository.
2. **Maak een nieuwe virtuele omgeving aan:**
   ```
   python -m venv venv
   ```
3. **Activeer de venv:**
   - PowerShell: `./venv/Scripts/Activate.ps1`
   - CMD: `./venv/Scripts/activate.bat`
4. **Installeer de dependencies:**
   ```
   pip install -r requirements.txt
   ```
5. **Installeer torch (PyTorch) handmatig:**
   - Voor CPU-only:
     ```
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
     ```
   - Zie https://pytorch.org/get-started/locally/ voor andere opties.

---

## 🛠️ Builden tot .exe (PyInstaller)

1. **Zorg dat alle dependencies geïnstalleerd zijn.**
2. **Bouw de executable:**
   ```
   pyinstaller --clean Magic_Time_Studio_v1.9.4_with_torch.spec
   ```
3. **De .exe vind je in de `dist/` map.**

### Let op:

- De .spec-file zorgt dat alle benodigde Whisper assets (`mel_filters.npz`, `multilingual.tiktoken`) en custom hooks worden meegenomen.
- MoviePy, Whisper, Numba, NumPy, SciPy en andere gevoelige dependencies zijn op stabiele, bewezen versies vastgezet.

---

## 📦 Belangrijkste dependency-versies

- **moviepy==1.0.3**
- **librosa==0.9.2**
- **numpy==1.24.4**
- **scipy==1.9.3**
- **openai-whisper** (laatste versie)
- **torch** (zie installatie-instructie)
- **psutil, pillow, requests, tqdm, etc.**

---

## 💡 Gebruiksgemak & recente verbeteringen

- **Sticky auto-scroll** in het logvenster: automatisch scrollen als je onderaan staat, handmatig scrollen als je dat wilt.
- **Alle hooks en assets worden nu gegarandeerd geladen in de .exe.**
- **Heldere foutmeldingen bij ontbrekende assets of dependencies.**
- **Batchverwerking, live log, en parallelle verwerking werken stabiel.**
- **Configuratie en voorkeuren worden automatisch opgeslagen.**

---

## 📝 Tips

- Gebruik altijd de juiste venv en dependency-versies voor een stabiele build.
- Voeg nieuwe Whisper assets toe aan de .spec als je een foutmelding krijgt over ontbrekende bestanden.
- Voor support of uitbreidingen: open een issue of neem contact op!

---

Veel succes en plezier met Magic Time Studio! 