# Wine Recommendation System

## Goal
This project aims to provide users with tailored wine recommendations based on their taste preferences. Using various embedding models, we generate latent spaces through embedding cosine similarity to deliver precise and delectable wine recommendations.

## Project Structure

### `data`
Contains the dataset primarily used for generating embeddings of wine names and their descriptions, which are crucial for the recommendation system.

### `demo`
Includes scripts to build and run the user interface of the application. The application is developed using Expo and Next.js, enabling both web and mobile interfaces.

### `notebook`
This directory houses Jupyter notebooks for:
- Exploratory Data Analysis (EDA) to understand dataset characteristics.
- Generating embeddings using various machine learning models.
- Implementing and testing a non-deep learning model (KNN) for recommendations.
- Evaluating the overall performance of the recommendation system.

### `scripts`
Scripts in this folder include:
- `KNN.py`: Implements the K-Nearest Neighbors (KNN) model.
- `open_ai_embeddings.py`: Script to generate embeddings using different models, based on OpenAI's techniques.
- `eval_embedding_model.py`: Evaluates the performance of the embedding-based recommendation system.

### `/setup.py`
A setup script to prepare the environment for generating embeddings, running the KNN model, and evaluating the system.

### `requirements.txt`
Lists all the necessary Python packages and libraries required to run the project. Ensure all dependencies are installed by running:


# BottleBuddy
https://www.kaggle.com/datasets/zynicide/wine-reviews
