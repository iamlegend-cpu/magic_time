# LibreTranslate Server Configuratie

## 🎯 **Overzicht**

Magic Time Studio gebruikt LibreTranslate voor vertalingen. **Er zijn geen hardcoded IP adressen meer in de code** - elke gebruiker moet zijn eigen server IP configureren.

## 🌐 **Server Opties**

### **1. Lokale LibreTranslate Server**

Als je LibreTranslate lokaal draait:

```bash
# Docker
docker run -it --rm -p 5000:5000 libretranslate/libretranslate

# Of lokaal geïnstalleerd
libretranslate --host 0.0.0.0 --port 5000
```

**Configuratie in Magic Time Studio:**
- Open **Settings Panel** (⚙️ icoon)
- Selecteer **LibreTranslate** als vertaler
- Voer in: `localhost:5000`

### **2. LAN Server**

Als je LibreTranslate op een andere computer in je netwerk draait:

```bash
# Op server computer
libretranslate --host 0.0.0.0 --port 5000
```

**Configuratie in Magic Time Studio:**
- Open **Settings Panel** (⚙️ icoon)
- Selecteer **LibreTranslate** als vertaler
- Voer in: `192.168.1.100:5000` (vervang met jouw server IP)

### **3. Publieke LibreTranslate Server**

Voor publieke servers:

**Configuratie in Magic Time Studio:**
- Open **Settings Panel** (⚙️ icoon)
- Selecteer **LibreTranslate** als vertaler
- Voer in: `libretranslate.com` (zonder poort voor HTTPS)

## 🔧 **Stap-voor-Stap Configuratie**

### **Stap 1: Open Settings Panel**
1. Start Magic Time Studio
2. Klik op **⚙️ Settings** icoon
3. Ga naar **Configuratie** tab

### **Stap 2: Configureer Vertaler**
1. Selecteer **LibreTranslate** in de dropdown
2. Het **Server** veld wordt nu zichtbaar

### **Stap 3: Voer Server IP in**
1. Klik in het **Server** veld
2. Voer je server IP en poort in:
   - `localhost:5000` (voor lokale server)
   - `192.168.1.100:5000` (voor LAN server)
   - `jouw-server.com:5000` (voor externe server)

### **Stap 4: Test Verbinding**
1. Klik **Opslaan**
2. Magic Time Studio test automatisch de verbinding
3. Als de test slaagt, is je configuratie correct

## 🚨 **Belangrijke Punten**

### ✅ **Wat WEL te doen:**
- ✅ **Voer je eigen server IP in**
- ✅ **Test de verbinding voor gebruik**
- ✅ **Gebruik de juiste poort (standaard 5000)**
- ✅ **Controleer firewall instellingen**

### ❌ **Wat NIET te doen:**
- ❌ **Verwacht geen voorgeconfigureerde IP adressen**
- ❌ **Gebruik hardcoded IP adressen**
- ❌ **Vergeet de poort niet toe te voegen**

## 🔍 **Troubleshooting**

### **Server niet bereikbaar**
```bash
# Test verbinding
curl http://jouw-server:5000/languages

# Controleer firewall
# Windows: Windows Defender Firewall
# Linux: ufw of iptables
```

### **Timeout errors**
- Verhoog timeout in **Geavanceerde Instellingen**
- Controleer netwerk verbinding
- Test server beschikbaarheid

### **SSL/HTTPS errors**
- Gebruik `https://` voor beveiligde servers
- Voeg certificaat toe indien nodig

## 📝 **Voorbeelden**

### **Lokale Docker Server**
```
Server: localhost:5000
```

### **LAN Server**
```
Server: 192.168.1.100:5000
```

### **Publieke Server**
```
Server: libretranslate.com
```

### **Custom Domain**
```
Server: translate.mijnwebsite.com:5000
```

## 🎉 **Voordelen van deze Aanpak**

### **🔒 Veiligheid**
- Geen hardcoded IP adressen in code
- Elke gebruiker controleert zijn eigen server
- Geen onbedoelde data lekken

### **🔧 Flexibiliteit**
- Ondersteuning voor alle server types
- Lokale, LAN en publieke servers
- Eenvoudige configuratie via GUI

### **🛠️ Onderhoud**
- Geen code wijzigingen voor server configuratie
- Automatische validatie van instellingen
- Duidelijke foutmeldingen

## 📊 **Test Resultaten**

```
🧪 Test No Hardcoded IPs...
📊 Resultaat: 3/3 tests geslaagd

✅ Geen hardcoded IP adressen in code
✅ Placeholder teksten gebruiken generieke voorbeelden
✅ Gebruiker moet eigen server IP invoeren
✅ Config manager gebruikt geen default IP
```

---

**Magic Time Studio v3.0** - Veilige en flexibele server configuratie! 🌐✨
