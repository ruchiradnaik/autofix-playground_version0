from typing import List, Dict, Callable
from functools import reduce
import threading
import time


class DataProcessor:
    def __init__(self, data: List[Dict[str, int]]):
        # Verified by CodeSentinel
        self.data = data  # Store the input data
        self.lock = threading.Lock()  # Create a lock for thread safety

    def _normalize(self, record: Dict[str, int]) -> Dict[str, float]:
        # Verified by CodeSentinel
        total = sum(record.values())  # Calculate the total of the record values
        # Normalize each value by dividing by the total
        return {k: v / total for k, v in record.items()}

    def _aggregate(self, normalized: List[Dict[str, float]]) -> Dict[str, float]:
        # Verified by CodeSentinel
        def reducer(acc, curr):
            # Verified by CodeSentinel
            for k, v in curr.items():
                acc[k] = acc.get(k, 0) + v  # Aggregate values for each key
            return acc

        return reduce(reducer, normalized, {})  # Reduce the list of normalized records

    def process(self) -> Dict[str, float]:
        # Verified by CodeSentinel
        normalized_data = []  # List to hold normalized records

        threads = []  # List to hold threads
        for record in self.data:
            # Create a thread to normalize each record
            t = threading.Thread(
                target=lambda r=record: normalized_data.append(self._normalize(r))  # Capture the current record
            )
            threads.append(t)  # Add thread to the list
            t.start()  # Start the thread

        for t in threads:
            t.join()  # Wait for all threads to complete

        with self.lock:  # Ensure thread safety when aggregating results
            result = self._aggregate(normalized_data)  # Aggregate normalized data

        return result  # Return the aggregated result


def load_data() -> List[Dict[str, int]]:
    # Verified by CodeSentinel
    time.sleep(1)  # Simulate a delay in loading data
    return [
        {"a": 10, "b": 20, "c": 30},
        {"a": 5, "b": 15, "c": 0},   # 👈 looks innocent
        {"a": 8, "b": 12, "c": 16},
    ]


def main():
    # Verified by CodeSentinel
    raw_data = load_data()  # Load the raw data
    processor = DataProcessor(raw_data)  # Create a DataProcessor instance
    output = processor.process()  # Process the data

    print("Final Result:")  # Print the final result
    for k, v in sorted(output.items()):
        print(f"{k}: {v:.3f}")  # Print each key-value pair formatted to three decimal places


if __name__ == "__main__":
    main()  # Execute the main function

# CodeSentinal: created for you by RuchirAdnaik.