import json
import multiprocessing
from tqdm import tqdm
import os
import sys
from collections import Counter
from tqdm import tqdm

def process_chunk(start, end, filename):
    """Process a chunk of the file and return results."""
    results = {}
    with open(filename, 'rb') as file:
        file.seek(start)
        while file.tell() < end:
            line = file.readline().decode('utf-8')
            if not line:
                break
            try:
                json_obj = json.loads(line)
                key = json_obj['asin']

                if json_obj['helpful'][0] == 0 and json_obj['helpful'][1] == 0:
                    continue

                if key in results:
                    results[key] = results[key] + 1
                else:
                    results[key] = 0

            except json.JSONDecodeError:
                print(f"Failed to parse line: {line}")
    return results

def chunkify(filename, size=1024*1024):
    file_end = os.path.getsize(filename)
    with open(filename, 'rb') as file:
        chunk_end = file.tell()
        while True:
            chunk_start = chunk_end
            file.seek(size, 1)
            file.readline()
            chunk_end = file.tell()
            yield chunk_start, chunk_end
            if chunk_end >= file_end:
                break

def additive_update(original_dict, new_data):
    for key, value in new_data.items():
        if key in original_dict:
            original_dict[key] += value
        else:
            original_dict[key] = value

def collect_results(result, chunk):
    global all_results
    additive_update(all_results, result)
    pbar.update(chunk[1] - chunk[0])

def singlecore(filename):
    total_lines = sum(1 for _ in open(filename, 'r'))
    with open(filename, 'r') as file:
        for line in tqdm(file, total=total_lines, unit="line"):
            try:
                json_obj = json.loads(line)
            except json.JSONDecodeError:
                print(f"Failed to parse line: {line}")

if __name__ == "__main__":
    filename = "aggressive_dedup.json"
    chunk_size = 1024 * 1024  # 1MB chunk size
    all_results = {}
    chunks = list(chunkify(filename, size=chunk_size))
    pbar = tqdm(total=os.path.getsize(filename), unit='B', unit_scale=True)
    cores = 10
    print("number of cores: " + str(cores))
    with multiprocessing.Pool(processes=cores) as pool:
        for chunk in chunks:
            callback = lambda result, chunk=chunk: collect_results(result, chunk)
            pool.apply_async(process_chunk, args=(chunk[0], chunk[1], filename), callback=callback)

        pool.close()
        pool.join()

    pbar.close()

    # all_results now contains all the aggregated results
    max_key = max(all_results, key=all_results.get)
    print(f"The key with the maximum value is: {max_key}")
    print(all_results[max_key])