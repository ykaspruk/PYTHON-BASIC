import os
import csv
from random import randint
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

OUTPUT_DIR = './output'
RESULT_FILE = './output/result.csv'


def fib(n: int):
    """
    Calculate a value in the Fibonacci sequence by ordinal number.
    Optimized for large integers using an iterative approach.
    """
    if n == 0: return 0
    if n == 1: return 1

    f0, f1 = 0, 1
    for _ in range(n - 1):
        f0, f1 = f1, f0 + f1
    return f1


def save_fib_to_file(n: int):
    """Helper function to calculate and save a single number."""
    value = fib(n)
    file_path = os.path.join(OUTPUT_DIR, f"{n}.txt")
    with open(file_path, 'w') as f:
        f.write(str(value))

def read_fib_file(filename: str):
    """Helper function to read a file and return the ordinal and value."""
    if filename.endswith('.txt'):
        ordinal = filename.replace('.txt', '')
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, 'r') as f:
            value = f.read().strip()
        return ordinal, value
    return None


def func1(array: list):
    """
    Uses ProcessPoolExecutor to calculate Fibonacci numbers in parallel.
    This bypasses the Python GIL for CPU-bound tasks.
    """
    print(f"Starting Task 1: Calculating {len(array)} Fibonacci numbers...")
    with ProcessPoolExecutor() as executor:
        executor.map(save_fib_to_file, array)
    print("Task 1 complete.")

def func2(result_file: str):
    """
    Uses ThreadPoolExecutor to read files concurrently and write to a CSV.
    I/O-bound tasks benefit from threading.
    """
    print(f"Starting Task 2: Aggregating files into {result_file}...")
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.txt')]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(read_fib_file, files))

    # Write results to CSV
    with open(result_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in results:
            if row:
                writer.writerow(row)
    print("Task 2 complete.")


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    random_ordinals = [randint(1000, 100000) for _ in range(1000)]

    func1(array=random_ordinals)
    func2(result_file=RESULT_FILE)