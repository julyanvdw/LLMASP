import os

# Set cache directory BEFORE importing transformers
os.environ["HF_HOME"] = "./cache"

from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/phi-2"

print(f"📦 Downloading model: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

print("✅ Download complete.")
