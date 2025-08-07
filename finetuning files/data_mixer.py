#!/usr/bin/env python3
"""
Data Mixing Script for Curriculum Training

Creates mixed datasets from multiple construct directories with specified proportions.
"""

import argparse
import json
import random
import os
from pathlib import Path

def load_raw_data(construct_path):
    """Load raw.jsonl from a construct directory"""
    raw_file = Path(construct_path) / "data" / "raw.jsonl"
    
    if not raw_file.exists():
        raise FileNotFoundError(f"No raw.jsonl found at {raw_file}")
    
    data = []
    with open(raw_file, 'r') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                data.append(json.loads(line.strip()))
    
    return data

def parse_construct_specs(construct_specs):
    """Parse construct specifications like 'phase1/facts:20' into (path, percentage)"""
    parsed = []
    for spec in construct_specs:
        if ':' not in spec:
            raise ValueError(f"Invalid construct spec: {spec}. Expected format: 'path:percentage'")
        
        path, percentage = spec.rsplit(':', 1)
        try:
            percentage = float(percentage)
            if not 0 <= percentage <= 100:
                raise ValueError(f"Percentage must be 0-100, got {percentage}")
        except ValueError:
            raise ValueError(f"Invalid percentage in spec: {spec}")
        
        parsed.append((path, percentage))
    
    return parsed

def validate_percentages(construct_specs):
    """Validate that percentages sum to 100"""
    total = sum(percentage for _, percentage in construct_specs)
    if abs(total - 100.0) > 0.01:  # Allow small floating point errors
        raise ValueError(f"Percentages must sum to 100%, got {total}%")

def create_mixed_dataset(construct_specs, target_size=None, seed=42):
    """Create mixed dataset according to specifications"""
    random.seed(seed)
    
    # Load all data
    all_data = {}
    total_available = 0
    
    print("📂 Loading data from constructs:")
    for path, percentage in construct_specs:
        data = load_raw_data(path)
        all_data[path] = data
        construct_name = Path(path).name
        print(f"  {construct_name}: {len(data):,} examples ({percentage}%)")
        total_available += len(data)
    
    print(f"\n📊 Total available examples: {total_available:,}")
    
    # Calculate target size
    if target_size is None:
        target_size = total_available
        print(f"🎯 Target size: {target_size:,} (using all available)")
    else:
        print(f"🎯 Target size: {target_size:,}")
        if target_size > total_available:
            print(f"⚠️  Target size exceeds available data, using maximum: {total_available:,}")
            target_size = total_available
    
    # Calculate samples needed from each construct
    mixed_data = []
    actual_samples = {}
    
    print(f"\n🔀 Mixing data:")
    for path, percentage in construct_specs:
        requested_samples = int(target_size * percentage / 100)
        available_samples = len(all_data[path])
        actual_samples_count = min(requested_samples, available_samples)
        
        # Sample data
        if actual_samples_count == available_samples:
            sampled = all_data[path]
        else:
            sampled = random.sample(all_data[path], actual_samples_count)
        
        mixed_data.extend(sampled)
        actual_samples[path] = actual_samples_count
        
        construct_name = Path(path).name
        print(f"  {construct_name}: {actual_samples_count:,}/{available_samples:,} samples ({actual_samples_count/len(mixed_data)*100:.1f}%)")
    
    # Shuffle the final dataset
    random.shuffle(mixed_data)
    
    print(f"\n✅ Created mixed dataset: {len(mixed_data):,} examples")
    return mixed_data, actual_samples

def generate_filename(construct_specs, actual_samples):
    """Generate filename like mixed_facts-20_rules-30_constraints-50.jsonl"""
    parts = []
    for path, _ in construct_specs:
        construct_name = Path(path).name
        actual_count = actual_samples[path]
        total_samples = sum(actual_samples.values())
        actual_percentage = int(actual_count / total_samples * 100) if total_samples > 0 else 0
        parts.append(f"{construct_name}-{actual_percentage}")
    
    return f"mixed_{'_'.join(parts)}.jsonl"

def main():
    parser = argparse.ArgumentParser(
        description="Mix datasets from multiple constructs with specified proportions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Mix 60% facts, 40% rules, output to curriculum directory
  python mix_datasets.py phase1/facts:60 phase1/rules:40 --output curriculum/stage2_mixed --size 1000
  
  # Mix three constructs equally
  python mix_datasets.py phase1/facts:33.3 phase1/rules:33.3 phase1/constraints:33.4 --output phase1/mixed
  
  # Use all available data with custom proportions
  python mix_datasets.py phase1/facts:20 phase1/rules:20 phase1/constraints:60 --output phase1/constraints
        """
    )
    
    parser.add_argument(
        "constructs", 
        nargs="+",
        help="Construct specifications in format 'path:percentage' (e.g., phase1/facts:60)"
    )
    
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output directory where mixed dataset will be saved"
    )
    
    parser.add_argument(
        "--size", "-s",
        type=int,
        default=None,
        help="Target dataset size (default: use all available data)"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible sampling (default: 42)"
    )
    
    args = parser.parse_args()
    
    try:
        # Parse and validate inputs
        construct_specs = parse_construct_specs(args.constructs)
        validate_percentages(construct_specs)
        
        print("🎯 Dataset Mixing Configuration:")
        print("=" * 50)
        for path, percentage in construct_specs:
            construct_name = Path(path).name
            print(f"  {construct_name}: {percentage}%")
        print(f"  Output: {args.output}")
        if args.size:
            print(f"  Target size: {args.size:,}")
        print()
        
        # Create mixed dataset
        mixed_data, actual_samples = create_mixed_dataset(
            construct_specs, 
            target_size=args.size,
            seed=args.seed
        )
        
        # Generate output filename
        filename = generate_filename(construct_specs, actual_samples)
        
        # Create output directory and file
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure data subdirectory exists
        data_dir = output_dir / "data"
        data_dir.mkdir(exist_ok=True)
        
        output_file = data_dir / filename
        
        # Write mixed dataset
        print(f"💾 Writing mixed dataset...")
        with open(output_file, 'w') as f:
            for example in mixed_data:
                f.write(json.dumps(example) + '\n')
        
        print(f"✅ Mixed dataset created successfully!")
        print(f"📁 Location: {output_file}")
        print(f"📊 Final size: {len(mixed_data):,} examples")
        
        # Print summary
        print(f"\n📋 Final Composition:")
        total_samples = sum(actual_samples.values())
        for path, _ in construct_specs:
            construct_name = Path(path).name
            count = actual_samples[path]
            percentage = count / total_samples * 100 if total_samples > 0 else 0
            print(f"  {construct_name}: {count:,} examples ({percentage:.1f}%)")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
