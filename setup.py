#!/usr/bin/python3

from scripts.KNN.py import main as KNN
from scripts.open_ai_embeddings.py import main as Embedding
from scripts.eval_embedding_model.py import main as Eval

def main():
    
    # Run Classical Model
    KNN()

    # Run Embedding Model
    Embedding()

    # Run evaluation
    Eval()

if __name__ == "__main__":
    main()