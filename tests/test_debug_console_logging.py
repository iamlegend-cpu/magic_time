#!/usr/bin/env python3
"""
Test script voor console logging en SRT generatie debugging
"""

import os
import sys
import logging
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def force_debug_mode():
    """Forceer debug mode door environment variables te zetten"""
    print("🔧 Forceer debug mode...")
    
    # Zet environment variables voor debug
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["LOG_TO_FILE"] = "true"
    
    print("✅ Debug mode geforceerd")
    print(f"📋 LOG_LEVEL: {os.environ.get('LOG_LEVEL', 'INFO')}")
    print(f"📋 LOG_TO_FILE: {os.environ.get('LOG_TO_FILE', 'false')}")

def test_direct_logging():
    """Test directe logging zonder config manager"""
    print("\n🔍 [DEBUG] Test directe logging...")
    
    try:
        # Import logging module
        from magic_time_studio.core.logging import logger
        
        print("✅ Logger geïmporteerd")
        
        # Test directe logging met geforceerde debug mode
        print("🔍 [DEBUG] Test directe debug logging...")
        
        # Forceer debug mode in logger
        logger.log_to_file = True
        logger.log_level = "DEBUG"
        
        # Test verschillende categorieën
        logger.log_debug("🔍 Direct debug test 1", "debug")
        logger.log_debug("ℹ️ Direct info test 2", "info")
        logger.log_debug("⚠️ Direct warning test 3", "warning")
        logger.log_debug("❌ Direct error test 4", "error")
        
        print("✅ Directe logging test voltooid")
        
    except Exception as e:
        print(f"❌ Directe logging test gefaald: {e}")
        import traceback
        traceback.print_exc()

def test_console_logging():
    """Test console logging functionaliteit"""
    print("🔍 [DEBUG] Test console logging...")
    
    try:
        # Import logging module
        from magic_time_studio.core.logging import logger, log_debug
        
        print("✅ Logging module geïmporteerd")
        
        # Test basis logging
        print("🔍 [DEBUG] Test basis logging...")
        log_debug("Test bericht 1", "debug")
        log_debug("Test bericht 2", "info")
        log_debug("Test bericht 3", "warning")
        log_debug("Test bericht 4", "error")
        
        print("✅ Basis logging test voltooid")
        
        # Test logger direct
        print("🔍 [DEBUG] Test logger direct...")
        logger.log_debug("Direct logger test 1", "debug")
        logger.log_debug("Direct logger test 2", "info")
        logger.log_debug("Direct logger test 3", "warning")
        logger.log_debug("Direct logger test 4", "error")
        
        print("✅ Direct logger test voltooid")
        
        # Test environment variables
        print("🔍 [DEBUG] Test environment variables...")
        from magic_time_studio.core.config import config_manager
        
        log_to_file = config_manager.get_env("LOG_TO_FILE", "false")
        log_level = config_manager.get_env("LOG_LEVEL", "INFO")
        
        print(f"📋 LOG_TO_FILE: {log_to_file}")
        print(f"📋 LOG_LEVEL: {log_level}")
        
        # Test logging config
        logging_config = config_manager.get("logging_config", {})
        print(f"📋 Logging config: {logging_config}")
        
        print("✅ Environment variables test voltooid")
        
    except Exception as e:
        print(f"❌ Console logging test gefaald: {e}")
        import traceback
        traceback.print_exc()

def test_srt_generation():
    """Test SRT generatie functionaliteit"""
    print("\n🔍 [DEBUG] Test SRT generatie...")
    
    try:
        # Import video processor
        from magic_time_studio.processing.video_processor import VideoProcessor
        
        print("✅ VideoProcessor geïmporteerd")
        
        # Maak test transcriptions
        test_transcriptions = [
            {
                "start": 0.0,
                "end": 5.0,
                "text": "Dit is een test transcriptie.",
                "language": "nl"
            },
            {
                "start": 5.0,
                "end": 10.0,
                "text": "Dit is het tweede segment.",
                "language": "nl"
            }
        ]
        
        print(f"📋 Test transcriptions: {len(test_transcriptions)} segmenten")
        
        # Test SRT bestand maken
        processor = VideoProcessor()
        
        # Maak tijdelijk test bestand
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mp4', delete=False) as temp_video:
            temp_video_path = temp_video.name
            temp_video.write("test video content")
        
        print(f"📋 Tijdelijk video bestand: {temp_video_path}")
        
        # Test SRT generatie
        settings = {
            "generate_srt": True,
            "generate_translated_srt": False,
            "preserve_original_subtitles": True
        }
        
        result = processor.generate_srt_files(
            video_path=temp_video_path,
            transcriptions=test_transcriptions,
            settings=settings
        )
        
        print(f"📋 SRT generatie result: {result}")
        
        if result.get("success"):
            output_files = result.get("output_files", {})
            print(f"📋 Output bestanden: {output_files}")
            
            # Controleer of bestanden bestaan
            for file_type, file_path in output_files.items():
                if os.path.exists(file_path):
                    print(f"✅ {file_type} bestand bestaat: {file_path}")
                    # Lees bestand inhoud
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    print(f"📄 Inhoud van {file_type}:")
                    print(content)
                else:
                    print(f"❌ {file_type} bestand bestaat niet: {file_path}")
        else:
            print(f"❌ SRT generatie gefaald: {result.get('error')}")
        
        # Ruim tijdelijk bestand op
        try:
            os.unlink(temp_video_path)
        except:
            pass
            
        print("✅ SRT generatie test voltooid")
        
    except Exception as e:
        print(f"❌ SRT generatie test gefaald: {e}")
        import traceback
        traceback.print_exc()

def test_environment_setup():
    """Test environment setup"""
    print("\n🔍 [DEBUG] Test environment setup...")
    
    try:
        # Test environment file
        env_file = Path("magic_time_studio/whisper_config.env")
        if env_file.exists():
            print(f"✅ Environment file bestaat: {env_file}")
            
            # Lees environment file
            with open(env_file, 'r', encoding='utf-8') as f:
                env_content = f.read()
            
            print("📋 Environment file inhoud:")
            print(env_content)
        else:
            print(f"❌ Environment file bestaat niet: {env_file}")
        
        # Test config manager
        from magic_time_studio.core.config import config_manager
        
        # Test environment variables
        env_vars = config_manager.load_env_variables()
        print(f"📋 Environment variables: {env_vars}")
        
        print("✅ Environment setup test voltooid")
        
    except Exception as e:
        print(f"❌ Environment setup test gefaald: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Hoofdfunctie"""
    print("🔍 [DEBUG] Console Logging en SRT Generatie Debug Test")
    print("=" * 60)
    
    # Forceer debug mode
    force_debug_mode()
    
    # Test environment setup
    test_environment_setup()
    
    # Test directe logging
    test_direct_logging()
    
    # Test console logging
    test_console_logging()
    
    # Test SRT generatie
    test_srt_generation()
    
    print("\n🎉 Debug test voltooid!")
    print("💡 Controleer de output hierboven voor problemen")

if __name__ == "__main__":
    main() 