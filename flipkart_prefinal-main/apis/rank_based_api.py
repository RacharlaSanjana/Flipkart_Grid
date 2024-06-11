import warnings
warnings.filterwarnings('ignore')
from flask_cors import CORS
import numpy as np
import pandas as pd

from flask import Flask,Blueprint, request, jsonify, render_template

app = Flask(__name__)

rank_based_api_bp = Blueprint('rank_based_api', __name__)
# Load and preprocess your data
df = pd.read_csv("interactions_information.csv")
df.columns = ['user_id', 'product_id', 'categorie', 'sub_categorie', 'rating']
# ... (your existing preprocessing code)
counts = df['user_id'].value_counts()
df_final = df[df['user_id'].isin(counts[counts >= 50].index)]
products_df = pd.read_csv("products_information.csv",encoding='ISO-8859-1')
products_df.columns = ['product_id', 'categories', 'sub_categories', 'product_name', 'price', 'image']
# Define the recommendation function
def generate_recommendations(sub_category):
    sub_cat = df_final[df_final['sub_categorie'] == sub_category].reset_index()
    aggregated_df = sub_cat.groupby(['user_id', 'product_id'])['rating'].mean().reset_index()

    final_ratings_matrix = aggregated_df.pivot_table(index='user_id', columns='product_id', values='rating', fill_value=0)
    given_num_of_ratings = np.count_nonzero(final_ratings_matrix)
    possible_num_of_ratings = final_ratings_matrix.shape[0] * final_ratings_matrix.shape[1]
    average_rating = aggregated_df.groupby('product_id').mean()['rating']

    # Calculate the count of ratings for each product
    count_rating = aggregated_df.groupby('product_id').count()['rating']
    # Create a dataframe with calculated average and count of ratings
    final_rating = pd.DataFrame({'avg_rating': average_rating, 'rating_count': count_rating})
    # Sort the dataframe by average of ratings
    final_rating = final_rating.sort_values(by='avg_rating', ascending=False)

    # Define the function to get the top n products based on highest average rating and minimum interactions
    def top_n_products(final_rating, n, min_interaction):
        # Finding products with minimum number of interactions
        recommendations = final_rating[final_rating['rating_count'] > min_interaction]
        # Sorting values w.r.t average rating
        recommendations = recommendations.sort_values('avg_rating', ascending=False)
        return recommendations.index[:n]

    recommendations = top_n_products(final_rating, 10, 50)  # Change '10' to the number of recommendations you want

    return recommendations

# # Define the root route to render the HTML page
# @app.route('/')
# def index():
#     return render_template('index.html')

# Define an API endpoint to get recommendations
@rank_based_api_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    sub_category = data.get('sub_category')

    recommendations = generate_recommendations(sub_category)

    recommendations = list(recommendations)
       # Get product details from the products_df based on the recommendations
    product_details = products_df[products_df['product_id'].isin(recommendations)]

    # Convert the product_details DataFrame to a list of dictionaries
    product_list = product_details.to_dict(orient='records')
    print(product_list)


    return jsonify({"recommendations": product_list})
    # Convert Int64Index to a list
 

    # output = most_popular

    # return jsonify(recommendation)
if __name__ == '__main__':
    app.run(debug=True)
