import os

def acquire_single_instance_lock():
    """Probeer een single instance lock te verkrijgen - eenvoudige versie voor exe"""
    try:
        import tempfile
        import time
        
        # Gebruik een unieke lock file naam voor exe omgeving
        lock_file = os.path.join(tempfile.gettempdir(), "magic_time_studio_v6.lock")
        
        # Probeer het bestand te maken met exclusive access
        try:
            with open(lock_file, 'x') as f:
                f.write(f"{os.getpid()}:{time.time()}")
            return lock_file
        except FileExistsError:
            # Bestand bestaat al, controleer of proces nog draait
            try:
                with open(lock_file, 'r') as f:
                    content = f.read().strip()
                    if not content:
                        # Leeg bestand, verwijder en maak nieuw
                        os.remove(lock_file)
                        with open(lock_file, 'x') as f:
                            f.write(f"{os.getpid()}:{time.time()}")
                        return lock_file
                    
                    # Parse PID en timestamp
                    try:
                        pid_str, timestamp_str = content.split(':', 1)
                        pid = int(pid_str)
                        lock_time = float(timestamp_str)
                    except (ValueError, IndexError):
                        # Bestand is corrupt, verwijder en maak nieuw
                        os.remove(lock_file)
                        with open(lock_file, 'x') as f:
                            f.write(f"{os.getpid()}:{time.time()}")
                        return lock_file
                
                # Controleer of proces nog draait
                try:
                    import psutil
                    process = psutil.Process(pid)
                    if process.is_running():
                        # Check of het proces recent is gestart (binnen 10 seconden)
                        current_time = time.time()
                        if current_time - lock_time < 10:  # Proces is recent gestart
                            return None  # Proces draait nog
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
                
                # Proces bestaat niet meer, verwijder bestand en maak nieuw
                try:
                    os.remove(lock_file)
                except:
                    pass
                
                with open(lock_file, 'x') as f:
                    f.write(f"{os.getpid()}:{time.time()}")
                return lock_file
                
            except (ValueError, OSError, IOError):
                # Bestand is corrupt of niet leesbaar, verwijder en maak nieuw
                try:
                    os.remove(lock_file)
                except:
                    pass
                
                with open(lock_file, 'x') as f:
                    f.write(f"{os.getpid()}:{time.time()}")
                return lock_file
                
    except Exception as e:
        print(f"⚠️ Single instance controle gefaald: {e}")
        return None

def release_single_instance_lock(lock_file):
    """Release de single instance lock"""
    if lock_file:
        try:
            if os.path.exists(lock_file):
                os.remove(lock_file)
                print(f"🗑️ Lock file verwijderd: {lock_file}")
        except Exception as e:
            print(f"⚠️ Kon lock file niet verwijderen: {e}")