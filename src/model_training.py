from datasets import load_dataset, concatenate_datasets
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from transformers import Trainer, DataCollatorForLanguageModeling
import torch
import os
from huggingface_hub import login
from config.config import HUGGING_FACE_TOKEN

def load_and_merge_tweet_eval():
    """Load and merge all TweetEval subsets"""
    try:
        print("Loading TweetEval subsets...")
        subsets = [
            "emotion", "hate", "irony", "offensive", 
            "sentiment", "stance_abortion", "stance_atheism",
            "stance_climate", "stance_feminist", "stance_hillary"
        ]
        
        all_datasets = []
        for subset in subsets:
            print(f"Loading subset: {subset}")
            dataset = load_dataset("tweet_eval", subset)
            
            # Format tweets based on subset type
            def format_text(examples):
                texts = examples["text"]
                labels = examples["label"]
                
                # Format based on subset type
                if subset == "emotion":
                    label_map = {0: "anger", 1: "joy", 2: "optimism", 3: "sadness"}
                elif subset == "sentiment":
                    label_map = {0: "negative", 1: "neutral", 2: "positive"}
                elif subset in ["irony", "hate", "offensive"]:
                    label_map = {0: "no", 1: "yes"}
                else:  # stance datasets
                    label_map = {0: "none", 1: "against", 2: "favor"}
                
                formatted = [
                    f"Tweet: {text}\nCategory: {subset}\nLabel: {label_map[label]}"
                    for text, label in zip(texts, labels)
                ]
                return {"text": formatted}
            
            # Process dataset
            processed = dataset.map(
                format_text,
                batched=True,
                remove_columns=dataset["train"].column_names
            )
            all_datasets.append(processed["train"])
        
        # Concatenate all training sets
        print("Merging datasets...")
        merged_dataset = concatenate_datasets(all_datasets)
        print(f"Total examples in merged dataset: {len(merged_dataset)}")
        
        return merged_dataset
        
    except Exception as e:
        print(f"Error loading datasets: {e}")
        raise

def tokenize_function(examples, tokenizer):
    """Tokenize and format data for causal language modeling"""
    # Add labels for causal language modeling (next token prediction)
    result = tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=128
    )
    
    # Create labels (same as input_ids for causal LM)
    result["labels"] = result["input_ids"].copy()
    
    return result

def train_model():
    try:
        # Login with token
        login(token=HUGGING_FACE_TOKEN)
        
        # Load and merge datasets
        dataset = load_and_merge_tweet_eval()
        
        print("Initializing model and tokenizer...")
        model_name = "distilgpt2"
        
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            padding_side="right",
            truncation_side="right"
        )
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            
        print("Loading model...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32
        )
        
        model.resize_token_embeddings(len(tokenizer))
        
        # Tokenize the dataset with labels
        print("Tokenizing dataset...")
        tokenized_dataset = dataset.map(
            lambda x: tokenize_function(x, tokenizer),
            batched=True,
            remove_columns=dataset.column_names
        )
        
        print("Configuring LoRA...")
        lora_config = LoraConfig(
            r=8,
            lora_alpha=32,
            target_modules=["c_attn"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
            fan_in_fan_out=True
        )
        
        print("Preparing model for training...")
        model = get_peft_model(model, lora_config)
        
        print("Setting up training arguments...")
        training_args = TrainingArguments(
            output_dir="./lora_gpt2_twitter",
            run_name="gpt2_twitter_training",
            num_train_epochs=1,
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            save_steps=500,
            logging_steps=50,
            learning_rate=2e-4,
            optim="adamw_torch",
            logging_dir="./logs",
            save_total_limit=2,
            load_best_model_at_end=True,
            eval_strategy="steps",
            eval_steps=500,
            remove_unused_columns=False,
            report_to=[],
            # Add these parameters for better training
            prediction_loss_only=True,
            label_names=["labels"]
        )
        
        # Split dataset into train and validation
        tokenized_dataset = tokenized_dataset.train_test_split(test_size=0.1)
        
        print("Initializing trainer...")
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset["train"],
            eval_dataset=tokenized_dataset["test"],
            # Remove tokenizer parameter to avoid deprecation warning
        )
        
        print("Starting training...")
        trainer.train()
        
        print("Saving model...")
        model.save_pretrained("./lora_gpt2_twitter")
        print("Training complete!")
        
    except Exception as e:
        print(f"Error in training process: {e}")
        raise

if __name__ == "__main__":
    print("Starting model training process...")
    train_model() 