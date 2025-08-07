import os
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

def load_model(checkpoint_path):
    """Load the fine-tuned model"""
    print(f"🔹 Loading model from: {checkpoint_path}")
    
    base_model = "microsoft/phi-2"
    
    # Load tokenizer
    print("🔹 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load base model
    print("🔹 Loading base model...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )
    
    base = AutoModelForCausalLM.from_pretrained(
        base_model,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    
    # Apply LoRA
    print(f"🔹 Applying LoRA from checkpoint...")
    model = PeftModel.from_pretrained(base, checkpoint_path)
    model.eval()
    
    print("✅ Model loaded successfully!")
    return model, tokenizer

def generate_response(model, tokenizer, prompt, max_tokens=64, temperature=0.0):
    """Generate ASP code from prompt - FIXED to allow multi-line"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=max_tokens,
            do_sample=temperature > 0,
            temperature=temperature if temperature > 0 else None,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    
    # Extract only the generated part
    prompt_length = inputs["input_ids"].shape[1]
    generated_ids = outputs[0][prompt_length:]
    generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)
    
    # ONLY strip whitespace - DON'T truncate at newlines!
    generated_text = generated_text.strip()
    
    # Optional: Clean up any trailing incomplete lines
    if generated_text and not generated_text.endswith('.'):
        # If doesn't end with period, might be incomplete
        lines = generated_text.split('\n')
        complete_lines = []
        for line in lines:
            if line.strip().endswith('.'):
                complete_lines.append(line)
            elif line.strip() and not line.strip().endswith('.'):
                # Incomplete line - only keep if it's the only line
                if len(lines) == 1:
                    complete_lines.append(line)
                break
        if complete_lines:
            generated_text = '\n'.join(complete_lines)
    
    return generated_text

def interactive_session(model, tokenizer):
    """Run interactive session"""
    # Default instruction (matching your training data)
    DEFAULT_INSTRUCTION = "Translate this to ASP code"
    
    print("\n" + "="*60)
    print("🤖 Interactive ASP Code Generator")
    print("="*60)
    print(f"Default instruction: '{DEFAULT_INSTRUCTION}'")
    print("\nCommands:")
    print("  'quit' or 'exit' - Exit the program")
    print("  'help' - Show this help")
    print("  'temp X' - Set temperature (0.0-1.0, default: 0.0)")
    print("  'instruction: <text>' - Change instruction")
    print("  'tokens X' - Set max tokens (default: 256)")
    print("  'debug' - Toggle debug mode")
    print("  Just type your input to get ASP code!")
    print("-"*60)
    
    current_instruction = DEFAULT_INSTRUCTION
    temperature = 0.0
    max_tokens = 256  # Increased default for multi-line
    debug_mode = False
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 Input: ").strip()
            
            if not user_input:
                continue
                
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            elif user_input.lower() == 'help':
                print("\nCommands:")
                print("  'quit' or 'exit' - Exit the program")
                print("  'help' - Show this help")
                print("  'temp X' - Set temperature (0.0-1.0)")
                print("  'instruction: <text>' - Change instruction")
                print("  'tokens X' - Set max tokens")
                print("  'debug' - Toggle debug mode")
                print("  Just type your input to get ASP code!")
                continue
                
            elif user_input.lower() == 'debug':
                debug_mode = not debug_mode
                print(f"🔧 Debug mode: {'ON' if debug_mode else 'OFF'}")
                continue
                
            elif user_input.startswith('temp '):
                try:
                    temperature = float(user_input.split(' ', 1)[1])
                    temperature = max(0.0, min(1.0, temperature))
                    print(f"🌡️ Temperature set to: {temperature}")
                except:
                    print("❌ Invalid temperature. Use: temp 0.5")
                continue
                
            elif user_input.startswith('instruction: '):
                current_instruction = user_input.split(': ', 1)[1]
                print(f"📝 Instruction changed to: '{current_instruction}'")
                continue
                
            elif user_input.startswith('tokens '):
                try:
                    max_tokens = int(user_input.split(' ', 1)[1])
                    max_tokens = max(1, min(512, max_tokens))
                    print(f"🔢 Max tokens set to: {max_tokens}")
                except:
                    print("❌ Invalid token count. Use: tokens 256")
                continue
            
            # Generate ASP code
            prompt = f"{current_instruction}: {user_input}\nResponse:"
            
            if debug_mode:
                print(f"🔧 Debug - Full prompt: '{prompt}'")
                print(f"🔧 Debug - Settings: temp={temperature}, tokens={max_tokens}")
            
            print(f"🤔 Thinking...")
            
            # Generate response
            asp_code = generate_response(model, tokenizer, prompt, max_tokens, temperature)
            
            # Display result with proper formatting
            print(f"🎯 ASP Code:")
            if '\n' in asp_code:
                # Multi-line output - format nicely
                print("=" * 50)
                for i, line in enumerate(asp_code.split('\n'), 1):
                    if line.strip():
                        print(f"{i:2d}: {line}")
                print("=" * 50)
            else:
                # Single line output
                print("=" * 50)
                print(f"    {asp_code}")
                print("=" * 50)
            
            if debug_mode:
                print(f"🔧 Debug - Raw output: '{asp_code}'")
                print(f"🔧 Debug - Character count: {len(asp_code)}")
                print(f"🔧 Debug - Line count: {len(asp_code.split('n')) if asp_code else 0}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            if debug_mode:
                import traceback
                traceback.print_exc()
            continue

def main():
    print("🚀 ASP Code Generator - Interactive Mode")
    
    # Parse command line arguments
    if len(sys.argv) != 2:
        print("\nUsage: python interactive_asp.py <checkpoint_path>")
        print("\nExamples:")
        print("  python interactive_asp.py ./final_production_model")
        print("  python interactive_asp.py ./interrupted_model")
        print("  python interactive_asp.py ./test_results/checkpoint-420")
        sys.exit(1)
    
    checkpoint_path = sys.argv[1]
    
    # Check if checkpoint exists
    if not os.path.exists(checkpoint_path):
        print(f"❌ Checkpoint path does not exist: {checkpoint_path}")
        sys.exit(1)
    
    try:
        # Load model
        model, tokenizer = load_model(checkpoint_path)
        
        # Start interactive session
        interactive_session(model, tokenizer)
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
