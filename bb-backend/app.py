import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
load_dotenv()

# MongoDB Configuration from environment variables
MONGODB_URI = os.getenv('MONGODB_URI')

# Connect to MongoDB
try:
    client = MongoClient(MONGODB_URI)
    db_name = 'BottleBuddy'
    collection_name = 'Wine'
    db = client[db_name]
    collection = db[collection_name]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

# Initialize the SentenceTransformer model
try:
    gist_model = SentenceTransformer('avsolatorio/GIST-Embedding-v0')
except Exception as e:
    print(f"Error loading Sentence Transformer model: {e}")
    exit(1)

def embed_data(text):
    """Generate Gist embeddings for the given text."""
    return gist_model.encode(text).tolist()

def fetch_data(embedding, k=5):
    """
    Fetch similar embeddings from MongoDB database using a vector search.
    """
    query = [
        {
            "$vectorSearch": {
                "index": "gist_index",
                "path": "gist_embeddings",
                "queryVector": embedding,
                "numCandidates": 50,
                "limit": k
            }
        }
    ]
    try:
        results = list(collection.aggregate(query))
    except Exception as e:
        print(f"Error performing vector search in MongoDB: {e}")
        results = []  # Return an empty list in case of error

    return results

@app.route('/find', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def find_data():
    data = request.json
    if not data or 'criteria' not in data:
        return jsonify({"error": "No data provided"}), 400
    
    criteria = " "
    for word in data['criteria']:
        criteria += word + ", "

    # Embed the input data
    embedding = embed_data(criteria)

    # Fetch data from MongoDB using the embedding
    results = fetch_data(embedding, k=5)

    results_list = []
    for result in results:
        results_list.append(result['title'])

    print(results_list)

    # Return the results to the frontend
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)