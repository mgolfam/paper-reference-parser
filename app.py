from flask import Flask
from db import db
from routes import main_routes

app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///references.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# Register the routes from the routes.py file
app.register_blueprint(main_routes)

if __name__ == '__main__':
    # Create the database tables if they do not exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
