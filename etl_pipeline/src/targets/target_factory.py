from typing import Dict, Any
from .local_storage import LocalStorageSink
from .sqlite_sink import SQLiteSink

class TargetFactory:
    @staticmethod
    def get_target(target_type: str, config: Dict[str, Any]):
        if target_type == 'local_storage':
            return LocalStorageSink(config)
        elif target_type == 'sqlite':
            return SQLiteSink(config)
        else:
            raise ValueError(f"Unknown target type: {target_type}")
