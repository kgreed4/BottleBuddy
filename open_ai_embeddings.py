
from pymongo import MongoClient
import certifi
import pymongo.errors as mongo_errors
import pandas as pd
import openai

# Here we create the openai object and set the API key so that we can use the OpenAI API.
openai.api_key = 'your_openai_api_key'

def get_database():
    """
    Purpose: Establish a connection to the MongoDB database.
    """
    uri = "mongodb+srv://sriveerisetti:Wine@wine.kdvgm.mongodb.net/?retryWrites=true&w=majority&appName=Wine"
    ca = certifi.where()

    try:
        client = MongoClient(uri, tlsCAFile=ca)
        client.list_database_names()
        # The name of the database is 'BottleBuddy'.
        db = client['BottleBuddy']
        print("Successfully connected to the database.")
        return db
    except mongo_errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_embedding(text, model="text-embedding-ada-002"):
    """
    Purpose: Generate an embedding for the given text using the specified model.
    Input: text - The text for which an embedding is to be generated.
    Input: model - The model to use for generating the embedding.
    """
    response = openai.Embedding.create(input=[text], model=model)
    embedding = response['data'][0]['embedding']
    return embedding

def store_row_with_embedding(custom_id, title, description, collection):
    """
    Purpose: Store the title, description, and its embedding in the database with a custom ID.
    Input: custom_id - The custom ID to use for the document.
    Input: title - The title of the content.
    Input: description - The description of the content.
    Input: collection - The MongoDB collection in which to store the document.
    """
    combined_text = title + " " + description
    # Here we use the generate_embedding function to generate the embedding for the combined text.
    embedding = generate_embedding(combined_text)
    collection.insert_one({
        "_id": custom_id,
        "title": title,
        "description": description,
        "openai_embedding": embedding
    })
    # I want to make sure that the content has been stored successfully in the database so we print a message after every row 
    # is added to the MongoDB collection.
    print(f"Content with title '{title}' has been successfully stored in MongoDB with ID {custom_id}.")

def process_csv_file(csv_path, collection):
    """
    Purpose: Process the CSV file and store the content along with its embedding in the database.
    Input: csv_path - The path to the CSV file containing the content.
    Input: collection - The MongoDB collection in which to store the documents.
    """
    data = pd.read_csv(csv_path)
    next_id = 0
    # Here we iterate over each row and store the content along with its embedding in the database.
    for index, row in data.iterrows():
        # We use the store_row_with_embedding function that we just created to store the content in the database.
        store_row_with_embedding(next_id, row['title'], row['description'], collection)
        next_id += 1

# The main function that will be executed when the script is run.
if __name__ == "__main__":
    db = get_database()
    if db is not None:
        # Define the collection
        collection = db['Wine']
        # Define the path to the csv file where you want to extract the data from
        csv_path = "path_to_your_csv_file.csv"
        # Run the process_csv_file function to process the CSV file and store the content in the database.
        process_csv_file(csv_path, collection)
