import inspect
import sys

def fake_getsource(*args, **kwargs):
    # Return empty string instead of raising error
    return ""

# Replace getsource before any torch imports
inspect.getsource = fake_getsource

# Also patch inspect.getsourcefile to avoid similar issues
def fake_getsourcefile(*args, **kwargs):
    return None

inspect.getsourcefile = fake_getsourcefile