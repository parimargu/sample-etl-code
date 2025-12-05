import sys
import os

# Add project root to sys.path
# Add backend directory to sys.path so 'app' module can be found
# backend/tests -> backend
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
