from typing import List, Dict, Callable
from functools import reduce
import threading
import time


class DataProcessor:
    def __init__(self, data: List[Dict[str, int]]):
        self.data = data
        self.lock = threading.Lock()

    def _normalize(self, record: Dict[str, int]) -> Dict[str, float]:
        total = sum(record.values())
        return {k: v / total for k, v in record.items()}

    def _aggregate(self, normalized: List[Dict[str, float]]) -> Dict[str, float]:
        def reducer(acc, curr):
            for k, v in curr.items():
                acc[k] = acc.get(k, 0) + v
            return acc

        return reduce(reducer, normalized, {})

    def process(self) -> Dict[str, float]:
        normalized_data = []

        threads = []
        for record in self.data:
            t = threading.Thread(
                target=lambda: normalized_data.append(self._normalize(record))
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        with self.lock:
            result = self._aggregate(normalized_data)

        return result


def load_data() -> List[Dict[str, int]]:
    time.sleep(1)
    return [
        {"a": 10, "b": 20, "c": 30},
        {"a": 5, "b": 15, "c": 0},   # 👈 looks innocent
        {"a": 8, "b": 12, "c": 16},
    ]


def main():
    raw_data = load_data()
    processor = DataProcessor(raw_data)
    output = processor.process()

    print("Final Result:")
    for k, v in sorted(output.items()):
        print(f"{k}: {v:.3f}")


if __name__ == "__main__":
    main()
