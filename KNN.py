import pandas as pd
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


def clean_data(df):
    """
    Clean the dataset by handling NA and non-helpful column values in certain columns
    parameters: 
        df (DataFrame): original dataframe
    returns:
        df_cleaned (DataFrame): cleaned dataframe
    """
    df.drop(columns = ['description', 'region_1', 'region_2', 'taster_twitter_handle'], inplace = True)

    #drop rows that do not have any info on province, variety, and/or country
    df_drop_na = df.dropna(subset = ['variety', 'province', 'country'])

    #replace NA of designation with 'no designation'
    df_drop_na['designation']= df_drop_na['designation'].fillna('no designation')

    #replace NA values for price with the average price of other wines that have same winery, variety values
    df_drop_na['price'] = df_drop_na.groupby(['winery', 'variety'])['price'].transform(lambda x: x.fillna(x.mean()))
    df_drop_na['price'] = df_drop_na.groupby(['variety'])['price'].transform(lambda x: x.fillna(x.mean()))
    df_drop_na = df_drop_na.dropna(subset = ['price'])

    #drop the rows where the winery name, designation, variety, province is a singular instance
    value_counts = df_drop_na['winery'].value_counts()
    values_to_drop = value_counts[value_counts==1].index
    df_drop_na = df_drop_na[~df_drop_na['winery'].isin(values_to_drop)]
    value_counts= df_drop_na['designation'].value_counts()
    values_to_drop = value_counts[value_counts==1].index
    df_drop_na = df_drop_na[~df_drop_na['designation'].isin(values_to_drop)]
    value_counts = df_drop_na['variety'].value_counts()
    values_to_drop = value_counts[value_counts<100].index
    df_drop_na = df_drop_na[~df_drop_na['variety'].isin(values_to_drop)]
    value_counts = df_drop_na['province'].value_counts()
    values_to_drop = value_counts[value_counts<100].index
    df_drop_na = df_drop_na[~df_drop_na['province'].isin(values_to_drop)]

    df_cleaned = df_drop_na.reset_index(drop=True)
    return df_cleaned

def run_evaluation(model, tasters, data, scaled_data):
    """
    Run evaluation on model: for evaluation, we consider each taster's top 10 wines based on the points given.
    For each of the top 10, we look at the 5 closest neighbors as recommendations, and see what percentage of the 
    recommended wines were within <5 points of the original top10 wine of each taster-- thus demonstrating similar interest

    parameters:
        model: KNN trained model
        tasters: list of unique taster_name in the original dataset
        data: data that includes the points given to each wine by each taster
        scaled_data: the scaled data X used for unsupervising training of the KNN
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
            reference_wine = scaled_data[reference_index].reshape(1, -1)  # Reshape to match the input format expected by kneighbors
            _, indices = model.kneighbors(reference_wine)

            nearest_neighbor_indices = indices[0]  # Indices of nearest neighbors
            nearest_neighbor_names = wine_names.iloc[nearest_neighbor_indices]
            nearest_neighbor_names = nearest_neighbor_names[1:]

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
                if x<=5:
                    meets_threshold_count+=1
            if len(recommended_point_differences)!=0:
                tasters_differences.append(meets_threshold_count/len(recommended_point_differences))
        if len(tasters_differences)!=0:
            final_percentages_recommended_less5difference.append(sum(tasters_differences)/len(tasters_differences))
    return final_percentages_recommended_less5difference

def main():
    df_original = pd.read_csv('data/data_first10k.csv')
    df_cleaned = clean_data(df_original)

    data = pd.get_dummies(df_cleaned, columns=['country', 'designation', 'province', 'variety', 'winery' ])

    scaler = StandardScaler()
    X = data.drop(columns = ['title', 'taster_name', 'points'], axis=1)
    scaled_data = scaler.fit_transform(X)

    k = 6  # Number of neighbors to consider
    knn_model = NearestNeighbors(n_neighbors=k, metric='euclidean')  # You can use different metrics like 'cosine' for similarity
    knn_model.fit(scaled_data)

    tasters = data['taster_name'].unique().tolist()

    taster_percentages = run_evaluation(knn_model, tasters, data, scaled_data)
    
    if len(taster_percentages)!=0:
        print(sum(taster_percentages)/len(taster_percentages) *100)
        return sum(taster_percentages)/len(taster_percentages)
    return 0

if __name__ == "__main__":
    main()
