from config import SERVICE_NAME
from repository import kv_store
from repository.cache_repository import snapshot


class UsageTracker:
    def __init__(self, unique_id: str):
        self.unique_id = unique_id

    def compute_usage_snapshot(self):
        kvs_key = f"usage_snapshot_requested_{self.unique_id}"
        usage_snapshot_requested = int(
            kv_store.get_cursor_values({kvs_key}).get(kvs_key, "0")
        )
        kv_store.set_cursor_values({kvs_key: str(usage_snapshot_requested + 1)})

        return [
            {
                "service": SERVICE_NAME,
                "tracker": self.unique_id,
                "snapshot_number": usage_snapshot_requested + 1,
                "cached_results": len(snapshot()),
            }
        ]
