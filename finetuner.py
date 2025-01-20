from unsloth import FastLanguageModel
import torch
import pandas as pd

max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.2-3B-Instruct", # or specify local model file path after the first time you have downloaded the model from HF
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
    # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
    # local_files_only=True
)

model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # Supports any, but = 0 is optimized
    bias = "none",    # Supports any, but = "none" is optimized
    # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    use_rslora = False,  # We support rank stabilized LoRA
    loftq_config = None, # And LoftQ
)

from datasets import load_dataset
# Load the training dataset
dataset = load_dataset("csv", data_files="data_stories.csv", split="train")


# Define a function to apply the chat template
def apply_chat_template(example):
    messages = [
        {"role": "user", "content": example['Prompt']},
        {"role": "assistant", "content": example['Story']}
    ]
    row = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    return {"text": row}

# Apply the chat template function to the dataset
new_dataset = dataset.map(apply_chat_template)
#new_dataset = new_dataset.train_test_split(0.20) # Let's keep 20% of the data
from pprint import pprint
#pprint(new_dataset[0])


"""ds = pd.read_csv("data_stories.csv")
print (ds.head())

dataset_data = [
    {
        "instruction": "You are a writer.",
        "input": row_dict["Prompt"],
        "output": row_dict["Story"]
    }
    for row_dict in ds.to_dict(orient="records")
]
 
print (dataset_data[0])"""

from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = new_dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False, # Can make training 5x faster for short sequences.
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 2,
        # num_train_epochs = 1, # For longer training runs!
        learning_rate = 2e-4,
        fp16 = not is_bfloat16_supported(),
        bf16 = is_bfloat16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none", # Use this for WandB etc
    ),
)
pprint ("start training")
trainer_stats = trainer.train()

pprint ("save lora model")

model.save_pretrained("lora_model")  # Local saving
tokenizer.save_pretrained("lora_model")

#pprint ("save model gguf")
#model.save_pretrained_gguf("model", tokenizer, quantization_method="q4_k_m", maximum_memory_usage = 0.7)