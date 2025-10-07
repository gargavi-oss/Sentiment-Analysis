import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

# ===============================
# STEP 1: Load your preprocessed CSV
# ===============================
df = pd.read_csv("twitter_data_small.csv")

# 80% train, 20% test split
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Convert to Hugging Face Dataset
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# ===============================
# STEP 2: Load tokenizer & encode
# ===============================
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def preprocess(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True)

train_dataset = train_dataset.map(preprocess, batched=True)
test_dataset = test_dataset.map(preprocess, batched=True)

# Set format for PyTorch
train_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])
test_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

# ===============================
# STEP 3: Load model
# ===============================
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# ===============================
# STEP 4: Define training args
# ===============================
training_args = TrainingArguments(
    output_dir="./twitter_sentiment_model",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=2,
    learning_rate=2e-5,
    weight_decay=0.01,
    logging_dir="./logs",
    do_eval=True,        # enable evaluation
    logging_steps=500,   # log every 500 steps
    eval_steps=1000      # evaluate every 1000 steps
)


# ===============================
# STEP 5: Trainer
# ===============================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
)

# ===============================
# STEP 6: Train & save
# ===============================
trainer.train()
trainer.save_model("./twitter_sentiment_model")
tokenizer.save_pretrained("./twitter_sentiment_model")

print("✅ Model trained and saved to './twitter_sentiment_model'")
