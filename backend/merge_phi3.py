"""
Merge MJ_QLORA_ADAPTER into the Phi-3 Mini base model
and save the fused checkpoint to:

backend/model/phi3_merged_mj/
"""

from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

# ── Paths ─────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent          # …/backend
MODEL_DIR = ROOT / "model"

BASE_MODEL_ID = "microsoft/phi-3-mini-128k-instruct"
ADAPTER_DIR   = MODEL_DIR / "MJ_QLORA_ADAPTER"  # your LoRA weights
OUT_DIR       = MODEL_DIR / "phi3_merged_mj"    # will be created

# ── Load base model + tokenizer ───────────────────────────────────────
print("🔄  Loading Phi-3 Mini base model …")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID, trust_remote_code=True)

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_ID,
    torch_dtype=torch.float16,       # use float32 if you’re strictly on CPU
    device_map="auto",
    trust_remote_code=True
)
print("✅ Base model loaded.")

# ── Load adapter & merge ──────────────────────────────────────────────
print(f"🔄  Loading adapter from {ADAPTER_DIR} …")
merged_model = PeftModel.from_pretrained(base_model, ADAPTER_DIR.as_posix())
print("✅ Adapter loaded.  Merging …")

merged_model = merged_model.merge_and_unload()   # fuse LoRA weights
print("✅ Merge complete.")

# ── Save merged checkpoint ────────────────────────────────────────────
print(f"💾  Saving merged model to {OUT_DIR} …")
OUT_DIR.mkdir(parents=True, exist_ok=True)
merged_model.save_pretrained(OUT_DIR)
tokenizer.save_pretrained(OUT_DIR)
print("🎉  All done!  Merged model lives at:", OUT_DIR)
