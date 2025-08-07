import os
import argparse

# CRITICAL: Set HF cache BEFORE any imports
os.environ["HF_HOME"] = "./cache"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Now import everything else
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    BitsAndBytesConfig,
    EarlyStoppingCallback,
    TrainerCallback
)
from peft import LoraConfig, get_peft_model, TaskType, PeftModel
from datasets import load_dataset
import torch
import numpy as np
import json
import pandas as pd
import random
from datetime import datetime
import time
from sklearn.model_selection import train_test_split

# Import the new evaluator
from Evaluator import create_evaluator

# =============================================================================
# TRAINING CONFIGURATION PARAMETERS
# =============================================================================

#Filename
FILENAME = "raw.jsonl"

# Data Split
TEST_SIZE = 100                             # Number of examples to hold out for testing

# Checkpoint and Evaluation Strategy (Combined)
EVAL_AND_SAVE_STEPS = 200                  # How often to evaluate AND save (combined)
KEEP_CHECKPOINTS = 3                       # Keep last 3 checkpoints total

# Metrics and Logging  
METRICS_LOG_STEPS = 10                   # How often to log detailed metrics to text files
PRINT_LOG_STEPS = 10			  # How often logs are printed

# Early Stopping and Plateau Detection
ENABLE_EARLY_STOPPING = True               # Set to False to disable early stopping
EARLY_STOPPING_PATIENCE = 3                # How many evals without improvement before stopping
EARLY_STOPPING_THRESHOLD = 0.01           # Minimum improvement to count as progress
PLATEAU_PATIENCE_STEPS = 200               # Steps to look back for plateau detection
OVERFITTING_THRESHOLD = 0.01               # Train vs eval loss divergence threshold

# Training Parameters
MAX_LENGTH = 512                           # Token sequence length
LEARNING_RATE = 2e-5                      # Base learning rate
BATCH_SIZE = 1                            # Per device batch size
GRADIENT_ACCUMULATION = 8                 # Gradient accumulation steps
NUM_EPOCHS = 3                            # Maximum training epochs
SCHEDULER_TYPE = "constant"               # Type of scheduler
WARMUP_STEPS = 100                        # Spreading out the learning rate

# Generation Parameters
MAX_NEW_TOKENS = 150   			  # Reduced for faster evaluation
MIN_NEW_TOKENS = 0                        # Allow early stopping

# Model Configuration
BASE_MODEL_NAME = "microsoft/phi-2"        # Base model to use
LORA_R = 32                               # LoRA rank
LORA_ALPHA = 64                           # LoRA alpha
LORA_DROPOUT = 0.05                       # LoRA dropout

# =============================================================================
# DIRECTORY MANAGEMENT FUNCTIONS
# =============================================================================

def create_timestamped_dirs(construct_path):
    """Create timestamped subdirectories for results and models"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create timestamped directories
    results_dir = f"{construct_path}/results/{timestamp}"
    models_dir = f"{construct_path}/trained_models/{timestamp}"
    
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    # Create symlinks to "latest" for convenience
    latest_results = f"{construct_path}/results/latest"
    latest_models = f"{construct_path}/trained_models/latest"
    
    # Remove existing symlinks if they exist
    if os.path.islink(latest_results):
        os.unlink(latest_results)
    if os.path.islink(latest_models):
        os.unlink(latest_models)
    
    # Create new symlinks (relative paths for portability)
    try:
        os.symlink(timestamp, latest_results)
        os.symlink(timestamp, latest_models)
    except OSError:
        # Symlinks might not work on all systems, create info files instead
        with open(latest_results + "_info.txt", 'w') as f:
            f.write(f"Latest run: {timestamp}\nFull path: {results_dir}\n")
        with open(latest_models + "_info.txt", 'w') as f:
            f.write(f"Latest run: {timestamp}\nFull path: {models_dir}\n")
    
    print(f"📁 Created timestamped directories:")
    print(f"  Results: {results_dir}")
    print(f"  Models:  {models_dir}")
    
    return results_dir, models_dir, timestamp

def list_previous_runs(construct_path):
    """List all previous training runs"""
    results_base = f"{construct_path}/results"
    models_base = f"{construct_path}/trained_models"
    
    if not os.path.exists(results_base):
        return []
    
    # Get all timestamped directories
    runs = []
    for item in os.listdir(results_base):
        item_path = os.path.join(results_base, item)
        if os.path.isdir(item_path) and item.replace("_", "").isdigit():
            # Parse timestamp
            try:
                timestamp = datetime.strptime(item, "%Y%m%d_%H%M%S")
                runs.append({
                    'timestamp_str': item,
                    'timestamp': timestamp,
                    'results_dir': item_path,
                    'models_dir': os.path.join(models_base, item)
                })
            except ValueError:
                continue  # Skip non-timestamp directories
    
    # Sort by timestamp (newest first)
    runs.sort(key=lambda x: x['timestamp'], reverse=True)
    return runs

# =============================================================================
# SIMPLIFIED EVALUATION LOGGER
# =============================================================================

class EvaluationLogger:
    """Simplified logger that focuses on training curves and plateau detection"""
    def __init__(self, results_dir, construct_name, timestamp):
        self.results_dir = results_dir
        self.construct_name = construct_name
        self.timestamp = timestamp
        self.metrics_file = f"{results_dir}/training_metrics.txt"
        self.curves_file = f"{results_dir}/loss_curves.txt"
        self.run_info_file = f"{results_dir}/run_info.txt"
        
        self.start_time = datetime.now()
        self.train_losses = []
        self.eval_losses = []
        self.plateau_detected = False
        self.plateau_step = None
        self.examples_at_plateau = None
        
        # Create run info file
        self._create_run_info()
        
        # Initialize curves file with header
        with open(self.curves_file, 'w') as f:
            f.write("step,epoch,examples_seen,train_loss,eval_loss,learning_rate,perplexity,token_accuracy,plateau_detected,wall_time\n")
    
    def _create_run_info(self):
        """Create a run info file with metadata"""
        with open(self.run_info_file, 'w') as f:
            f.write("=== TRAINING RUN INFORMATION ===\n")
            f.write(f"Timestamp: {self.timestamp}\n")
            f.write(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Construct: {self.construct_name}\n")
            f.write(f"Results Directory: {self.results_dir}\n\n")
            
            f.write("=== HYPERPARAMETERS ===\n")
            f.write(f"MAX_LENGTH: {MAX_LENGTH}\n")
            f.write(f"LEARNING_RATE: {LEARNING_RATE}\n")
            f.write(f"BATCH_SIZE: {BATCH_SIZE}\n")
            f.write(f"GRADIENT_ACCUMULATION: {GRADIENT_ACCUMULATION}\n")
            f.write(f"NUM_EPOCHS: {NUM_EPOCHS}\n")
            f.write(f"LORA_R: {LORA_R}\n")
            f.write(f"LORA_ALPHA: {LORA_ALPHA}\n")
            f.write(f"LORA_DROPOUT: {LORA_DROPOUT}\n")
            f.write(f"EVAL_AND_SAVE_STEPS: {EVAL_AND_SAVE_STEPS}\n")
            f.write(f"EARLY_STOPPING: {ENABLE_EARLY_STOPPING}\n")
    
    def detect_plateau(self, patience_evals=None):
        """Detect plateau by monitoring train vs eval loss divergence"""
        if patience_evals is None:
            patience_evals = PLATEAU_PATIENCE_STEPS // METRICS_LOG_STEPS
        
        if len(self.train_losses) < patience_evals:
            return False, None
        
        # Look at recent window
        recent_train = self.train_losses[-patience_evals:]
        recent_eval = self.eval_losses[-patience_evals:]
        
        # Check if training loss keeps decreasing but eval loss stagnates/increases
        train_improvement = recent_train[0] - recent_train[-1]  # Positive = improving
        eval_improvement = recent_eval[0] - recent_eval[-1]
        
        # Plateau if: train still improving but eval stopped/getting worse
        overfitting = (train_improvement > OVERFITTING_THRESHOLD) and (eval_improvement < OVERFITTING_THRESHOLD/2)
        
        plateau_step = len(self.train_losses) - patience_evals if overfitting else None
        return overfitting, plateau_step
    
    def log_training_step(self, step, epoch, train_loss, eval_loss, learning_rate, perplexity, token_accuracy):
        """Log step data to curves file"""
        self.train_losses.append(train_loss)
        self.eval_losses.append(eval_loss)
        
        # Check for plateau
        if not self.plateau_detected:
            is_plateau, plateau_step_idx = self.detect_plateau()
            if is_plateau:
                self.plateau_detected = True
                self.plateau_step = (plateau_step_idx + 1) * METRICS_LOG_STEPS  # Convert back to actual step
                self.examples_at_plateau = self.plateau_step * BATCH_SIZE * GRADIENT_ACCUMULATION
                print(f"🔄 Plateau detected at step {self.plateau_step} ({self.examples_at_plateau:,} examples)")
        
        # Calculate wall time
        wall_time = (datetime.now() - self.start_time).total_seconds()
        examples_seen = step * BATCH_SIZE * GRADIENT_ACCUMULATION
        
        # Write to curves file
        with open(self.curves_file, 'a') as f:
            f.write(f"{step},{epoch:.2f},{examples_seen},{train_loss:.6f},{eval_loss:.6f},")
            f.write(f"{learning_rate:.8f},{perplexity:.3f},{token_accuracy:.1f},{self.plateau_detected},{wall_time:.1f}\n")
    
    def finalize_training_summary(self, final_metrics, train_dataset_size, eval_dataset_size, start_model_info, task_type):
        """Write final summary to metrics file"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        with open(self.metrics_file, 'w') as f:
            f.write("=== TRAINING METRICS SUMMARY ===\n")
            f.write(f"Timestamp: {self.timestamp}\n")
            f.write(f"Construct: {self.construct_name}\n")
            f.write(f"Task Type: {task_type}\n")
            f.write(f"Training Start: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Training End: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Duration: {str(duration).split('.')[0]}\n\n")
            
            f.write("=== MODEL INFO ===\n")
            f.write(f"Starting Model: {start_model_info['type']}\n")
            f.write(f"Model Path: {start_model_info['path']}\n")
            if start_model_info['type'] == 'checkpoint':
                f.write(f"Previous Training: {start_model_info['description']}\n")
            f.write("\n")
            
            f.write("=== DATASET INFO ===\n")
            f.write(f"Training Examples: {train_dataset_size:,}\n")
            f.write(f"Evaluation Examples: {eval_dataset_size:,}\n")
            f.write(f"Total Tokens Processed: {final_metrics.get('total_tokens', 'N/A'):,}\n\n")
            
            f.write("=== PLATEAU DETECTION ===\n")
            f.write(f"Plateau Detected: {'Yes' if self.plateau_detected else 'No'}\n")
            if self.plateau_detected:
                f.write(f"Plateau Step: {self.plateau_step:,}\n")
                f.write(f"Examples Seen at Plateau: {self.examples_at_plateau:,}\n")
                f.write(f"Plateau Criteria: Train vs eval loss divergence (threshold: {OVERFITTING_THRESHOLD})\n")
            
            f.write(f"\n=== EARLY STOPPING CONFIG ===\n")
            f.write(f"Early Stopping Enabled: {'Yes' if ENABLE_EARLY_STOPPING else 'No'}\n")
            if ENABLE_EARLY_STOPPING:
                f.write(f"Early Stopping Patience: {EARLY_STOPPING_PATIENCE} evaluations\n")
                f.write(f"Early Stopping Threshold: {EARLY_STOPPING_THRESHOLD}\n")
            
            f.write(f"\n=== FINAL PERFORMANCE ===\n")
            f.write(f"Final Training Loss: {final_metrics.get('train_loss', 0):.6f}\n")
            f.write(f"Final Validation Loss: {final_metrics.get('eval_loss', 0):.6f}\n")
            f.write(f"Final Exact Match Rate: {final_metrics.get('exact_match_rate', 0):.1%}\n")
            if task_type == 'cnl-asp':
                f.write(f"Final Syntax Valid Rate: {final_metrics.get('syntax_valid_rate', 0):.1%}\n")
                f.write(f"Final Semantic Match Rate: {final_metrics.get('semantic_match_rate', 0):.1%}\n")
            f.write(f"Final Perplexity: {final_metrics.get('perplexity', 0):.3f}\n")
            
            total_steps = len(self.train_losses) * METRICS_LOG_STEPS if self.train_losses else 0
            total_examples = total_steps * BATCH_SIZE * GRADIENT_ACCUMULATION
            f.write(f"\n=== EFFICIENCY METRICS ===\n")
            f.write(f"Total Training Steps: {total_steps:,}\n")
            f.write(f"Total Examples Processed: {total_examples:,}\n")
            f.write(f"Training Time: {duration.total_seconds()/3600:.2f} hours\n")
            if duration.total_seconds() > 0:
                examples_per_sec = total_examples / duration.total_seconds()
                f.write(f"Examples per Second: {examples_per_sec:.2f}\n")
        
        # Update run info with completion
        with open(self.run_info_file, 'a') as f:
            f.write(f"\n=== COMPLETION INFO ===\n")
            f.write(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Duration: {str(duration).split('.')[0]}\n")
            f.write(f"Task Type: {task_type}\n")
            f.write(f"Final Exact Match Rate: {final_metrics.get('exact_match_rate', 0):.1%}\n")
            if task_type == 'cnl-asp':
                f.write(f"Final Syntax Valid Rate: {final_metrics.get('syntax_valid_rate', 0):.1%}\n")
                f.write(f"Final Semantic Match Rate: {final_metrics.get('semantic_match_rate', 0):.1%}\n")
            f.write(f"Final Loss: {final_metrics.get('eval_loss', 0):.6f}\n")

# =============================================================================
# DATA PROCESSING FUNCTIONS (UNCHANGED)
# =============================================================================

def create_train_test_split(data_dir, test_size=TEST_SIZE):
    """Load FILENAME and split into train/test"""
    print(f"🔹 Loading and splitting data...")
    
    # Load raw data
    raw_file = f"{data_dir}/{FILENAME}"
    if not os.path.exists(raw_file):
        raise FileNotFoundError(f"Expected {raw_file} not found!")
    
    # Read jsonl file
    data = []
    with open(raw_file, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    
    print(f"  Total examples: {len(data)}")
    
    if len(data) < test_size:
        raise ValueError(f"Not enough data! Need at least {test_size} examples, found {len(data)}")
    
    # Random split
    train_data, test_data = train_test_split(
        data, 
        test_size=test_size, 
        random_state=42,  # Reproducible split
        shuffle=True
    )
    
    print(f"  Train examples: {len(train_data)}")
    print(f"  Test examples: {len(test_data)}")
    
    return train_data, test_data

def validate_dataset(dataset, tokenizer, name="Dataset"):
    """Validate dataset quality before training"""
    print(f"🔍 {name} Validation:")
    print(f"  Total examples: {len(dataset)}")
    
    # Check for empty outputs
    empty_outputs = sum(1 for ex in dataset if not ex['output'].strip())
    if empty_outputs > 0:
        print(f"  ⚠️  Empty outputs: {empty_outputs}")
    
    # Check token length distribution
    lengths = []
    for ex in dataset:
        full_text = f"{ex['instruction']}: {ex['input']}\nResponse: {ex['output']}"
        length = len(tokenizer(full_text)['input_ids'])
        lengths.append(length)
    
    print(f"  Token lengths - Min: {min(lengths)}, Max: {max(lengths)}, Avg: {sum(lengths)/len(lengths):.1f}")
    
    return True

def preprocess(example, tokenizer, max_length=MAX_LENGTH):
    """Train only on the target ASP code"""
    instruction = example["instruction"]
    input_text = example["input"]
    output_text = example["output"]
    
    # Format: prompt + target
    prompt = f"{instruction}: {input_text}\nResponse:"
    full_text = prompt + f" {output_text}{tokenizer.eos_token}"
    
    # Tokenize separately for precise control
    prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
    full_ids = tokenizer(full_text, truncation=True, max_length=max_length)["input_ids"]
    
    # Pad to max_length
    input_ids = full_ids + [tokenizer.pad_token_id] * (max_length - len(full_ids))
    input_ids = torch.tensor(input_ids[:max_length])
    
    attention_mask = torch.ones_like(input_ids)
    attention_mask[len(full_ids):] = 0
    
    # Labels: only learn the output part
    labels = input_ids.clone()
    labels[:len(prompt_ids)] = -100  # Mask everything before output
    labels[attention_mask == 0] = -100  # Mask padding
    
    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels,
    }

def compute_metrics(eval_preds):
    """Better metrics than just loss"""
    predictions, labels = eval_preds
    
    # Calculate perplexity from loss
    loss = eval_preds[0].mean()
    perplexity = np.exp(loss)
    
    # Token-level accuracy (for non-masked tokens)
    pred_tokens = np.argmax(predictions, axis=-1)
    valid_mask = labels != -100
    
    if valid_mask.sum() > 0:
        valid_preds = pred_tokens[valid_mask]
        valid_labels = labels[valid_mask]
        token_accuracy = np.mean(valid_preds == valid_labels)
    else:
        token_accuracy = 0.0
    
    return {
        "perplexity": perplexity,
        "token_accuracy": token_accuracy,
    }

# =============================================================================
# MODEL SETUP FUNCTIONS (UPDATED)
# =============================================================================

def setup_model_and_tokenizer(start_checkpoint=None):
    """Load and configure model with QLoRA, optionally from checkpoint"""
    
    print("🔹 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    
    start_model_info = {}
    
    if start_checkpoint is None:
        # Start from base model
        print(f"🔹 Loading base model: {BASE_MODEL_NAME}")
        print("🔹 Applying 4-bit quantization...")
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_NAME,
            device_map="auto",
            quantization_config=bnb_config,
            trust_remote_code=True,
            local_files_only=True,
        )
        
        print("🔹 Applying QLoRA configuration...")
        lora_config = LoraConfig(
            r=LORA_R,
            lora_alpha=LORA_ALPHA,
            target_modules=[
                "q_proj", "k_proj", "v_proj", "dense",
                "fc1", "fc2"
            ],
            lora_dropout=LORA_DROPOUT,
            bias="none",
            task_type=TaskType.CAUSAL_LM,
            inference_mode=False,
        )
        model = get_peft_model(model, lora_config)
        
        start_model_info = {
            "type": "base_model",
            "path": BASE_MODEL_NAME,
            "description": "Fresh base model with new LoRA adapters"
        }
        
    else:
        # Start from checkpoint
        print(f"🔹 Loading from checkpoint: {start_checkpoint}")
        
        # Check if it's a PEFT checkpoint or full model checkpoint
        if os.path.exists(os.path.join(start_checkpoint, "adapter_config.json")):
            # It's a PEFT model - load base model first, then adapters
            print("🔹 Detected PEFT checkpoint, loading base model + adapters...")
            
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )
            
            base_model = AutoModelForCausalLM.from_pretrained(
                BASE_MODEL_NAME,
                device_map="auto",
                quantization_config=bnb_config,
                trust_remote_code=True,
                local_files_only=True,
            )
            
            # Load the PEFT adapters
            model = PeftModel.from_pretrained(
                base_model, 
                start_checkpoint,
                local_files_only=True, 
            )
            
            # Prepare for training - CRITICAL FIX
            model = model.train()
            if hasattr(model, 'enable_input_require_grads'):
                model.enable_input_require_grads()
            
            # Ensure LoRA parameters are trainable
            for name, param in model.named_parameters():
                if 'lora' in name.lower():
                    param.requires_grad = True
            
            start_model_info = {
                "type": "checkpoint",
                "path": start_checkpoint,
                "description": f"PEFT checkpoint from previous training"
            }
            
        else:
            # It's a full model checkpoint
            print("🔹 Loading full model checkpoint...")
            
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )
            
            model = AutoModelForCausalLM.from_pretrained(
                start_checkpoint,
                device_map="auto",
                quantization_config=bnb_config,
                trust_remote_code=True,
                local_files_only=True,
            )
            
            # Apply new LoRA adapters on top
            lora_config = LoraConfig(
                r=LORA_R,
                lora_alpha=LORA_ALPHA,
                target_modules=[
                    "q_proj", "k_proj", "v_proj", "dense",
                    "fc1", "fc2"
                ],
                lora_dropout=LORA_DROPOUT,
                bias="none",
                task_type=TaskType.CAUSAL_LM,
                inference_mode=False,
            )
            model = get_peft_model(model, lora_config)
            
            start_model_info = {
                "type": "checkpoint",
                "path": start_checkpoint,
                "description": f"Full model checkpoint with new LoRA adapters"
            }

    # GRADIENT FIX - Enable gradients for quantized models
    model = model.train()  # Ensure model is in training mode
    
    # For quantized models, enable input gradients
    if hasattr(model, 'enable_input_require_grads'):
        model.enable_input_require_grads()

    # Print trainable parameters
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"🔢 Trainable params: {trainable_params:,} ({trainable_params/total_params*100:.2f}%)")
    
    return model, tokenizer, start_model_info

def setup_training_arguments(models_dir, results_dir):
    """Setup training arguments with timestamped paths"""
    return TrainingArguments(
        # Paths
        output_dir=models_dir,
        logging_dir=f"{results_dir}/logs",
        overwrite_output_dir=True,
        
        # Training schedule
        num_train_epochs=NUM_EPOCHS,
        learning_rate=LEARNING_RATE,
        lr_scheduler_type=SCHEDULER_TYPE,
        warmup_steps=WARMUP_STEPS, 
        
        # Batch sizes and accumulation
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE * 2,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION,
        
        # Regularization
        weight_decay=0.01,
        max_grad_norm=1.0,
        
        # Memory and performance
        fp16=False,  # Changed from True to False
        gradient_checkpointing=False,
        dataloader_pin_memory=False,
        dataloader_num_workers=0,
        
        # Combined checkpoint and evaluation strategy
        save_strategy="steps",
        save_steps=EVAL_AND_SAVE_STEPS,
        save_total_limit=KEEP_CHECKPOINTS,
        eval_strategy="steps",
        eval_steps=EVAL_AND_SAVE_STEPS,
        
        # Logging
        logging_strategy="steps",
        logging_steps=PRINT_LOG_STEPS,
        report_to=[],
        
        # Early stopping setup
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        
        # Other settings
        remove_unused_columns=False,
        label_names=["labels"],
        prediction_loss_only=False,
    )

# =============================================================================
# UPDATED CALLBACK CLASS WITH NEW EVALUATOR
# =============================================================================

class DetailedLoggingCallback(TrainerCallback):
    def __init__(self, logger, eval_data, tokenizer, task_type='cnl-asp', construct_name='unknown'):
        self.logger = logger
        self.evaluator = create_evaluator(task_type, enable_semantic=True)  # Enable semantic evaluation
        self.eval_data = eval_data
        self.tokenizer = tokenizer
        self.task_type = task_type
        self.construct_name = construct_name
    
    def on_evaluate(self, args, state, control, model, **kwargs):
        # Only do detailed evaluation on our schedule
        if state.global_step % EVAL_AND_SAVE_STEPS == 0 and state.global_step > 0:
            print(f"🔍 Running detailed evaluation at step {state.global_step}...")
            
            # Generate predictions on test set
            predictions = []
            model.eval()
            with torch.no_grad():
                for example in self.eval_data[:min(30, len(self.eval_data))]:  # Reduced for speed
                    prompt = f"{example['instruction']}: {example['input']}\nResponse:"
                    inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=MAX_LENGTH)
                    
                    if torch.cuda.is_available():
                        inputs = {k: v.cuda() for k, v in inputs.items()}
                    
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=MAX_NEW_TOKENS,
                        do_sample=False,
                        pad_token_id=self.tokenizer.eos_token_id,
                        eos_token_id=self.tokenizer.eos_token_id,                                   
                    )
                    
                    generated = self.tokenizer.decode(outputs[0][len(inputs['input_ids'][0]):], skip_special_tokens=True)
                    predictions.append(generated.strip())
            
            # Evaluate predictions using new evaluator
            targets = [ex['output'] for ex in self.eval_data[:len(predictions)]]
            eval_results = self.evaluator.evaluate(predictions, targets)
            
            # Save detailed evaluation report using evaluator
            metadata = {
                'step': state.global_step,
                'construct_name': self.construct_name,
                'test_examples': len(predictions),
                'task_type': self.task_type,
                'epoch': state.epoch
            }
            
            step_report_path = f"{self.logger.results_dir}/step_{state.global_step}_evaluation.txt"
            self.evaluator.save_evaluation_report(eval_results, step_report_path, metadata)
            
            # Updated print statement with 4 metrics
            if self.task_type == 'cnl-asp':
                print(f"📊 Step {state.global_step} - "
                      f"Syntax: {eval_results['syntax_valid_rate']:.1%}, "
                      f"Semantic: {eval_results.get('semantic_match_rate', 0):.1%}, "
                      f"Exact: {eval_results['exact_match_rate']:.1%}, "
                      f"Non-empty: {eval_results['non_empty_rate']:.1%}")
            else:
                print(f"📊 Step {state.global_step} - "
                      f"Exact: {eval_results['exact_match_rate']:.1%}, "
                      f"Non-empty: {eval_results['non_empty_rate']:.1%}")
    
    def on_log(self, args, state, control, **kwargs):
        # Log training curves on our schedule
        if state.global_step % METRICS_LOG_STEPS == 0 and state.global_step > 0:
            logs = kwargs.get('logs', {})
            train_loss = logs.get('train_loss', 0)
            eval_loss = logs.get('eval_loss', 0)
            learning_rate = logs.get('learning_rate', 0)
            epoch = logs.get('epoch', 0)
            
            # Get additional metrics
            perplexity = logs.get('eval_perplexity', np.exp(eval_loss) if eval_loss > 0 else 0)
            token_accuracy = logs.get('eval_token_accuracy', 0) * 100
            
            self.logger.log_training_step(
                state.global_step, epoch, train_loss, eval_loss, 
                learning_rate, perplexity, token_accuracy
            )

# =============================================================================
# MAIN TRAINING FUNCTION
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Fine-tune LLM for language processing")
    parser.add_argument("--construct_path", required=True, 
                       help="Path to construct directory (e.g., phase1/facts)")
    parser.add_argument("--start_checkpoint", default=None,
                       help="Path to checkpoint/model to start from (default: use base model)")
    parser.add_argument("--task_type", choices=['cnl-asp', 'nl-cnl'], default='cnl-asp',
                       help="Task type: 'cnl-asp' for CNL→ASP, 'nl-cnl' for NL→CNL")
    parser.add_argument("--list_runs", action="store_true",
                       help="List all previous training runs and exit")
    args = parser.parse_args()
    
    # Handle list runs command
    if args.list_runs:
        runs = list_previous_runs(args.construct_path)
        if not runs:
            print(f"No previous training runs found in {args.construct_path}")
        else:
            print(f"Previous training runs for {args.construct_path}:")
            print("=" * 80)
            for i, run in enumerate(runs, 1):
                print(f"{i}. {run['timestamp_str']} ({run['timestamp'].strftime('%Y-%m-%d %H:%M:%S')})")
                print(f"   Results: {run['results_dir']}")
                print(f"   Models:  {run['models_dir']}")
                
                # Check if run completed
                metrics_file = os.path.join(run['results_dir'], 'training_metrics.txt')
                if os.path.exists(metrics_file):
                    print(f"   Status:  ✅ Completed")
                else:
                    print(f"   Status:  ❌ Incomplete")
                print()
        return
    
    print(f"🚀 Starting {args.task_type.upper()} Fine-tuning")
    print("=" * 80)
    
    # Setup paths
    construct_path = args.construct_path
    construct_name = os.path.basename(construct_path)
    data_dir = f"{construct_path}/data"
    
    # Create timestamped directories
    results_dir, models_dir, timestamp = create_timestamped_dirs(construct_path)
    
    print(f"📁 Construct: {construct_name}")
    print(f"📁 Data dir: {data_dir}")
    print(f"📁 Task type: {args.task_type}")
    print(f"📁 Run timestamp: {timestamp}")
    
    if args.start_checkpoint:
        print(f"🔄 Starting from checkpoint: {args.start_checkpoint}")
    else:
        print(f"🆕 Starting from base model: {BASE_MODEL_NAME}")
    
    # List previous runs for context
    previous_runs = list_previous_runs(construct_path)
    if previous_runs:
        print(f"📚 Previous runs: {len(previous_runs)} (use --list_runs to see details)")
    
    # Setup model and tokenizer
    model, tokenizer, start_model_info = setup_model_and_tokenizer(args.start_checkpoint)
    
    # Load and split data
    train_data, test_data = create_train_test_split(data_dir, TEST_SIZE)
    
    # Convert to HuggingFace datasets
    from datasets import Dataset
    train_dataset = Dataset.from_list(train_data)
    eval_dataset = Dataset.from_list(test_data)
    
    # Validate datasets
    validate_dataset(train_dataset, tokenizer, "Training")
    validate_dataset(eval_dataset, tokenizer, "Evaluation")
    
    # Preprocess datasets
    print("🔹 Preprocessing datasets...")
    def preprocess_wrapper(example):
        return preprocess(example, tokenizer, MAX_LENGTH)
    
    train_dataset = train_dataset.map(
        preprocess_wrapper, 
        remove_columns=train_dataset.column_names,
        desc="Processing training data"
    )
    eval_dataset = eval_dataset.map(
        preprocess_wrapper, 
        remove_columns=eval_dataset.column_names,
        desc="Processing evaluation data"
    )

    # Dataset information
    print("\n🔍 DATASET INFORMATION")
    print(f"Raw eval data length: {len(test_data)}")
    print(f"Processed eval dataset length: {len(eval_dataset)}")

    # Check first example from raw data
    raw_example = test_data[0]
    prompt = f"{raw_example['instruction']}: {raw_example['input']}\nResponse:"
    full_text = prompt + f" {raw_example['output']}"
    prompt_tokens = len(tokenizer(prompt)['input_ids'])
    full_tokens = len(tokenizer(full_text)['input_ids'])

    print(f"\nFirst example token analysis:")
    print(f"  Prompt tokens: {prompt_tokens}")
    print(f"  Total tokens needed: {full_tokens}")
    print(f"  MAX_LENGTH setting: {MAX_LENGTH}")
    print(f"  Will truncate: {'YES' if full_tokens > MAX_LENGTH else 'NO'}")

    # Check processed version
    processed = eval_dataset[0]
    labels_tensor = torch.tensor(processed['labels'])
    learning_tokens = (labels_tensor != -100).sum().item()
    print(f"  After preprocessing - learning tokens: {learning_tokens}")
    print(f"  Learning percentage: {learning_tokens/MAX_LENGTH*100:.1f}%")

    if learning_tokens == 0:
        print("  ❌ PROBLEM: No tokens to learn from!")
    else:
        # Show what we're learning
        input_ids_tensor = torch.tensor(processed['input_ids'])
        learning_ids = input_ids_tensor[labels_tensor != -100]
        sample_text = tokenizer.decode(learning_ids[:30], skip_special_tokens=True)
        print(f"  Learning sample: '{sample_text}...'")
    
    # Setup training arguments
    training_args = setup_training_arguments(models_dir, results_dir)
    
    # Setup evaluation and logging with new evaluator
    logger = EvaluationLogger(results_dir, construct_name, timestamp)
    
    # Setup trainer with conditional early stopping
    callback = DetailedLoggingCallback(logger, test_data, tokenizer, args.task_type, construct_name)
    
    # Conditional early stopping
    callbacks = [callback]
    if ENABLE_EARLY_STOPPING:
        callbacks.append(
            EarlyStoppingCallback(
                early_stopping_patience=EARLY_STOPPING_PATIENCE,
                early_stopping_threshold=EARLY_STOPPING_THRESHOLD
            )
        )
        print(f"⏰ Early stopping enabled: patience={EARLY_STOPPING_PATIENCE}, threshold={EARLY_STOPPING_THRESHOLD}")
    else:
        print("⏰ Early stopping disabled - will train for full epochs")
    
    trainer = Trainer(
        model=model,
        processing_class=tokenizer,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,
        callbacks=callbacks
    )
    
    # Start training
    print("🔷 Starting training...")
    print("=" * 80)
    
    try:
        trainer.train()
        print("✅ Training completed successfully!")
        
        # Save final model
        print("🔹 Saving final model...")
        trainer.save_model(f"{models_dir}/final_model")
        
        # Get final metrics and run final evaluation
        final_metrics = trainer.evaluate()
        
        # Run final detailed evaluation with new evaluator
        print("🔍 Running final detailed evaluation...")
        evaluator = create_evaluator(args.task_type, enable_semantic=True)  # Enable semantic evaluation
        
        # Generate final predictions
        predictions = []
        model.eval()
        with torch.no_grad():
            for example in test_data:
                prompt = f"{example['instruction']}: {example['input']}\nResponse:"
                inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=MAX_LENGTH)
                
                if torch.cuda.is_available():
                    inputs = {k: v.cuda() for k, v in inputs.items()}
                
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=MAX_NEW_TOKENS,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                )
                
                generated = tokenizer.decode(outputs[0][len(inputs['input_ids'][0]):], skip_special_tokens=True)
                predictions.append(generated.strip())
        
        targets = [ex['output'] for ex in test_data]
        final_eval_results = evaluator.evaluate(predictions, targets)
        
        # Save final evaluation report using evaluator
        final_metadata = {
            'construct_name': construct_name,
            'checkpoint_path': f"{models_dir}/final_model",
            'data_path': data_dir,
            'test_examples': len(test_data),
            'training_timestamp': timestamp,
            'task_type': args.task_type,
            'final_evaluation': True
        }
        
        final_report_path = f"{results_dir}/final_evaluation_report.txt"
        evaluator.save_evaluation_report(final_eval_results, final_report_path, final_metadata)
        
        # Update final metrics with evaluation results
        final_metrics.update({
            'total_tokens': len(train_dataset) * MAX_LENGTH * NUM_EPOCHS,
            'exact_match_rate': final_eval_results['exact_match_rate'],
            'syntax_valid_rate': final_eval_results.get('syntax_valid_rate', 0),
            'semantic_match_rate': final_eval_results.get('semantic_match_rate', 0),
        })
        
        # Finalize logging
        logger.finalize_training_summary(final_metrics, len(train_dataset), len(eval_dataset), start_model_info, args.task_type)
        
        print(f"💾 Final model saved to: {models_dir}/final_model")
        print(f"📊 Training metrics saved to: {results_dir}")
        print(f"🏷️  Run timestamp: {timestamp}")
        print(f"🎯 Final exact match rate: {final_eval_results['exact_match_rate']:.1%}")
        if args.task_type == 'cnl-asp':
            print(f"🔧 Final syntax valid rate: {final_eval_results['syntax_valid_rate']:.1%}")
            print(f"🎯 Final semantic match rate: {final_eval_results.get('semantic_match_rate', 0):.1%}")
        print("🎉 Training complete!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Training interrupted by user")
        print("💾 Saving current checkpoint...")
        trainer.save_model(f"{models_dir}/interrupted_model")
        
    except Exception as e:
        print(f"\n❌ Training failed with error: {e}")
        raise

if __name__ == "__main__":
    main()
