# Semantic-Movie-Recommendation-System-using-LLM-Embeddings
# 🎬 LLM-Based Movie Recommendation System

This project is a semantic movie recommendation system powered by a Large Language Model (LLM) using the `sentence-transformers` library. It understands user preferences from natural language inputs and provides personalized movie suggestions by comparing semantic similarity between user queries and movie descriptions.

## 🚀 Features

- Utilizes the `all-MiniLM-L6-v2` model from Hugging Face for fast and efficient semantic embeddings.
- Accepts natural language input to recommend movies based on context and meaning.
- Uses cosine similarity to rank movie descriptions by relevance to user queries.
- Optimized for Google Colab with custom Hugging Face cache directory for quicker model loading.

## 🧠 How It Works

1. **User Input**: A natural language query like “Recommend me a sci-fi movie with time travel.”
2. **Embedding Generation**: The system generates vector embeddings for both the input and movie dataset.
3. **Similarity Matching**: It calculates cosine similarity between the query and each movie description.
4. **Output**: Returns the top N most semantically similar movies.

## 🛠️ Installation

Install required libraries:

```bash
pip install sentence-transformers

**Datasets**
Link:- https://drive.google.com/drive/u/0/folders/1s9gA9hxG8p3IvxMBpJl9U_ZEteIp2OOS

📁 Project Structure

├── movie recommendation.ipynb       # Core logic for movie recommendation
├── README.md                        # Project documentation

📦 Model Used
all-MiniLM-L6-v2:
A compact yet powerful transformer model optimized for generating sentence-level embeddings with high performance.

💻 Environment
Python 3.7+

sentence-transformers

Google Colab (recommended for ease of use and GPU access)

Hugging Face cache configured at /content/huggingface_cache for faster downloads

🙌 Acknowledgments
Hugging Face
Sentence Transformers
The open-source community for inspiring this project


Let me know if you’d like to add a section on datasets, model fine-tuning, or how to deploy this as a web app.
