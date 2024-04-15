from pymongo import MongoClient
import certifi
import pymongo.errors as mongo_errors
import pandas as pd
import openai
from sentence_transformers import SentenceTransformer

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

def generate_gist_embedding(user_data, model_name='avsolatorio/GIST-Embedding-v0'):
    """
    Purpose: Generate an embedding for the given user_data using the specified model.
    Input: user_data - The user_data for which an embedding is to be generated.
    Input: model_name - The model to use for generating the embedding.
    """
    # Initialize the SentenceTransformer
    model = SentenceTransformer(model_name)

    # Embed the query
    embedding = model.encode([user_data], convert_to_tensor=True)

    # Convert embedded query tensor to list before querying the index
    embedding = embedding[0].squeeze().tolist()

    return embedding

def generate_openai_embedding(text, model="text-embedding-ada-002"):
    """
    Purpose: Generate an embedding for the given text using the specified model.
    Input: text - The text for which an embedding is to be generated.
    Input: model - The model to use for generating the embedding.
    """
    #client = openai.Client(OPENAI_API_KEY)
    openai.api_key = 'your-openai-api-key'
    response = openai.Embedding.create(input=text, model=model)
    embedding = response['data'][0]['embedding']
    return embedding

def fetch_data(embedding, name, k=5):
    """
    Fetch similar embeddings from MongoDB database using a vector search.
    """
    query = [
        {
            "$vectorSearch": {
                "index": f"{name}_index",
                "path": f"{name}_embeddings",
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

def run_evaluation(tasters, data, points):
    """
    Run evaluation on model: for evaluation, we consider each taster's top 5 wines based on the points given.
    For each of the top 5, we look at the 10 most similar vectors as recommendations, and see what percentage of the
    recommended wines were within <5 points of the original top10 wine of each taster-- thus demonstrating similar interest

    parameters:
        tasters: list of unique taster_name in the original dataset
        data: data that includes the points given to each wine by each taster
        points: threshold to be within
    returns: percentage value of how often the recommended wines were within <5 points of original top-10 wine for each user
    """
    final_percentages_recommended_less5difference = []
    wine_names = data['title']
    for name in tasters:
        tasters_differences = []
        voted_wines =  data[data['taster_name']==name]
        voted_wines.sort_values(by='points', ascending=False, inplace = True)

        voters_top_10 = voted_wines.head(10)
        point_values = voters_top_10['points'].tolist()
        indexes = voters_top_10.index.tolist()
        for i in range(len(indexes)):
            recommended_point_differences = []
            index_value = indexes[i]
            reference_index = index_value # Adjust as needed
            reference_wine = data.loc[reference_index]['description']
            # reference_wine = scaled_data[reference_index].reshape(1, -1)  # Reshape to match the input format expected by kneighbors
            # _, indices = model.kneighbors(reference_wine)
            reference_desc = generate_gist_embedding(reference_wine)
            gist_results = fetch_data(reference_desc, 'gist', 10)
            results_list = []
            for result in gist_results:
                results_list.append(result['title'])

            nearest_neighbor_names = results_list

            #get the points
            for nearest_neighbor_name in nearest_neighbor_names:
                if nearest_neighbor_name in voted_wines['title'].values:
                    # Get the row where the name is present in the 'title' column
                    row = voted_wines[voted_wines['title'] == nearest_neighbor_name]
                    # Get the points column value from the row
                    difference = abs(point_values[i]-row['points'].values[0])
                    recommended_point_differences.append(difference)
            meets_threshold_count = 0
            for x in recommended_point_differences:
                if x<=points:
                    meets_threshold_count+=1
            if len(recommended_point_differences)!=0:
                tasters_differences.append(meets_threshold_count/len(recommended_point_differences))
        if len(tasters_differences)!=0:
            final_percentages_recommended_less5difference.append(sum(tasters_differences)/len(tasters_differences))
    return final_percentages_recommended_less5difference

# The main function that will be executed when the script is run.
if __name__ == "__main__":
    db = get_database()
    if db is not None:
        # Define the collection
        collection = db['Wine']

        # Set up data for evaluation
        df = pd.read_csv('/content/data_first10k.csv')
        data = pd.get_dummies(df, columns=['country', 'designation', 'province', 'variety', 'winery' ])
        tasters = data['taster_name'].unique().tolist()

        # Run evaluation
        point_threshold = 5
        percentages = run_evaluation(tasters, data, point_threshold)
        
        # Calculate the average percentage
        print('With a point threshold of 5, the average percentage of recommended wines within the threshold is:' , sum(percentages)/len(percentages))