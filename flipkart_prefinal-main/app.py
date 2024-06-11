from flask import Flask, render_template
from apis.similar_user_api import similar_user_api_bp
from apis.rank_based_api import rank_based_api_bp
from apis.model_based_api import model_based_api_bp

app = Flask(__name__)

# Register blueprints for each API
app.register_blueprint(similar_user_api_bp, url_prefix='/api/similar_user')
app.register_blueprint(rank_based_api_bp, url_prefix='/api/rank_based')
app.register_blueprint(model_based_api_bp, url_prefix='/api/model_based')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
