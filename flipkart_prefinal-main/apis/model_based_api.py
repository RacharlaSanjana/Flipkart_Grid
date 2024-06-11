import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
from flask import Flask,Blueprint, request, jsonify, render_template

app = Flask(__name__)

model_based_api_bp = Blueprint('model_based_api', __name__)
# Load and preprocess your data
df = pd.read_csv('interactions_information.csv')
df.columns = ['user_id', 'product_id', 'categorie', 'sub_categorie', 'rating']

counts = df['user_id'].value_counts()
df_final = df[df['user_id'].isin(counts[counts >= 50].index)]
aggregated_df = df_final.groupby(['user_id', 'product_id'])['rating'].mean().reset_index()
final_ratings_matrix = aggregated_df.pivot_table(index='user_id', columns='product_id', values='rating', fill_value=0)
f=list(set(df['user_id']))
f.sort()
final_ratings_matrix['user_index'] = np.arange(0, final_ratings_matrix.shape[0])
final_ratings_matrix.set_index(['user_index'], inplace=True)
products_df = pd.read_csv("products_information.csv", encoding='ISO-8859-1')
products_df.columns = ['product_id', 'categories', 'sub_categories', 'product_name', 'price', 'image']

product_id_mapping = {idx: product_id for idx, product_id in enumerate(final_ratings_matrix.columns)}

final_ratings_sparse = csr_matrix(final_ratings_matrix.values)
U, s, Vt = svds(final_ratings_sparse, k=250)  # Set k to the desired number of latent features

# Construct diagonal array in SVD
sigma = np.diag(s)
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)

# Predicted ratings
preds_df = pd.DataFrame(abs(all_user_predicted_ratings), columns=final_ratings_matrix.columns)
preds_matrix = csr_matrix(preds_df.values)

def recommend_items_with_user_id(user_id, interactions_matrix, preds_matrix, num_recommendations, product_id_mapping, final_ratings_matrix):
        user_index=f.index(user_id)
        user_ratings = interactions_matrix[user_index, :].toarray().reshape(-1)
        user_predictions = preds_matrix[user_index, :].toarray().reshape(-1)

        temp = pd.DataFrame({'user_ratings': user_ratings, 'user_predictions': user_predictions})
        temp['Recommended Products'] = np.arange(len(user_ratings))
        temp = temp.set_index('Recommended Products')

        temp = temp.loc[temp.user_ratings == 0]
        temp = temp.sort_values('user_predictions', ascending=False)

        recommended_product_indices = temp.index[:num_recommendations]
        recommended_products = []

        for product_index in recommended_product_indices:
            product_id = product_id_mapping[product_index]
            user_id_for_product = find_user_id_for_product(user_index, product_id, final_ratings_matrix)
            if user_id_for_product:
                recommended_products.append(product_id)
                
            else:
                recommended_products.append(product_id)
                


        return recommended_products

def find_user_id_for_product(user_index, product_id, final_ratings_matrix):
    user_id = final_ratings_matrix.index[user_index]

    if final_ratings_matrix.loc[user_id, product_id] != 0:
        return user_id
    else:
        return None

# @app.route('/')
# def index():
#     return render_template('index.html')

@model_based_api_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        num_recommendations = data.get('num_recommendations', 10)

        if user_id not in df_final['user_id'].values:
            return jsonify({"error": "User ID not found"}), 404

        recommended_products = recommend_items_with_user_id(user_id, final_ratings_sparse, preds_matrix, num_recommendations, product_id_mapping, final_ratings_matrix)
        print(products_df)
        product_details = products_df[products_df['product_id'].isin(recommended_products)]
        print(product_details)
        product_list = product_details.to_dict(orient='records')
        print(product_list)

        return jsonify({"recommended_products": product_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
