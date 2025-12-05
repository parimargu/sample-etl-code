import sys
import os

# Add project root to sys.path
# This assumes the test file is in etl_pipeline/tests/
# So we go up two levels: etl_pipeline/tests -> etl_pipeline -> root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
