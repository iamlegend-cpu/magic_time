# 🌐 Environment Variables Setup - Magic Time Studio v2.0.0

## 📋 Overzicht

Magic Time Studio v2.0.0 ondersteunt nu environment variables via `.env` bestanden voor LibreTranslate configuratie. Dit maakt het eenvoudiger om verschillende servers en instellingen te gebruiken zonder de code aan te passen.

## 🚀 Snelle Setup

### Stap 1: Template kopiëren
```bash
# Kopieer de template naar een .env bestand
cp config_template.env .env
```

### Stap 2: Aanpassen
Bewerk het `.env` bestand en pas de waarden aan:

```env
# LibreTranslate Server Configuratie
LIBRETRANSLATE_SERVER=http://100.90.127.78:5000

# API Key voor LibreTranslate (indien vereist)
# LIBRETRANSLATE_API_KEY=your_api_key_here

# Timeout instellingen
LIBRETRANSLATE_TIMEOUT=30

# Rate limiting instellingen
LIBRETRANSLATE_RATE_LIMIT=60
```

## 🔧 Beschikbare Variables

### LIBRETRANSLATE_SERVER
**Type:** URL  
**Standaard:** `http://100.90.127.78:5000`  
**Beschrijving:** De URL van je LibreTranslate server

**Voorbeelden:**
```env
# Lokale server
LIBRETRANSLATE_SERVER=http://localhost:5000

# Publieke server
LIBRETRANSLATE_SERVER=https://libretranslate.com

# Custom server
LIBRETRANSLATE_SERVER=http://192.168.1.100:5000
```

### LIBRETRANSLATE_API_KEY
**Type:** String  
**Standaard:** (leeg)  
**Beschrijving:** API key voor LibreTranslate (indien vereist)

```env
LIBRETRANSLATE_API_KEY=your_secret_api_key_here
```

### LIBRETRANSLATE_TIMEOUT
**Type:** Integer (seconden)  
**Standaard:** `30`  
**Beschrijving:** Timeout voor API requests

```env
LIBRETRANSLATE_TIMEOUT=60
```

### LIBRETRANSLATE_RATE_LIMIT
**Type:** Integer (requests per minuut)  
**Standaard:** `60`  
**Beschrijving:** Rate limiting voor API requests

```env
LIBRETRANSLATE_RATE_LIMIT=30
```

## 📁 Bestand Locaties

Magic Time Studio zoekt naar `.env` bestanden in deze volgorde:

1. **`magic_time_studio/.env`** - Project directory (aanbevolen)
2. **`./.env`** - Huidige werkdirectory
3. **`~/.env`** - Home directory

## 🎯 Gebruik in Code

De environment variables worden automatisch geladen en zijn beschikbaar via de config manager:

```python
from magic_time_studio.core.config import config_manager

# LibreTranslate server URL
server_url = config_manager.get_env("LIBRETRANSLATE_SERVER", "http://localhost:5000")

# Timeout instelling
timeout = int(config_manager.get_env("LIBRETRANSLATE_TIMEOUT", "30"))

# API key
api_key = config_manager.get_env("LIBRETRANSLATE_API_KEY", "")
```

## 🔒 Beveiliging

### Best Practices:
- ✅ **Gebruik `.env` voor lokale configuratie**
- ✅ **Voeg `.env` toe aan `.gitignore`**
- ✅ **Gebruik `config_template.env` als template**
- ✅ **Deel geen API keys in code**

### Wat NIET te doen:
- ❌ **Commit `.env` bestanden naar Git**
- ❌ **Hardcode API keys in code**
- ❌ **Deel `.env` bestanden publiekelijk**

## 🌐 LibreTranslate Server Opties

### 1. Publieke Servers
```env
# Officiële LibreTranslate server
LIBRETRANSLATE_SERVER=https://libretranslate.com

# Community servers
LIBRETRANSLATE_SERVER=https://translate.argosopentech.com
```

### 2. Lokale Server
```env
# Docker
LIBRETRANSLATE_SERVER=http://localhost:5000

# Lokale installatie
LIBRETRANSLATE_SERVER=http://127.0.0.1:5000
```

### 3. Custom Server
```env
# LAN server
LIBRETRANSLATE_SERVER=http://192.168.1.100:5000

# VPS server
LIBRETRANSLATE_SERVER=https://translate.yourdomain.com
```

## 🔧 Troubleshooting

### .env bestand wordt niet geladen
```bash
# Controleer of het bestand bestaat
ls -la .env

# Controleer de syntax
cat .env
```

### Server niet bereikbaar
```bash
# Test de server URL
curl http://your-server:5000/languages

# Controleer firewall instellingen
```

### Timeout errors
```env
# Verhoog timeout
LIBRETRANSLATE_TIMEOUT=60
```

## 📝 Voorbeelden

### Basis Configuratie
```env
LIBRETRANSLATE_SERVER=http://localhost:5000
LIBRETRANSLATE_TIMEOUT=30
```

### Met API Key
```env
LIBRETRANSLATE_SERVER=https://libretranslate.com
LIBRETRANSLATE_API_KEY=your_api_key_here
LIBRETRANSLATE_TIMEOUT=60
LIBRETRANSLATE_RATE_LIMIT=30
```

### Productie Configuratie
```env
LIBRETRANSLATE_SERVER=https://translate.yourdomain.com
LIBRETRANSLATE_API_KEY=production_api_key
LIBRETRANSLATE_TIMEOUT=120
LIBRETRANSLATE_RATE_LIMIT=100
```

## 🤝 Bijdragen

Heb je suggesties voor extra environment variables? Open een issue of pull request!

---

**Magic Time Studio v2.0.0** - Flexibele LibreTranslate configuratie! 🌐✨ 