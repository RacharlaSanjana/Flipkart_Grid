import warnings
warnings.filterwarnings('ignore')
from flask_cors import CORS
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics.pairwise import cosine_similarity

from sklearn.metrics import mean_squared_error
from flask import Flask,Blueprint, request, jsonify, render_template

app = Flask(__name__)

similar_user_api_bp = Blueprint('similar_user_api', __name__)

# Load and preprocess your data
df = pd.read_csv("interactions_information.csv")
df.columns = ['user_id', 'product_id', 'categorie', 'sub_categorie', 'rating']

counts = df['user_id'].value_counts()
df_final = df[df['user_id'].isin(counts[counts >= 50].index)]
f=list(set(df['user_id']))
f.sort()
print(f)
aggregated_df = df_final.groupby(['user_id', 'product_id'])['rating'].mean().reset_index()
final_ratings_matrix = aggregated_df.pivot_table(index='user_id', columns='product_id', values='rating', fill_value=0)
products_df = pd.read_csv("products_information.csv", encoding='ISO-8859-1')
products_df.columns = ['product_id', 'categories', 'sub_categories', 'product_name', 'price', 'image']
final_ratings_matrix['user_index'] = np.arange(0, final_ratings_matrix.shape[0])
final_ratings_matrix.set_index(['user_index'], inplace=True)

# Function to get similar users
# defining a function to get similar users
def similar_users(user_index, interactions_matrix):
    similarity = []
    user_data = interactions_matrix.loc[user_index].values.reshape(1, -1)
    print("dfas")
    for user in range(interactions_matrix.shape[0]):
        other_user_data = interactions_matrix.loc[user].values.reshape(1, -1)        
        sim = cosine_similarity(user_data, other_user_data)[0][0]
        similarity.append((user, sim))
    similarity.sort(key=lambda x: x[1], reverse=True)
    most_similar_users = [tup[0] for tup in similarity]
    similarity_score = [tup[1] for tup in similarity]
    most_similar_users.remove(user_index)
    similarity_score.remove(similarity_score[0])

    return most_similar_users, similarity_score

# similar = similar_users(3,final_ratings_matrix)[0][0:10]

def recommendations(user_index, num_of_products, interactions_matrix):
    #Saving similar users using the function similar_users defined above
    most_similar_users = similar_users(user_index, interactions_matrix)[0]
    print("sdf")

    #Finding product IDs with which the user_id has interacted
    prod_ids = set(list(interactions_matrix.columns[np.where(interactions_matrix.loc[user_index] > 0)]))
    recommendations = []

    observed_interactions = prod_ids.copy()
    for similar_user in most_similar_users:
        if len(recommendations) < num_of_products:

            #Finding 'n' products which have been rated by similar users but not by the user_id
            similar_user_prod_ids = set(list(interactions_matrix.columns[np.where(interactions_matrix.loc[similar_user] > 0)]))
            recommendations.extend(list(similar_user_prod_ids.difference(observed_interactions)))
            observed_interactions = observed_interactions.union(similar_user_prod_ids)
        else:
            break

    return recommendations[:num_of_products]

# Define the root route to render the HTML page
# @app.route('/')
# def index():
#     return render_template('index.html')

# Define an API endpoint to get recommendations
@similar_user_api_bp.route('/recommendations', methods=['POST'])
def get_user_recommendations():
    print("////////////")
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        print(user_id)
        # Check if user_id exists in df_final
        if user_id not in df_final['user_id'].values:
            return jsonify({"error": "User ID not found"}), 404

        # Get the user index based on user_id
        user_index = f.index(user_id)
        print(user_index)
        # Get recommendations for the user index
        user_recommendations = recommendations(user_index, 10, final_ratings_matrix)
        print(user_recommendations)

        product_details = []
        for prod_id in user_recommendations:
            product = products_df[products_df['product_id'] == prod_id].iloc[0]
            product_details.append({
                "product_id": prod_id,
                "product_name": product['product_name'],
                "price": product['price'],
                "image_url": product['image']
            })

        return jsonify({"user_id": user_id, "recommendations": product_details})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)