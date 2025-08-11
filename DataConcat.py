import json
import random
import sys
from pathlib import Path

def concat_and_shuffle_jsonl(input_files, output_file):
    all_entries = []
    for file_path in input_files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    all_entries.append(json.loads(line))
    print(f"Loaded {len(all_entries)} entries from {len(input_files)} files.")
    random.shuffle(all_entries)
    with open(output_file, "w", encoding="utf-8") as out_f:
        for entry in all_entries:
            out_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"Shuffled and wrote {len(all_entries)} entries to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python DataConcat.py <output_file.jsonl> <input1.jsonl> <input2.jsonl> ...")
        sys.exit(1)
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    # Validate files exist
    for f in input_files:
        if not Path(f).is_file():
            print(f"Error: File not found: {f}")
            sys.exit(1)
    # Call the function to actually process the files
    concat_and_shuffle_jsonl(input_files, output_file)