# distill_model.py
import torch
from torch.nn import KLDivLoss
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
from datasets import load_dataset

# -----------------------
# Device (MPS for Apple Silicon)
# -----------------------
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
print("Using device:", device)

# -----------------------
# Paths
# -----------------------
TEACHER_MODEL_PATH = "aarushibakshi/repo"       # large 6.5GB model
STUDENT_SAVE_PATH = "distilbert-sentiment"     # folder to save distilled model
DATA_FILE = "./twitter_data_small.csv"         # local CSV/JSON/Parquet

# -----------------------
# Load Teacher Model
# -----------------------
teacher_model = AutoModelForSequenceClassification.from_pretrained(
    TEACHER_MODEL_PATH,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
)
teacher_model.eval()
teacher_model.to(device)   # move to MPS

# -----------------------
# Load Student Model
# -----------------------
student_model_name = "distilbert-base-uncased"
student_tokenizer = DistilBertTokenizer.from_pretrained(student_model_name)
student_model = DistilBertForSequenceClassification.from_pretrained(
    student_model_name,
    num_labels=2
)
student_model.train()
student_model.to(device)   # move to MPS

# -----------------------
# Load Local Dataset
# -----------------------
dataset = load_dataset("csv", data_files=DATA_FILE)
train_data = dataset["train"]

# -----------------------
# Training Parameters
# -----------------------
batch_size = 16
epochs = 3
temperature = 2.0
optimizer = torch.optim.Adam(student_model.parameters(), lr=5e-5)
criterion = KLDivLoss(reduction="batchmean")

# -----------------------
# Distillation Loop
# -----------------------
for epoch in range(epochs):
    print(f"Epoch {epoch+1}/{epochs}")
    for i in range(0, len(train_data), batch_size):
        # Select batch
        batch_rows = train_data.select(range(i, min(i + batch_size, len(train_data))))
        batch_texts = [x["text"] for x in batch_rows]

        # Tokenize batch and move tensors to device
        inputs = student_tokenizer(batch_texts, truncation=True, padding=True,
                                   return_tensors="pt", max_length=128)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Teacher predictions
        with torch.no_grad():
            teacher_logits = teacher_model(**inputs).logits

        # Student predictions
        student_logits = student_model(**inputs).logits

        # Distillation loss
        loss = criterion(
            torch.nn.functional.log_softmax(student_logits / temperature, dim=-1),
            torch.nn.functional.softmax(teacher_logits / temperature, dim=-1)
        ) * (temperature ** 2)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Logging every 50 batches
        if (i // batch_size) % 50 == 0:
            print(f"Batch {i // batch_size}/{len(train_data)//batch_size}, Loss: {loss.item():.4f}")

    print(f"Epoch {epoch+1} completed")

# -----------------------
# Save Distilled Model
# -----------------------
student_model.save_pretrained(STUDENT_SAVE_PATH)
student_tokenizer.save_pretrained(STUDENT_SAVE_PATH)
print("Distilled model saved at:", STUDENT_SAVE_PATH)
