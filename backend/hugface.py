from huggingface_hub import upload_folder


# 2️⃣ Repo ID on Hugging Face (username/repo)
REPO_ID = "gargavi/repo"

# 3️⃣ Path to your local model folder
MODEL_DIR = "twitter_sentiment_model"


# 5️⃣ Upload the folder to your Hugging Face repo
upload_folder(
    folder_path=MODEL_DIR,
    repo_id=REPO_ID,
    repo_type="model",
    ignore_patterns=["*.pyc", "__pycache__"]  # Optional: ignore temp files
)

print("Model uploaded successfully!")
