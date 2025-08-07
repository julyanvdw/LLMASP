import os

# CRITICAL: Set HF cache BEFORE any imports (same as finetune script)
os.environ["HF_HOME"] = "./cache"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Now import everything else
import json
import argparse
import random
from datetime import datetime
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from Evaluator import create_evaluator

# =====================================================
# CONFIGURATION PARAMETERS
# =====================================================
DEFAULT_N_EXAMPLES = 100        # Default number of test examples to evaluate
MAX_NEW_TOKENS = 400           # Maximum tokens to generate
SEED = 42                      # Random seed for reproducible sampling
TASK_TYPE = 'cnl-asp'          # Default task type

def load_test_data(data_path: str, n_examples: int = DEFAULT_N_EXAMPLES, seed: int = SEED) -> list:
    """Load test data from jsonl file"""
    test_file = os.path.join(data_path, 'data', 'raw.jsonl')
    
    if not os.path.exists(test_file):
        raise FileNotFoundError(f"Test file not found: {test_file}")
    
    # Load all test examples
    examples = []
    with open(test_file, 'r') as f:
        for line in f:
            examples.append(json.loads(line.strip()))
    
    # Sample n examples if specified and less than total
    if n_examples and n_examples < len(examples):
        random.seed(seed)
        examples = random.sample(examples, n_examples)
        print(f"📋 Sampled {len(examples)} test examples from {test_file}")
    else:
        print(f"📋 Loaded all {len(examples)} test examples from {test_file}")
    
    return examples

def load_model_and_tokenizer(checkpoint_path: str = None):
    """Load model and tokenizer - uses cached models like finetune script"""
    
    if checkpoint_path is None or checkpoint_path.lower() == 'base':
        # Load base phi-2 model from cache (same as finetune script)
        model_name = 'microsoft/phi-2'
        print(f"🔄 Loading base model: {model_name}")
        print(f"📁 Using HF cache: {os.environ.get('HF_HOME')}")
        
        # Load from cache (same pattern as finetune script)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        
        source_type = "base"
        source_name = "phi2-base"
        
    else:
        # Load fine-tuned checkpoint
        if not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
        
        print(f"🔄 Loading fine-tuned model from {checkpoint_path}")
        
        # Load tokenizer from base model (same as finetune script approach)
        base_model = 'microsoft/phi-2'
        tokenizer = AutoTokenizer.from_pretrained(base_model)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load fine-tuned model
        model = AutoModelForCausalLM.from_pretrained(
            checkpoint_path,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        
        source_type = "checkpoint"
        # Extract source construct from checkpoint path
        path_parts = checkpoint_path.rstrip('/').split('/')
        if 'phase1' in path_parts:
            phase1_idx = path_parts.index('phase1')
            if phase1_idx + 1 < len(path_parts):
                source_name = path_parts[phase1_idx + 1]
            else:
                source_name = "unknown"
        else:
            source_name = os.path.basename(os.path.dirname(checkpoint_path))
    
    model.eval()
    print(f"✅ Model loaded successfully")
    
    return model, tokenizer, source_type, source_name

def generate_predictions(model, tokenizer, examples: list, max_new_tokens: int = MAX_NEW_TOKENS) -> list:
    """Generate predictions for test examples"""
    predictions = []
    
    print(f"🚀 Generating predictions for {len(examples)} examples...")
    
    for i, example in enumerate(examples):
        # Format input prompt (same as finetune script)
        input_text = example['input']
        prompt = f"Instruction: {example.get('instruction', 'Convert to ASP')}\nInput: {input_text}\nOutput:"
        
        # Tokenize
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=1024
        ).to(model.device)
        
        # Generate (same parameters as finetune script)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        
        # Decode prediction
        input_length = inputs['input_ids'].shape[1]
        generated_tokens = outputs[0][input_length:]
        prediction = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
        
        predictions.append(prediction)
        
        if (i + 1) % 25 == 0:
            print(f"  Generated {i + 1}/{len(examples)} predictions")
    
    print(f"✅ Generated {len(predictions)} predictions")
    return predictions

def create_output_filename(target_construct: str, source_name: str, source_type: str) -> str:
    """Create standardized output filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if source_type == "base":
        filename = f"BASELINE-{target_construct}-vs-{source_name}-{timestamp}.txt"
    else:
        filename = f"TRANSFER-{target_construct}-from-{source_name}-{timestamp}.txt"
    
    return filename

def create_enhanced_metadata(source_name: str, source_type: str, target_construct: str, 
                           checkpoint_path: str, data_path: str, test_examples: int) -> dict:
    """Create enhanced metadata for the evaluator report"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    metadata = {
        'evaluation_timestamp': timestamp,
        'source_model': source_name,
        'source_type': source_type,
        'target_construct': target_construct,
        'data_path': data_path,
        'test_examples': test_examples,
        'evaluation_type': 'transfer_learning' if source_type != 'base' else 'baseline'
    }
    
    if checkpoint_path and checkpoint_path.lower() != 'base':
        metadata['checkpoint_path'] = checkpoint_path
    else:
        metadata['base_model'] = 'microsoft/phi-2'
        metadata['hf_cache'] = os.environ.get('HF_HOME', 'default')
    
    return metadata

class EnhancedCNLToASPEvaluator:
    """Enhanced evaluator that adds inputs to detailed results for better reporting"""
    
    def __init__(self, base_evaluator):
        self.base_evaluator = base_evaluator
        self.enable_semantic = base_evaluator.enable_semantic
    
    def evaluate_with_inputs(self, predictions: list, targets: list, inputs: list) -> dict:
        """Evaluate predictions and add input information to results"""
        
        # Run base evaluation
        results = self.base_evaluator.evaluate(predictions, targets)
        
        # Add inputs to detailed results
        for i, result in enumerate(results['detailed_results']):
            if i < len(inputs):
                result['input'] = inputs[i]
        
        return results
    
    def get_evaluation_summary(self, results: dict) -> str:
        """Get evaluation summary from base evaluator"""
        return self.base_evaluator.get_evaluation_summary(results)
    
    def save_enhanced_evaluation_report(self, results: dict, output_path: str, 
                                      metadata: dict = None):
        """Save enhanced evaluation report with full input/target/prediction display"""
        
        with open(output_path, 'w') as f:
            # Write enhanced header
            f.write("=" * 120 + "\n")
            if metadata and metadata.get('evaluation_type') == 'baseline':
                f.write("🔍 BASE MODEL EVALUATION REPORT\n")
            else:
                f.write("🔄 TRANSFER LEARNING EVALUATION REPORT\n")
            f.write("=" * 120 + "\n")
            
            if metadata:
                f.write(f"🕒 Evaluation Timestamp: {metadata.get('evaluation_timestamp', 'Unknown')}\n")
                f.write(f"🎯 Source Model: {metadata.get('source_model', 'Unknown')} ({metadata.get('source_type', 'Unknown')})\n")
                f.write(f"📋 Target Construct: {metadata.get('target_construct', 'Unknown')}\n")
                
                if metadata.get('checkpoint_path'):
                    f.write(f"🔧 Checkpoint Path: {metadata['checkpoint_path']}\n")
                elif metadata.get('base_model'):
                    f.write(f"🔧 Model: {metadata['base_model']} (base)\n")
                    f.write(f"📁 HF Cache: {metadata.get('hf_cache', 'default')}\n")
                
                f.write(f"📁 Data Path: {metadata.get('data_path', 'Unknown')}\n")
                f.write(f"🧪 Test Examples: {metadata.get('test_examples', 'Unknown')}\n")
            
            f.write("\n")
            
            # Write evaluation summary (includes error cases and metrics)
            f.write(self.get_evaluation_summary(results))
            f.write("\n\n")
            
            # Write detailed test cases with enhanced formatting
            f.write("📋 INDIVIDUAL TEST CASES (FULL OUTPUT)\n")
            f.write("=" * 120 + "\n\n")
            
            for result in results['detailed_results']:
                test_num = result['test_case']
                
                # Status indicator
                if result['exact_match']:
                    status = "✅ EXACT MATCH"
                elif result.get('semantic_match') and self.enable_semantic:
                    status = "🎯 SEMANTIC MATCH"
                elif result['syntax_valid']:
                    status = "🔧 SYNTAX VALID"
                elif result['non_empty']:
                    status = "❌ SYNTAX ERROR"
                else:
                    status = "🔴 EMPTY OUTPUT"
                
                f.write(f"{status} - Test Case {test_num}\n")
                f.write("─" * 80 + "\n")
                
                # Input section
                if 'input' in result:
                    f.write("INPUT:\n")
                    input_lines = result['input'].split('\n') if result['input'] else ['']
                    for line in input_lines:
                        f.write(f"  {line}\n")
                    f.write("\n")
                
                # Target section with box formatting
                f.write("TARGET:\n")
                f.write("┌" + "─" * 100 + "┐\n")
                target_lines = result['target'].split('\n') if result['target'] else ['']
                for line in target_lines:
                    # Handle very long lines by wrapping
                    while line:
                        chunk = line[:96]  # Leave space for box borders
                        f.write(f"│ {chunk:<98} │\n")
                        line = line[96:] if len(line) > 96 else ""
                if not target_lines or not target_lines[0]:
                    f.write(f"│ {'(empty)':<98} │\n")
                f.write("└" + "─" * 100 + "┘\n\n")
                
                # Predicted section with box formatting
                f.write("PREDICTED:\n")
                f.write("┌" + "─" * 100 + "┐\n")
                predicted_lines = result['predicted'].split('\n') if result['predicted'] else ['']
                for line in predicted_lines:
                    # Handle very long lines by wrapping
                    while line:
                        chunk = line[:96]  # Leave space for box borders
                        f.write(f"│ {chunk:<98} │\n")
                        line = line[96:] if len(line) > 96 else ""
                if not predicted_lines or not predicted_lines[0]:
                    f.write(f"│ {'(empty)':<98} │\n")
                f.write("└" + "─" * 100 + "┘\n\n")
                
                # Analysis section
                target_chars = len(result['target']) if result['target'] else 0
                pred_chars = len(result['predicted']) if result['predicted'] else 0
                f.write(f"📏 Lengths: Target={target_chars} chars, Predicted={pred_chars} chars\n")
                
                f.write(f"\n🔍 Analysis:\n")
                f.write(f"   ✅ Exact Match:    {result['exact_match']}\n")
                f.write(f"   🔧 Syntax Valid:   {result['syntax_valid']}\n")
                if self.enable_semantic:
                    f.write(f"   🎯 Semantic Match: {result['semantic_match']}\n")
                f.write(f"   📝 Non-empty:      {result['non_empty']}\n")
                
                if result.get('error_type'):
                    f.write(f"   ⚠️ Error Type:     {result['error_type']}\n")
                
                if result.get('clingo_analysis'):
                    f.write(f"   🔍 Clingo Analysis:\n")
                    clingo_info = result['clingo_analysis']
                    if clingo_info.get('predicted_errors'):
                        for error in clingo_info['predicted_errors']:
                            f.write(f"      {error}\n")
                
                f.write("\n")

def main():
    parser = argparse.ArgumentParser(description="Transfer Learning Evaluator")
    parser.add_argument('--data_path', type=str, required=True,
                       help='Path to target construct data (e.g., phase1/rules)')
    parser.add_argument('--checkpoint_path', type=str, default=None,
                       help='Path to source construct checkpoint (default: base phi-2 model)')
    parser.add_argument('--n_examples', type=int, default=DEFAULT_N_EXAMPLES,
                       help=f'Number of test examples to evaluate (default: {DEFAULT_N_EXAMPLES})')
    parser.add_argument('--max_new_tokens', type=int, default=MAX_NEW_TOKENS,
                       help=f'Maximum new tokens to generate (default: {MAX_NEW_TOKENS})')
    parser.add_argument('--seed', type=int, default=SEED,
                       help=f'Random seed for sampling examples (default: {SEED})')
    parser.add_argument('--task_type', type=str, default=TASK_TYPE,
                       choices=['cnl-asp', 'asp', 'nl-cnl', 'nl'],
                       help=f'Task type for evaluation (default: {TASK_TYPE})')
    parser.add_argument('--enable_semantic', action='store_true', default=True,
                       help='Enable semantic evaluation using Clingo answer sets')
    
    args = parser.parse_args()
    
    # Extract construct names from paths
    target_construct = os.path.basename(args.data_path.rstrip('/'))
    
    if args.checkpoint_path is None:
        print("🔍 BASE MODEL EVALUATION")
        print("=" * 50)
        print(f"🎯 Evaluating base phi-2 model on {target_construct} data")
    else:
        print("🔄 TRANSFER LEARNING EVALUATION")
        print("=" * 50)
        source_construct = os.path.basename(os.path.dirname(args.checkpoint_path.rstrip('/')))
        print(f"🎯 Transfer: {source_construct} → {target_construct}")
    
    print(f"📁 Data: {args.data_path}")
    print(f"🧪 Test examples: {args.n_examples}")
    if args.checkpoint_path:
        print(f"🔧 Checkpoint: {args.checkpoint_path}")
    else:
        print(f"🔧 Model: microsoft/phi-2 (base)")
    print(f"🎯 Semantic evaluation: {'enabled' if args.enable_semantic else 'disabled'}")
    print("")
    
    try:
        # Load test data
        test_examples = load_test_data(args.data_path, args.n_examples, args.seed)
        
        # Load model and tokenizer
        model, tokenizer, source_type, source_name = load_model_and_tokenizer(args.checkpoint_path)
        
        # Generate predictions
        predictions = generate_predictions(model, tokenizer, test_examples, args.max_new_tokens)
        
        # Extract targets and inputs
        targets = [example['output'] for example in test_examples]
        inputs = [example['input'] for example in test_examples]
        
        # Create evaluator with semantic evaluation
        print("🔍 Running evaluation...")
        base_evaluator = create_evaluator(args.task_type, enable_semantic=args.enable_semantic)
        enhanced_evaluator = EnhancedCNLToASPEvaluator(base_evaluator)
        
        # Evaluate with inputs included
        eval_results = enhanced_evaluator.evaluate_with_inputs(predictions, targets, inputs)
        
        # Print summary to console
        print("\n" + "=" * 60)
        if source_type == "base":
            print("📊 BASELINE EVALUATION SUMMARY")
        else:
            print("📊 TRANSFER EVALUATION SUMMARY")
        print("=" * 60)
        print(enhanced_evaluator.get_evaluation_summary(eval_results))
        
        # Create metadata for report
        metadata = create_enhanced_metadata(
            source_name, source_type, target_construct,
            args.checkpoint_path, args.data_path, len(test_examples)
        )
        
        # Create output file path
        target_dir = f"phase1/{target_construct}"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        filename = create_output_filename(target_construct, source_name, source_type)
        output_path = os.path.join(target_dir, filename)
        
        # Save enhanced evaluation report
        enhanced_evaluator.save_enhanced_evaluation_report(eval_results, output_path, metadata)
        
        # Final output
        if source_type == "base":
            print(f"🎉 Baseline evaluation completed!")
        else:
            print(f"🎉 Transfer evaluation completed!")
        print(f"💾 Results saved: {filename}")
        print(f"📄 Full path: {output_path}")
        
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
