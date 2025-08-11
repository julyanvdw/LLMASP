"""
DataViewer.py - View random samples from JSONL training data files

Usage:
    python DataViewer.py <filename.jsonl> --n <number_of_samples>
    python DataViewer.py data.jsonl --n 5
"""

import json
import random
import argparse
import sys
import subprocess
import tempfile
import os
from pathlib import Path

# Try to import clingo Python module
try:
    import clingo
    CLINGO_AVAILABLE = True
except ImportError:
    CLINGO_AVAILABLE = False

def validate_asp_with_clingo(asp_code):
    """
    Validate ASP code using clingo.
    Passes if code is syntactically valid and clingo can solve (SAT or UNSAT).
    Fails only on syntax/parse errors or if clingo cannot process the code.
    Ignores warnings about undefined atoms.
    """
    if not CLINGO_AVAILABLE:
        return None, "Clingo not found - install clingo to enable ASP validation"
    
    try:
        ctl = clingo.Control([])
        ctl.logger = lambda code, msg: None  # Suppress info/warning output
        ctl.add("base", [], asp_code)
        ctl.ground([("base", [])])
        ctl.solve()  # Try to solve (SAT or UNSAT both OK)
        return True, "Valid ASP syntax (SAT or UNSAT)"
    except Exception as e:
        error_msg = str(e)
        if "syntax error" in error_msg.lower():
            return False, f"Syntax error: {error_msg}"
        elif "parse error" in error_msg.lower():
            return False, f"Parse error: {error_msg}"
        else:
            return False, f"ASP error: {error_msg}"

def load_jsonl(filename):
    """Load JSONL file and return list of entries"""
    entries = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    entries.append(entry)
                except json.JSONDecodeError as e:
                    print(f"Warning: Error parsing line {line_num}: {e}")
                    continue
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    return entries

def print_sample(entry, sample_num, validate_asp=False):
    """Print a formatted sample"""
    print(f"\n{'='*60}")
    print(f"SAMPLE {sample_num}")
    print('='*60)
    
    if 'instruction' in entry:
        print(f"Instruction: {entry['instruction']}")
        print()
    
    if 'input' in entry and 'output' in entry:
        print("INPUT (CNL):")
        print(f"  {entry['input']}")
        print()
        print("OUTPUT (ASP):")
        print(f"  {entry['output']}")
        
        # Validate ASP code if requested
        if validate_asp and 'output' in entry:
            asp_code = entry['output']
            is_valid, message = validate_asp_with_clingo(asp_code)
            
            if is_valid is None:  # Clingo not available
                print(f"  [Validation: {message}]")
            elif is_valid:
                print(f"  ✓ ASP Validation: {message}")
            else:
                print(f"  ✗ ASP Validation FAILED: {message}")
    else:
        # Handle other formats
        for key, value in entry.items():
            print(f"{key.upper()}:")
            print(f"  {value}")
            
            # Validate if this looks like ASP code
            if validate_asp and key.lower() in ['output', 'asp', 'asp_code']:
                is_valid, message = validate_asp_with_clingo(str(value))
                if is_valid is None:
                    print(f"  [Validation: {message}]")
                elif is_valid:
                    print(f"  ✓ ASP Validation: {message}")
                else:
                    print(f"  ✗ ASP Validation FAILED: {message}")
            print()

def main():
    parser = argparse.ArgumentParser(
        description="View random samples from JSONL training data files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python DataViewer.py data.jsonl --n 5
  python DataViewer.py data.jsonl --n 10 --validate
  python DataViewer.py data.jsonl --validate-all
  python DataViewer.py comprehensive_facts_cnl_to_asp_10k.jsonl --n 3 --validate
        """
    )
    
    parser.add_argument('filename', help='JSONL file to sample from')
    parser.add_argument('--n', type=int, default=5, 
                       help='Number of random samples to show (default: 5)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducible sampling')
    parser.add_argument('--validate', action='store_true',
                       help='Validate ASP code using clingo (requires clingo to be installed)')
    parser.add_argument('--validate-all', action='store_true',
                       help='Validate all entries in the dataset and show statistics')
    
    args = parser.parse_args()
    
    # Validate file exists
    if not Path(args.filename).exists():
        print(f"Error: File '{args.filename}' does not exist.")
        sys.exit(1)
    
    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
        print(f"Using random seed: {args.seed}")
    
    # Load data
    print(f"Loading data from: {args.filename}")
    entries = load_jsonl(args.filename)
    
    if not entries:
        print("Error: No valid entries found in the file.")
        sys.exit(1)
    
    print(f"Total entries: {len(entries):,}")
    
    # Validate all entries if requested
    if args.validate_all:
        print("\nValidating all ASP entries...")
        valid_count = 0
        invalid_count = 0
        no_clingo_warning = False
        
        for i, entry in enumerate(entries):
            if i % 100 == 0 and i > 0:
                print(f"  Validated {i:,} entries...")
            
            asp_code = None
            if 'output' in entry:
                asp_code = entry['output']
            elif 'asp' in entry:
                asp_code = entry['asp']
            
            if asp_code:
                is_valid, message = validate_asp_with_clingo(asp_code)
                if is_valid is None:
                    if not no_clingo_warning:
                        print(f"  Warning: {message}")
                        no_clingo_warning = True
                    break
                elif is_valid:
                    valid_count += 1
                else:
                    invalid_count += 1
                    if invalid_count <= 5:  # Show first 5 errors
                        print(f"  Invalid ASP at entry {i+1}: {message}")
                        print(f"    Code: {asp_code}")
        
        if not no_clingo_warning:
            total_validated = valid_count + invalid_count
            print(f"\nValidation Results:")
            print(f"  Total validated: {total_validated:,}")
            print(f"  Valid: {valid_count:,} ({valid_count/total_validated*100:.1f}%)")
            print(f"  Invalid: {invalid_count:,} ({invalid_count/total_validated*100:.1f}%)")
            
            if invalid_count > 0:
                print(f"  Warning: Found {invalid_count} invalid ASP entries!")
        
        if not args.validate:  # If only validating all, don't show samples
            return
    
    # Sample entries
    n_samples = min(args.n, len(entries))
    if n_samples < args.n:
        print(f"Warning: Requested {args.n} samples but only {n_samples} available.")
    
    sampled_entries = random.sample(entries, n_samples)
    
    print(f"\nShowing {n_samples} random samples:")
    
    # Display samples
    for i, entry in enumerate(sampled_entries, 1):
        print_sample(entry, i, validate_asp=args.validate or args.validate_all)
    
    print(f"\n{'='*60}")
    print(f"Displayed {n_samples} samples from {len(entries):,} total entries")

if __name__ == "__main__":
    main()
