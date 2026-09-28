import time
from typing import List, Dict, Any, Optional

class LWWElementSet:
    def __init__(self):
        self.add_set: Dict[str, float] = {}
        self.remove_set: Dict[str, float] = {}

    def add(self, element: str, timestamp: Optional[float] = None) -> Dict[str, Any]:
        ts = timestamp if timestamp is not None else time.time()
        self.add_set[element] = max(self.add_set.get(element, 0.0), ts)
        return {"action": "add", "element": element, "timestamp": ts}

    def remove(self, element: str, timestamp: Optional[float] = None) -> Dict[str, Any]:
        ts = timestamp if timestamp is not None else time.time()
        self.remove_set[element] = max(self.remove_set.get(element, 0.0), ts)
        return {"action": "remove", "element": element, "timestamp": ts}

    def contains(self, element: str) -> bool:
        add_ts = self.add_set.get(element)
        if add_ts is None:
            return False
        remove_ts = self.remove_set.get(element, -1.0)
        return add_ts >= remove_ts

    def elements(self) -> List[str]:
        return [elem for elem in self.add_set if self.contains(elem)]

    def merge_state(self, remote_add: Dict[str, float], remote_remove: Dict[str, float]) -> Dict[str, Any]:
        for k, ts in remote_add.items():
            self.add_set[k] = max(self.add_set.get(k, 0.0), ts)
        for k, ts in remote_remove.items():
            self.remove_set[k] = max(self.remove_set.get(k, 0.0), ts)
        return {
            "converged_elements": self.elements(),
            "total_adds": len(self.add_set),
            "total_removes": len(self.remove_set)
        }

    def benchmark_crdt_sync(self) -> Dict[str, Any]:
        self.add("task-alpha", 100.0)
        self.add("task-beta", 105.0)
        self.remove("task-alpha", 110.0)
        remote_adds = {"task-alpha": 120.0, "task-gamma": 90.0}
        remote_rems = {"task-gamma": 80.0}
        return self.merge_state(remote_adds, remote_rems)
