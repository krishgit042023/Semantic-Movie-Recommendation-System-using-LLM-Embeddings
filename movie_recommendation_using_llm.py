# -*- coding: utf-8 -*-
"""Movie Recommendation using LLM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZJNVgmB-U0wDJ5kD1gQibXF-MEqOoxNP
"""

!pip install sentence-transformers

import kagglehub

# Download latest version
path = kagglehub.dataset_download("tmdb/tmdb-movie-metadata")

print("Path to dataset files:", path)

# prompt: load dataset

import pandas as pd
df_credits = pd.read_csv("/content/tmdb_5000_credits.csv")
df_credits.head()

df_credits.shape

df_movies = pd.read_csv("/content/tmdb_5000_movies.csv")
df_movies.head()

df_movies.shape

# prompt: show the list of columns in df_movies

df_movies.columns

# prompt: remove 'original title' and 'title' column from df_movies

df_movies = df_movies.drop(columns=['original_title', 'title'], errors='ignore')

df_movies.shape

# prompt: join df_credits and df_movies  and name the new dataframe as dataset

import pandas as pd
# Assuming 'id' in df_movies and 'movie_id' in df_credits, correct the merge operation
dataset = pd.merge(df_credits, df_movies, left_on='movie_id', right_on='id', how='inner')

# After the merge, you can drop the redundant 'movie_id' column if you wish
dataset = dataset.drop(columns=['movie_id'])

dataset.head()

dataset.shape

dataset.columns

# prompt: check for null values in dataset dataframe

dataset.isnull().sum()

# prompt: create a new dataframe consisting of columns 'overview' ,'title', 'genres', 'keywords', 'cast', 'crew' and name the dataframe as movie

movie = dataset[['overview', 'title', 'genres', 'keywords', 'cast', 'crew']]

movie.head()

movie.shape

# prompt: check for null values

movie.isnull().sum()

# prompt: show the row in which the overview column contain null values

import pandas as pd
movie = dataset[['overview', 'title', 'genres', 'keywords', 'cast', 'crew']]
# Find rows where 'overview' is null
null_overview_rows = movie[movie['overview'].isnull()]
null_overview_rows

# prompt: drop the 3 rows in which the overview column contains nan values

movie = movie.dropna(subset=['overview'])
movie.isnull().sum()

movie.shape

movie.columns

"""**Compute Embeddings**"""

import pandas as pd

# Function to combine the relevant fields into one text string per movie
def combine_movie_info(row):
    # Ensure each column is converted to string if it's not already
    return f"{row['overview']} {row['title']} {row['genres']} {row['keywords']} {row['cast']} {row['crew']}"

# Create a new column 'combined_text'
movie['combined_text'] = movie.apply(combine_movie_info, axis=1)

# Optionally, inspect the combined text for the first few movies
print(movie['combined_text'].head())

from sentence_transformers import SentenceTransformer
import os

# Specify Hugging Face cache directory using environment variable
os.environ['TRANSFORMERS_CACHE'] = '/content/huggingface_cache'  # Using a custom path within Colab

# Load the pre-trained model, forcing a re-download if needed
model = SentenceTransformer('all-MiniLM-L6-v2') # Remove cache_dir and download_progress_bar

from sentence_transformers import SentenceTransformer

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert the combined text into a list
movie_texts = movie['combined_text'].tolist()

# Compute embeddings for each movie's combined text
movie_embeddings = model.encode(movie_texts)

# Verify the result: print the shape of the embedding vector for the first movie
print("Shape of embedding for the first movie:", movie_embeddings[0].shape)

"""**Build Query-Based Recommendations**"""

user_query = input("Enter your movie preference query (e.g., 'I love mind-bending sci-fi'): ")


#Using the same model to convert the user query into an embedding

query_embedding = model.encode(user_query, convert_to_tensor=True)



from sentence_transformers import util

# Compute cosine similarity between the query embedding and all movie embeddings
cosine_scores = util.cos_sim(query_embedding, movie_embeddings)

# Convert the scores to a numpy array for easier handling
cosine_scores = cosine_scores[0].cpu().numpy()



#display the top 5 recommendations

import numpy as np

# Get the indices of the top 5 movies with the highest cosine similarity scores
top_indices = np.argsort(-cosine_scores)[:5]

print("\nTop 5 Recommended Movies:")
for idx in top_indices:
    title = movie.iloc[idx]['title']  # Assuming your DataFrame 'df' has the movie titles
    score = cosine_scores[idx]
    print(f"{title} (Similarity Score: {score:.4f})")

"""**Build a Similar-Movie Recommendation Feature**"""

from sentence_transformers import util
import numpy as np

# Step 1: Accept user input for a movie title
query_title = input("Enter a movie title (e.g., 'Batman'): ").strip().lower()

# Step 2: Find matching movie in the 'movie' DataFrame
# Using a simple case-insensitive substring search in the 'title' column
matched_movies = movie[movie['title'].str.lower().str.contains(query_title)]

if matched_movies.empty:
    print("No movie found with that title.")
else:
    # For simplicity, take the first matched movie
    selected_movie = matched_movies.iloc[0]
    print(f"Found movie: {selected_movie['title']}")

    # Step 3: Retrieve the index and embedding of the selected movie
    movie_index = selected_movie.name  # Ensure the DataFrame index aligns with the embeddings order
    query_movie_embedding = movie_embeddings[movie_index]

    # Step 4: Compute cosine similarity between the selected movie and all movies
    # The function returns a tensor; we convert it to a numpy array for easier manipulation
    cosine_scores = util.cos_sim(query_movie_embedding, movie_embeddings)[0].cpu().numpy()

    # Step 5: Exclude the selected movie by setting its similarity to -infinity
    cosine_scores[movie_index] = -np.inf

    # Get the indices of the top 5 movies with the highest similarity scores
    top_indices = np.argsort(-cosine_scores)[:5]

    # Step 6: Display the top 5 recommended movies
    print("\nTop 5 movies similar to", selected_movie['title'])
    for idx in top_indices:
        similar_title = movie.iloc[idx]['title']
        score = cosine_scores[idx]
        print(f"{similar_title} (Similarity Score: {score:.4f})")

"""**Deploying the model**"""

!pip install gradio

# prompt: create a user interface using gradio where the user can give input based on genres or movie name names ,, and in output the top 5 recommendations will be given

import numpy as np
import gradio as gr

def recommend_movies(query_type, input_text):
    if query_type == "Movie Name":
        query_title = input_text.strip().lower()
        matched_movies = movie[movie['title'].str.lower().str.contains(query_title)]
        if matched_movies.empty:
            return "No movie found with that title."
        else:
            selected_movie = matched_movies.iloc[0]
            movie_index = selected_movie.name
            query_movie_embedding = movie_embeddings[movie_index]
            cosine_scores = util.cos_sim(query_movie_embedding, movie_embeddings)[0].cpu().numpy()
            cosine_scores[movie_index] = -np.inf
            top_indices = np.argsort(-cosine_scores)[:5]
            recommendations = "\n".join([f"{movie.iloc[idx]['title']} (Similarity Score: {cosine_scores[idx]:.4f})" for idx in top_indices])
            return recommendations
    elif query_type == "Genre/Description":
        user_query = input_text
        query_embedding = model.encode(user_query, convert_to_tensor=True)
        cosine_scores = util.cos_sim(query_embedding, movie_embeddings)
        cosine_scores = cosine_scores[0].cpu().numpy()
        top_indices = np.argsort(-cosine_scores)[:5]
        recommendations = "\n".join([f"{movie.iloc[idx]['title']} (Similarity Score: {cosine_scores[idx]:.4f})" for idx in top_indices])
        return recommendations
    else:
        return "Invalid query type."

iface = gr.Interface(
    fn=recommend_movies,
    inputs=[
        gr.Radio(["Movie Name", "Genre/Description"], label="Query Type"),
        gr.Textbox(label="Enter Movie Name or Genre/Description")
    ],
    outputs=gr.Textbox(label="Top 5 Recommendations"),
    title="Movie Recommendation Engine",
    description="Get movie recommendations based on movie name or genre/description."
)

iface.launch()

