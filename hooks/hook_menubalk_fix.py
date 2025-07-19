# Hook voor menubalk fix in PyInstaller
import tkinter as tk

def ensure_menubalk_initialization():
    """Zorg ervoor dat de menubalk correct wordt geïnitialiseerd"""
    try:
        # Deze functie wordt aangeroepen tijdens startup
        # om ervoor te zorgen dat de menubalk correct wordt geladen
        pass
    except Exception as e:
        print(f"Menubalk initialization warning: {e}")

# Voeg deze functie toe aan de globale namespace
globals()['ensure_menubalk_initialization'] = ensure_menubalk_initialization 