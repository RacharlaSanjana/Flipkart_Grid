# Flipkart_Grid
# Re.com - Flipkart Grid 5.0

*Submission by:*
- Sanjana Racharla
- Keerthi Sree Konkimalla
- Bhanu Prakash Sanikommu

## Problem Statement

In the dynamic landscape of online shopping and e-commerce, one of the most critical factors for success is the ability to provide users with personalized product recommendations and rankings. Users expect a tailored experience that aligns with their preferences and behavior. The challenge is to develop an algorithm or model that creates accurate and relevant product recommendations and rankings for individual users. The solution should consider user-specific and product-related factors, including historical interactions, product popularity, user similarities, and evolving market trends.

## Deliverables

Our comprehensive solution encompasses the following core facets:

1. *Personalized Recommendation Engine:* We have crafted an innovative recommendation engine that provides personalized product suggestions based on historical interactions, individual preferences, and product popularity.

2. *Scalability and Efficiency:* Our solution is designed for scalability and efficiency, accommodating extensive user bases and diverse product catalogs while maintaining a seamless user experience.

## Subproblems

1. *Web Scraping for Electronics Data:* We extracted data from electronics websites using BeautifulSoup in Python3.

2. *Model Training:* Models were trained on raw electronics dataset to learn product patterns.

3. *Popularity Metric Calculation:* Our algorithm determined product popularity by combining ratings and reviews.

4. *API Creation and Usage for Recommendations:* APIs were developed after model training and utilized to recommend products.

## Project Requirements

The project was implemented using the following tools and libraries:

- Python
- Beautiful Soup
- Scikit-learn (sklearn)
- NumPy
- Pandas
- SciPy
- Seaborn
- Flask

## Data Collection via Web Scraping

Web scraping was conducted using BeautifulSoup in Python3. We targeted three e-commerce websites for data extraction, focusing on electronics:

1. Flipkart
2. Amazon

The collected data included attributes such as product name, price, brand, and image links. Data was organized and stored in a CSV file.

## Simulated Interaction Data

A separate CSV file contained fabricated interactions data, emulating user interactions. Parameters included User ID, Product ID, Ratings, Subcategory, and Category. This dataset facilitated algorithm testing and user behavior modeling.

## Rank-Based Product Recommendation

*Objective:*
- Suggest products based on popularity determined by ratings.

*Outputs:*
- Recommend top products with a minimum of 50/100 ratings or interactions.

*Approach:*
1. Compute average rating for each product.
2. Calculate total number of ratings received by each product.
3. Construct DataFrame, arranging by average rating.
4. Develop function to extract top 'n' products with specified minimum interaction threshold.

## Similarity-Based Collaborative Filtering

*Objective:*
- Deliver personalized recommendations based on interactions of comparable users.

*Outputs:*
- Recommend products based on interactions of similar users.

*Approach:*
1. Convert user IDs to numerical values.
2. Identify users with similar preferences using cosine similarity.
3. Propose products considering preferences of similar users.

## Model-Based Collaborative Filtering

*Objective:*
- Provide tailored suggestions leveraging historical behaviors and addressing data sparsity.

*Outputs:*
- Offer top product recommendations tailored to specific users.

*Approach:*
1. Transform product rating matrix to compact CSR format.
2. Use Singular Value Decomposition (SVD) to reduce dimensionality.
3. Estimate projected ratings using SVD.
4. Store predicted ratings in DataFrame with user and product attributes.
5. Construct function to suggest products using predicted ratings and user preferences.
6. Gauge model performance using Root Mean Square Error (RMSE).

## API Integration and Web Interface

APIs were developed for all three recommendation models. Using Flask, APIs were integrated into a frontend web page. Users could receive personalized recommendations directly through the web interface, enhancing user experience.

## Installation and Usage

### Prerequisites

- Python 3.x
- Git (for repository cloning)

### Installation Steps

1. **Install Python:** Ensure Python 3.x is installed on your system. You can obtain it from the official Python website: [Python Downloads](https://www.python.org/downloads/)

2. **Clone the Repository:** Clone this repository to your local machine. Open a terminal or command prompt, navigate to the desired folder, and execute:

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

3. **Create a Virtual Environment (Optional but Recommended):** It's recommended to establish a virtual environment for managing project-specific dependencies. In your project folder, initiate:

   ```bash
   python -m venv venv
   ```

   - **Activate the Virtual Environment:**

     On Windows:

     ```bash
     venv\Scripts\activate
     ```

     On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:** Within the project folder, install the necessary libraries using pip, the Python package manager. If you possess a `requirements.txt` file, utilize:

   ```bash
   pip install -r requirements.txt
   ```

   If a `requirements.txt` file is absent, manually install the libraries enumerated in your project documentation.

5. **Run the Flask App:** Initiate the Flask app by executing the following command in the terminal:

   ```bash
   python app.py
   ```

   This will launch the development server, and you'll observe output confirming the app's operation.

6. **Access the Web Interface:** Open your web browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to interact with the web interface. Refer to your project documentation for effective utilization instructions.

---
