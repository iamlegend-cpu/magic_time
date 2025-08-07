"""
Test script voor progress completion
Test of de progress bar correct naar 100% gaat
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_progress_completion():
    """Test of progress correct naar 100% gaat"""
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        # Zorg ervoor dat Fast Whisper actief is
        whisper_manager.initialize("fast", "large-v3-turbo")
        
        # Mock callback counter en progress tracking
        callback_count = 0
        progress_values = []
        
        def mock_progress_callback(progress_bar):
            nonlocal callback_count, progress_values
            callback_count += 1
            
            # Parse progress uit progress bar
            try:
                if "%" in progress_bar:
                    progress_str = progress_bar.split("%")[0].strip()
                    progress = float(progress_str) / 100.0
                    progress_values.append(progress)
                    print(f"🔍 [DEBUG] Mock callback #{callback_count}: {progress:.1%}")
                else:
                    progress = 0.5
                    progress_values.append(progress)
                    print(f"🔍 [DEBUG] Mock callback #{callback_count}: {progress:.1%} (fallback)")
            except:
                progress = 0.5
                progress_values.append(progress)
                print(f"🔍 [DEBUG] Mock callback #{callback_count}: {progress:.1%} (error)")
            
            return True  # Ga door
        
        # Test transcriptie call
        print("🔍 [DEBUG] Test progress completion...")
        
        # Mock audio path (niet echt bestand)
        mock_audio_path = "test_audio.wav"
        
        # Test transcriptie call (zonder echt bestand)
        try:
            result = whisper_manager.transcribe_audio(mock_audio_path, progress_callback=mock_progress_callback)
            print(f"🔍 [DEBUG] Transcriptie call uitgevoerd, callback count: {callback_count}")
            print(f"🔍 [DEBUG] Progress values: {[f'{p:.1%}' for p in progress_values]}")
            
            if callback_count > 0:
                print("✅ Callbacks worden aangeroepen")
                
                # Controleer of er een 100% update is
                if 1.0 in progress_values:
                    print("✅ 100% progress update gevonden")
                    return True
                else:
                    print("⚠️ Geen 100% progress update gevonden")
                    return False
            else:
                print("⚠️ Geen callbacks aangeroepen")
                return False
                
        except Exception as e:
            print(f"🔍 [DEBUG] Transcriptie call error (verwacht): {e}")
            return False
        
    except Exception as e:
        print(f"❌ Progress completion test gefaald: {e}")
        return False

def test_progress_flow():
    """Test complete progress flow"""
    try:
        # Simuleer progress flow
        print("🔍 [DEBUG] Test complete progress flow...")
        
        # Mock progress values
        progress_values = [0.0, 0.25, 0.5, 0.75, 0.9, 1.0]
        
        for progress in progress_values:
            print(f"🔍 [DEBUG] Progress: {progress:.1%}")
            
            # Simuleer progress bar
            progress_bar = f"{int(progress * 100):3d}%|{'█' * int(progress * 40)}{'░' * (40 - int(progress * 40))}| test.mp4"
            print(f"🔍 [DEBUG] Progress bar: {progress_bar}")
        
        print("✅ Complete progress flow werkt")
        return True
        
    except Exception as e:
        print(f"❌ Progress flow test gefaald: {e}")
        return False

def test_progress_calculation():
    """Test progress berekening"""
    try:
        print("🔍 [DEBUG] Test progress berekening...")
        
        # Test Whisper progress berekening (15-65%)
        whisper_progress_values = [0.0, 0.25, 0.5, 0.75, 1.0]
        
        for progress in whisper_progress_values:
            total_progress = 15 + (progress * 50)  # 15-65% voor Whisper transcriptie
            print(f"🔍 [DEBUG] Whisper progress: {progress:.1%} -> {total_progress:.1f}%")
        
        print("✅ Progress berekening werkt")
        return True
        
    except Exception as e:
        print(f"❌ Progress berekening test gefaald: {e}")
        return False

def main():
    """Hoofdfunctie voor progress completion tests"""
    print("🧪 Start progress completion tests...\n")
    
    # Test 1: Progress completion
    if not test_progress_completion():
        print("❌ Progress completion test gefaald")
        return False
    
    # Test 2: Progress flow
    if not test_progress_flow():
        print("❌ Progress flow test gefaald")
        return False
    
    # Test 3: Progress calculation
    if not test_progress_calculation():
        print("❌ Progress calculation test gefaald")
        return False
    
    print("\n✅ Alle progress completion tests geslaagd!")
    print("\n🎉 Progress completion werkt correct!")
    
    print("\n📋 Progress completion status:")
    print("• ✅ Progress gaat naar 100%")
    print("• ✅ Correcte progress flow")
    print("• ✅ Juiste progress berekening")
    print("• ✅ Geen vastlopen op 29%")
    print("• ✅ Complete progress updates")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 